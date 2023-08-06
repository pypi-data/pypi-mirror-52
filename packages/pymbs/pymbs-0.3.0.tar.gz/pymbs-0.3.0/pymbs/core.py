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

from collections import namedtuple, OrderedDict
from copy import copy
from datetime import datetime
from dateutil.relativedelta import *
import decimal
import json
import os
from typing import Generator, Optional, Union

import pandas as pd

from pymbs import payment_rules  # noqa
from pymbs.config import config
from pymbs.enums import ALL_GROUPS, ExitCode, PrepayBenchmark, URL
from pymbs.exceptions import (
    AssumedCollatError, CollatError, DateError,
    PrepaymentBenchmarkError, handle_gracefully
)
from pymbs.log import get_logger
from pymbs.utils import ACNT, _parse_waterfall, _round_dec

logger = get_logger(__name__)

dec = decimal.Decimal
d0 = dec('0')
d1 = dec('1')
d12 = dec('12')
d100 = dec('100')


def _load_assumed_collat(
        group_id: Optional[Union[str, int]] = ALL_GROUPS) -> pd.DataFrame:
    if not config.terms_sheet:
        handle_gracefully(
            config._ipython_active,
            logger,
            'no_deal',
            exit_code=ExitCode.EX_CONFIG
        )
    else:
        ts = config.terms_sheet

    group_id = str(group_id)
    group_collat = None
    assumed_collat = None

    if group_id == ALL_GROUPS:
        for group in ts['groups']:
            try:
                group_collat = ts['groups'][group].get('collateral')
            except KeyError:
                raise CollatError(group)
            if group_collat:
                ac = _get_assumed_collat(group, group_collat)
                if assumed_collat is not None:
                    assumed_collat = assumed_collat.append(
                        ac, ignore_index=True
                    )
                else:
                    assumed_collat = ac
    else:
        try:
            group_collat = ts['groups'][group_id].get('collateral')
        except KeyError:
            raise CollatError(group_id)

        if group_collat:
            assumed_collat = _get_assumed_collat(group_id, group_collat)

    assumed_collat.index = range(1, len(assumed_collat) + 1)

    return assumed_collat


def _get_assumed_collat(group_id, group_collat):
    assumed_collat = None
    assumed = group_collat.get('assumed')
    if assumed:
        for item in assumed:
            if assumed_collat is not None:
                item['group_id'] = group_id
                assumed_collat = assumed_collat.append(
                    pd.Series(item), ignore_index=True
                )
            else:
                assumed_collat = pd.DataFrame(item, index=[0])
                assumed_collat.insert(0, "group_id", group_id)

    return assumed_collat


def _load_prepayment_scenarios(
        series_id: str,
        group_id: str) -> Union[Exception, dict, None]:

    pps_json = os.path.join(
        config.project_dir, f"{series_id}", f"{series_id}_pps.json"
    )
    try:
        with open(pps_json, 'r') as ppsj:
            pps = json.load(ppsj)
    except FileNotFoundError:
        handle_gracefully(
            config._ipython_active,
            logger,
            'no_pps',
            series_id=series_id,
            json_file=pps_json,
            exit_code=ExitCode.EX_NOINPUT
        )

    for scenario_group in pps['prepayment_scenarios']:
        if scenario_group['group_id'] == group_id:
            return scenario_group
            break
    else:
        return None


def _run_collat_cf(
        group_id: Union[str, int], repline_num: Optional[int] = -1) -> dict:
    # TODO: Run collateral cash flows for known collateral.
    # TODO: Run collateral cash flows for securitzed collateral.
    group_id = str(group_id)
    assumed_collat = _load_assumed_collat(group_id)

    if assumed_collat is None:
        raise AssumedCollatError(group_id)

    # We're using itertuples() here to loop over the dataframe of the replines
    # belonging to one group. This looping isn't ideal, from a performance
    # perspective, but we anticipate that the given dataframe will always be
    # small enough that there shouldn't be much of an impact.
    if repline_num < 0:
        i = 0
        for repline in assumed_collat.itertuples():
            if i == 0:
                cash_flows = _run_repline_cf(repline)
                i += 1
            else:
                cf = _run_repline_cf(repline)
                cash_flows.add(cf, fill_value=0)
    else:
        row = assumed_collat[assumed_collat['repline'] == repline_num]
        try:
            repline = ACNT(*row.values[0])
        except IndexError:
            raise AssumedCollatError(group_id, repline_num)
        else:
            cash_flows = _run_repline_cf(repline)

    return cash_flows


