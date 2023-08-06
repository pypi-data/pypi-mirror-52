"""
PyMBS is a Python library for use in modeling Mortgage-Backed Securities.

Copyright (C) 2019  Brian Farrell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: brian.farrell@me.com
"""

from collections import namedtuple
import decimal
import json
import re

from pymbs.config import config
from pymbs.enums import URL
from pymbs.exceptions import handle_gracefully, PayRuleError
from pymbs.log import get_logger

logger = get_logger(__name__)

dec = decimal.Decimal

ACNT = namedtuple('AssumedRepline', [
    'group_id',
    'repline',
    'upb',
    'coupon',
    'original_term',
    'wac',
    'wam',
    'wala'
])

PNT = namedtuple('Pandas', [
    'Index',
    'period',
    'payment_date',
    'beginning_balance',
    'smm',
    'scheduled_payment',
    'net_interest',
    'scheduled_principal',
    'prepayment',
    'total_principal',
    'cash_flow',
    'ending_balance',
    'buckets'
])


def _round_dec(decimal_value, precision=config.round_precision):
    places = dec('10') ** dec(f"{-precision}")
    try:
        rounded_value = decimal_value.quantize(places)
    except decimal.InvalidOperation:
        ctx = decimal.getcontext()
        dv_rep = decimal_value.as_tuple()
        len_integer_part = len(dv_rep.digits) + dv_rep.exponent
        max_allowed_precision = ctx.prec - len_integer_part
        places = dec('10') ** dec(f"{-max_allowed_precision}")
        rounded_value = decimal_value.quantize(places)
        handle_gracefully(
            config._ipython_active,
            logger,
            'rounding_error',
            decimal_value=decimal_value,
            precision=precision,
            config_precision=config.precision,
            max_allowed_precision=max_allowed_precision,
            pymbs_config_url=URL.PYMBS_CONFIG.value,
            quantize_help_url=URL.QUANTIZE_HELP.value,
            no_exit=True
        )
    return rounded_value


def _parse_waterfall(waterfall):
    wf = []
    for rule in waterfall:
        pr = re.match(
            r'(?P<full_rule>(?P<pay_rule>\w+)\('
            r'(?P<buckets>\[(?:\'\w+\'(?:,\s|\]))*)'
            r'(?:,\s(?P<tranches>\[(?:\'\w+\'(?:,\s|\]))*))?(?:(?:,\s)'
            r'(?:\'(?P<expression>.*)\'))?\))',
            rule,
            re.S
        )

        if not pr:
            raise PayRuleError(rule, 'no_parse')

        if pr.group('pay_rule') == 'pay_accrue':
            if pr.group('tranches') or pr.group('expression'):
                raise PayRuleError(pr.group('full_rule'), 'invalid')
            else:
                func = pr.group('full_rule')
                # In the case of the pay_accrue rule, the tranches to accrue
                # are captured by the 'buckets' group
                tranches = pr.group('buckets')
        elif pr.group('pay_rule') == 'calculate':
            if pr.group('tranches'):
                raise PayRuleError(pr.group('full_rule'), 'invalid')
            else:
                func = pr.group('full_rule')
                tranches = None
        else:
            if pr.group('pay_rule') not in ['pay_accrue', 'calculate']:
                if pr.group('expression') or not \
                        (pr.group('buckets') and pr.group('tranches')):
                    raise PayRuleError(pr.group('full_rule'), 'invalid')
                else:
                    func = pr.group('full_rule')
                    tranches = pr.group('tranches')
        wf.append(dict(tranches=tranches, func=func))
    return wf