def _run_repline_cf(repline: namedtuple) -> dict:
    ts = config.terms_sheet

    series_id = ts['deal']['series_id']
    group_id = repline.group_id
    pps = _load_prepayment_scenarios(series_id, group_id)

    prepayment_benchmark = pps.get('prepayment_benchmark')
    prepayment_speeds = pps.get('speeds')
    # TODO: Need to figure out how to handle prepayment vectors correctly
    prepayment_vector = pps.get('vector')

    if not (prepayment_benchmark and prepayment_speeds) or prepayment_vector:
        raise PrepaymentBenchmarkError(
            'None',
            ('You must provide either a Prepayment Benchmark and a Prepayment '
             'Speed, or a Prepayment Vector.')
        )

    payment_period = ts['deal'].get('payment_period')
    first_payment_date = datetime.strptime(
        ts['deal'].get('first_payment_date'),
        '%Y-%m-%d'
    )

    if not first_payment_date:
        raise DateError(
            'None',
            'You must provide a First Payment Date.'
        )

    if prepayment_benchmark and prepayment_speeds:
        cash_flows = {}
        benchmark = pps['prepayment_benchmark']
        for speed in pps['speeds']:
            sched = pd.DataFrame(
                _amortize_repline(
                    repline.upb,
                    repline.wac,
                    repline.wam,
                    repline.wala,
                    repline.coupon,
                    payment_period,
                    prepayment_benchmark,
                    speed,
                    prepayment_vector,
                    first_payment_date
                )
            )
            sched.index = range(1, len(sched) + 1)
            cash_flows[f"{speed} {benchmark}"] = sched

        return cash_flows


def _amortize_repline(
        orig_upb: decimal.Decimal,
        wac: decimal.Decimal,
        wam: int,
        wala: int,
        coupon: decimal.Decimal,
        payment_period: Optional[int] = 12,
        prepayment_benchmark: Optional[str] = None,
        prepayment_speed: Optional[str] = None,
        prepayment_vector: Optional[list] = [],
        start_date: Optional[datetime] = None) -> Generator:

    ctx = decimal.getcontext()
    ctx.prec = config.precision
    ctx.Emax = config.emax
    ctx.Emin = config.emin
    decimal.setcontext(ctx)
    payment_period = dec(payment_period)
    prepayment_speed = dec(prepayment_speed)
    # initialize the variables to keep track of
    # the periods and running balances
    p = d1
    beg_balance = orig_upb
    end_balance = orig_upb

    # The Simple Periodic Rate is the wac divided by the payment_period
    spr = (wac / d100) / payment_period

    # The Monthly Passthrough Rate is the coupon divided by the payment_period
    mpr = (coupon / d100) / payment_period

    while end_balance > 0:

        # Recalculate the interest based on the current balance
        # interest = round(((coupon / payment_period) * beg_balance), 2)
        interest = (mpr * beg_balance)

        # Determine Single Monthly Mortality Rate for Current Period
        numerator = spr * ((d1 + spr)**(wam - p + d1))
        denominator = ((d1 + spr)**(wam - p + d1)) - d1

        if denominator > dec('0.00001'):
            pmt = beg_balance * (numerator / denominator)
        else:
            pmt = beg_balance

        smm = _calculate_smm(
            prepayment_benchmark, prepayment_speed, wala, p
        )

        sched_principal = pmt - (spr * beg_balance)

        prepayment = (beg_balance - sched_principal) * smm

        # Ensure additional payment gets adjusted if the loan is being paid off
        prepay_principal = min(prepayment, beg_balance - sched_principal)
        total_principal = sched_principal + prepay_principal
        cash_flow = interest + total_principal
        end_balance = beg_balance - (sched_principal + prepay_principal)

        yield OrderedDict([
            ('period', p),
            ('payment_date', start_date),
            ('beginning_balance', beg_balance),
            ('smm', smm),
            ('scheduled_payment', pmt),
            ('net_interest', interest),
            ('scheduled_principal', sched_principal),
            ('prepayment', prepay_principal),
            ('total_principal', total_principal),
            ('cash_flow', cash_flow),
            ('ending_balance', end_balance)
        ])

        # Increment the counter, balance and date
        p += d1
        start_date += relativedelta(months=1)
        beg_balance = end_balance