def _parse_expression(exp):
    expr_tokens = re.match(
        r'(?P<first_term>(?:COLL|(?:^COLL|[A-Za-z0-9]))+?_'
        r'(?:PRINCIPAL|ACCRUAL|PREPAY|BALANCE|SCHEDULED|VAR))'
        r'(?:\s(?P<operator>\+|\-|\*|\/)\s)'
        r'(?=(?:(?:COLL|(?:^COLL|[A-Za-z0-9])+)_'
        r'(?:PRINCIPAL|ACCRUAL|PREPAY|BALANCE|SCHEDULED|VAR)))'
        r'(?<=(?:\s(?:\+|\-|\*|\/)\s))'
        r'(?P<second_term>(?:COLL|(?:^COLL|[A-Za-z0-9]))+?_'
        r'(?:PRINCIPAL|ACCRUAL|PREPAY|BALANCE|SCHEDULED|VAR))', exp, re.S)

    first_term_tokens = re.findall(
        r'(?P<token>[A-Za-z0-9]+)', expr_tokens.group('first_term'), re.S)

    second_term_tokens = re.findall(
        r'(?P<token>[A-Za-z0-9]+)', expr_tokens.group('second_term'), re.S)

    # If the first token is 'COLL', then we assume that it is referring to the
    # collater cash flow passed to the calling function
    if first_term_tokens[0] == 'COLL':
        ft_1 = 'payment'
    # If the first token is NOT COLL and the second token is NOT VAR, then we
    # assume that it is referreing to cash flow of a Tranche in the same
    # group as the one for which the waterfall is being run
    if first_term_tokens[0] != 'COLL' and first_term_tokens[1] != 'VAR':
        ft_1 = (f"model['groups'][group_id]['tranches']"
                f"['{first_term_tokens[0]}'].periodic_cf")

    # If the second token is VAR, then the first token is the name of the
    # variable being evaluated
    if first_term_tokens[1] == 'VAR':
        ft_1 = first_term_tokens[0]
        ft_2 = ''
    elif first_term_tokens[1] == 'PRINCIPAL':
        ft_2 = 'total_principal'
    elif first_term_tokens[1] == 'ACCRUAL':
        ft_2 = 'accrual'
    elif first_term_tokens[1] == 'PREPAY':
        ft_2 = 'prepayment'
    elif first_term_tokens[1] == 'BALANCE':
        ft_2 = 'beginning_balance'
    elif first_term_tokens[1] == 'SCHEDULED':
        ft_2 = 'scheduled_principal'

    # If the first token is 'COLL', then we assume that it is referring to the
    # collater cash flow passed to the calling function
    if second_term_tokens[0] == 'COLL':
        st_1 = 'payment'
    # If the first token is NOT COLL and the second token is NOT VAR, then we
    # assume that it is referreing to cash flow of a Tranche in the same
    # group as the one for which the waterfall is being run
    if second_term_tokens[0] != 'COLL' and first_term_tokens[1] != 'VAR':
        st_1 = (f"model['groups'][group_id]['tranches']"
                f"['{second_term_tokens[0]}'].periodic_cf")

    # If the second token is VAR, then the first token is the name of the
    # variable being evaluated
    if second_term_tokens[1] == 'VAR':
        st_1 = second_term_tokens[0]
        st_2 = ''
    elif second_term_tokens[1] == 'PRINCIPAL':
        st_2 = 'total_principal'
    elif second_term_tokens[1] == 'ACCRUAL':
        st_2 = 'accrual'
    elif second_term_tokens[1] == 'PREPAY':
        st_2 = 'prepayment'
    elif second_term_tokens[1] == 'BALANCE':
        st_2 = 'beginning_balance'
    elif second_term_tokens[1] == 'SCHEDULED':
        st_2 = 'scheduled_principal'

    if ft_2 == '':
        term_1 = f"{ft_1} "
    else:
        term_1 = f"{ft_1}.{ft_2}"

    if st_2 == '':
        term_2 = f"{st_1} "
    else:
        term_2 = f"{st_1}['{st_2}']"

    operator = f" {expr_tokens.group('operator')} "

    return f"{term_1}{operator}{term_2}"


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


class TSDecimalDecoder(json.JSONDecoder):
    """TSDecimalDecoder is a custom JSON decoder for the Terms Sheet
    """

    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook)

    def object_hook(self, obj):
        dict_keys = ['deal', 'pricing_speed', ]
        list_dict_keys = [
            'assumed',
            'known',
            'notional_with',
            'securitized',
            'schedules',
            'tranches'
        ]
        list_str_keys = ['range', 'values']

        for k, v in obj.items():
            if k in dict_keys:
                item = self.decimalize_dict(obj[k])
                obj[k].update(item)
            elif k in list_dict_keys:
                for idx, item in enumerate(obj[k]):
                    item = self.decimalize_dict(item)
                    obj[k][idx].update(item)
            elif k in list_str_keys:
                for idx, item in enumerate(obj[k]):
                    item = self.decimalize(item)
                    obj[k][idx] = item
        return obj

    def decimalize(self, value):
        try:
            value = decimal.Decimal(value)
        except (decimal.InvalidOperation, TypeError):
            pass
        return value

    def decimalize_dict(self, dct):
        for k, v in dct.items():
            if isinstance(dct[k], str):
                try:
                    value = decimal.Decimal(dct[k])
                except (decimal.InvalidOperation, TypeError):
                    pass
                else:
                    dct[k] = value
        return dct