def _calculate_smm(
        prepayment_benchmark: str,
        prepayment_speed: decimal.Decimal,
        wala: int,
        period) -> decimal.Decimal:

    if prepayment_benchmark == PrepayBenchmark.PSA.value:
        benchmark_cpr = dec('0.06')
        seasoned_period = dec('30')

        if (period + wala) < seasoned_period:
            cpr = benchmark_cpr * ((period + wala) / seasoned_period)
        else:
            cpr = benchmark_cpr
        smm = d1 - (d1 - ((prepayment_speed / d100) * cpr))**(d1 / d12)
    elif prepayment_benchmark == PrepayBenchmark.CPR.value:
        pass
    else:
        raise PrepaymentBenchmarkError(
            prepayment_benchmark,
            f"Unknown Prepayment Benchmark: {prepayment_benchmark}"
        )

    return smm


def _calculate_wal(
        cash_flow: pd.DataFrame,
        collat_flag: Optional[bool] = False) -> decimal.Decimal:

    if collat_flag:
        principal = 'total_principal'
    else:
        principal = 'principal'
    cash_flow['period'] = cash_flow['period'].astype(str).transform(dec)
    wal = (sum(
        cash_flow['period'].apply(dec) * cash_flow[f"{principal}"]
    ) / (sum(cash_flow[f"{principal}"]) * d12))

    return wal


def _prepare_wals(
        group_id: str,
        model: dict) -> dict:

    _wals = {
        "columns": ["group_id", "tranche_id", "prepay_scenario", "wal"],
        "data": []
    }

    _group = model['groups'][group_id]
    collat_cf = _group['collat_cf']
    for prepay_scenario, cash_flow in collat_cf.items():
        collat_flag = True
        tranche_id = f"Group {group_id} Collat"
        wal = _calculate_wal(cash_flow, collat_flag)
        _wals['data'].append([group_id, tranche_id, prepay_scenario, wal])

    if model['groups'][group_id]['waterfall']:
        collat_flag = False
        for tranche_id in model['groups'][group_id]['tranches']:
            tranche_cfs = _group['tranches'][tranche_id].cash_flows.items()
            for prepay_scenario, cash_flow in tranche_cfs:
                # TODO: STOP this "SB" madness!!!
                # This goes away once we start paying-down notional
                # balances correctly.
                if tranche_id != "SB":
                    wal = _calculate_wal(cash_flow, collat_flag)
                    _wals['data'].append(
                        [group_id, tranche_id, prepay_scenario, wal]
                    )
    return _wals


def _round_wals(wals, precision):
    requested_precision = copy(precision)
    precision_exception_flag = False
    ctx = decimal.getcontext()
    max_allowed_prec = ctx.prec - 1
    for wal_item in wals['data']:
        wal = wal_item[3]
        wal_rep = wal.as_tuple()
        len_integer_part = len(wal_rep.digits) + wal_rep.exponent
        allowed_rounding_prec = ctx.prec - len_integer_part
        max_allowed_prec = min(
            precision, max_allowed_prec, allowed_rounding_prec
        )
        if allowed_rounding_prec < precision:
            precision_exception_flag = True

    if max_allowed_prec <= precision:
        precision = max_allowed_prec

    for wal_item in wals['data']:
        wal = wal_item[3]
        wal = _round_dec(wal_item[3], precision)
        wal_item[3] = wal

    if precision_exception_flag:
        handle_gracefully(
            config._ipython_active,
            logger,
            'rounding_error_wals',
            requested_precision=requested_precision,
            config_precision=config.precision,
            max_allowed_precision=max_allowed_prec,
            pymbs_config_url=URL.PYMBS_CONFIG.value,
            quantize_help_url=URL.QUANTIZE_HELP.value,
            no_exit=True
        )

    return wals


def _run_wals(
        group_id: str,
        precision: decimal.Decimal,
        model: dict) -> Union[dict, pd.DataFrame]:

    cash_flows = _run_collat_cf(group_id)
    model['groups'][group_id]['collat_cf'].update(cash_flows)
    if model['groups'][group_id]['waterfall']:
        tranches = _get_regular_tranches(model, group_id)
        _make_payments(model, group_id, cash_flows, tranches)
    wals = _prepare_wals(group_id, model)

    wals = _round_wals(wals, precision)

    return wals


def _pivot_wal_table(wals):
    column_order = [wal for wal in wals['prepay_scenario'].unique()]

    def f(x):
        return (x.pivot('tranche_id', 'prepay_scenario', 'wal'))

    _wal_table = wals.groupby('group_id', group_keys=True).apply(f)
    wal_table = _wal_table.reindex(columns=column_order)

    return wal_table


def _get_wals(
    group_id: Optional[Union[str, int]] = ALL_GROUPS,
    precision: Optional[int] = config.round_precision,
    data_frame_flag: Optional[bool] = False
) -> Union[dict, pd.DataFrame]:
    """Calulate the Weigted Average Lives (WALs) of all Regular tranches in the
    group specified, including those for the collateral. Currently WALs are NOT
    calcuated for Notional or MACR classes. This functionality will be exposed
    in a future release.

    If no Group number is specified in the call to this function, WALs will
    be calculated for all groups in the deal. This is not necessarily
    desireable, as the Prepayment Scenarios will be different for different
    groups, so the table that is returned will contain a number of 'missing'
    values. An enhancement to handle this gracefully will be provided in a
    future release. In the meantime, it is recommended that the user specify
    a group number when calling this function.

    Args:
        group_id: The number of the Group for which to run the WALs.
                  By default, this value is set to 'ALL_GROUPS', which will
                  run WALs for all of the groups in the deal at the Prepayment
                  Scenarios specified for each group.

        precision: The precision of the calculated WALs may be optionally
                   specified. If not specifed, it will use the
                   ``round_precision`` value specified in the configuration
                   object. This value is set to 10 decimal places by default,
                   which is almost always sufficient for tying-out the cash
                   flows with a counter-party. The precision of the WALs
                   disclosed in the Prospectus Supplement is 1 decimal.

    Returns:
        A Pandas Dataframe showing the WALs for each tranche, calulated based
        on the cash flows run at each Prepayment Sceanrio specified for the
        group.
    """
    if not config.model:
        handle_gracefully(
            config._ipython_active,
            logger,
            'no_model',
            exit_code=ExitCode.EX_CONFIG
        )
    else:
        model = config.model

    group_id = str(group_id)
    wals = {}

    if group_id == ALL_GROUPS:
        groups = config.terms_sheet['groups']
        for group in groups:
            if group != "R":
                _wals = _run_wals(group, precision, model)
                if data_frame_flag:
                    wal_table = pd.DataFrame.from_records(
                        _wals['data'],
                        columns=_wals['columns']
                    )
                    wal_table = _pivot_wal_table(wal_table)
                    wals[group] = wal_table
                else:
                    wals[group] = _wals
    else:
        _wals = _run_wals(group_id, precision, model)
        if data_frame_flag:
            wal_table = pd.DataFrame.from_records(
                _wals['data'],
                columns=_wals['columns']
            )
            wal_table = _pivot_wal_table(wal_table)
            wals[group_id] = wal_table
        else:
            wals = _wals

    return wals


def _get_regular_tranches(model: dict, group_id: str) -> list:

    tranches = []
    for tranche_id in model['groups'][group_id]['tranches']:
        tranche = model['groups'][group_id]['tranches'][tranche_id]
        if not tranche.macr:
            tranches.append(tranche)

    return tranches


def _make_payments(
        model: dict,
        group_id: str,
        cash_flows: pd.DataFrame,
        tranches: list) -> None:

    waterfall = model['groups'][group_id]['waterfall']
    if type(waterfall[0]) is str:
        waterfall = _parse_waterfall(model['groups'][group_id]['waterfall'])
    model['groups'][group_id]['waterfall'] = waterfall

    for prepay_scenario in cash_flows:
        collat_cf = cash_flows[prepay_scenario]
        for payment in collat_cf.itertuples():
            _pay_tranches(
                model, group_id, prepay_scenario, payment, tranches)

    for tranche in tranches:
        tranche.tabulate_cf()


def _pay_tranches(
        model: dict,
        group_id: str,
        prepay_scenario: str,
        payment: namedtuple,
        tranches: list) -> None:

    interest = payment.net_interest
    for tranche in tranches:
        tranche.new_periodic_cf(
            prepay_scenario,
            payment.period,
            payment.payment_date
        )
        interest = tranche.pay_interest(interest)
    _pay_waterfall(model, group_id, prepay_scenario, payment, tranches)
    for tranche in tranches:
        tranche.end_periodic_cf()


def _pay_waterfall(
        model: dict,
        group_id: str,
        prepay_scenario: str,
        payment: namedtuple,
        tranches: list) -> None:

    ctx = decimal.getcontext()
    ctx.prec = config.precision
    ctx.Emax = config.emax
    ctx.Emin = config.emin
    decimal.setcontext(ctx)
    waterfall = model['groups'][group_id]['waterfall']
    config.cache.update(
        model=model, prepay_scenario=prepay_scenario,
        group_id=group_id, payment=payment
    )
    for rule in waterfall:
        if rule['tranches']:
            tranches = [
                tranche for tranche in tranches if
                tranche.id in rule['tranches']
            ]
            config.cache.update(tranches=tranches)
        eval(f"payment_rules.{rule['func']}")
