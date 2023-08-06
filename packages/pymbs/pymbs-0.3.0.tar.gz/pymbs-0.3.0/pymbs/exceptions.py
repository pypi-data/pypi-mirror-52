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

from io import StringIO
from logging import Logger
import re
import sys
from typing import NoReturn

from IPython.display import display
from jinja2 import Environment, PackageLoader, select_autoescape

from pymbs.enums import ExitCode

_jinja_env = Environment(
    loader=PackageLoader('pymbs', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def handle_gracefully(
        ipython_status: bool,
        logger: Logger,
        message: str,
        **kwargs: str) -> NoReturn:
    """Handle an error condition in a graceful manner.

    Args:
        ipython_status: The status as to whether or not PyMBS is running
            inside an IPython kernel. This status can be passed with the
            ``config._ipython_active`` attribute.

        logger: The logger object, passed in from the caller. This keeps
            references in the log to the actual module where the excpeption
            occured, rather than logging them as occuring inside the
            exceptions module.

        message: A string with the same name as one of the messages available
            in the GracefulMessage object, described below, in this module.

        kwargs: Keyword arguments, supplying any values interpolated in the
            message templates of the GracefulMessage object.
    """
    if message == 'no_deal':
        message = 'no_data'
        kwargs['data'] = 'deal'
    elif message == 'no_model':
        message = 'no_data'
        kwargs['data'] = 'model'
    elif message == 'no_model_file':
        message = 'no_file'
        kwargs['file_type'] = 'Model'
    elif message == 'no_terms':
        message = 'no_file'
        kwargs['file_type'] = 'Terms Sheet'
    elif message == 'no_pps':
        message = 'no_file'
        kwargs['file_type'] = 'Prepayment Scenario'

    kwargs['ipython_status'] = ipython_status
    msg = GracefulMessage(message, **kwargs)
    no_exit = kwargs.get('no_exit')
    if ipython_status:
        display(msg)
        msg = re.sub(r'\n', r'', str(msg))
        if no_exit:
            logger.warn(msg)
            return
        else:
            logger.error(msg)
            raise IpyExit
    else:
        print(msg)
        msg = re.sub(r'\n\n', r' ', str(msg))
        msg = re.sub(r'\n', r'', str(msg))
        if no_exit:
            logger.warning(msg)
            return
        else:
            exit_code = kwargs.get('exit_code')
            if not exit_code:
                exit_code = ExitCode.EX_GENERAL
            logger.error(msg)
            sys.exit(exit_code)


class GracefulMessage(object):
    """The GracefulMessage object allows various messages to be displayed in
    the most appropriate format, depending on how PyMBS is being used at the
    time.

    If PyMBS is being used in something like a Jupyter Notebook, where HTML
    can be displayed, it will display HTML. If the front-end is only
    capable of displaying text, it will display plain text.

    TODO: Implement a _repr_json_ method to output the error message as a
    JSON string, for when PyMBS is integrated with a RESTful/GraphQL API.
    """

    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs
        self.msg_template = _jinja_env.get_template(f"{self.message}.j2")

    def __repr__(self):
        """IPython actually misuses the conept of __repr__.
        It expects __repr__ to be a string, rather than an unambiguous
        representation of the object. The functionality the IPython expects
        from __repr__ is actually that delivered by __str__, but if I
        implement this method as __str__, rather than __repr__, IPython
        actually displays a __repr__ of the object, which is not what we
        want here!

        When in Rome...
        """
        msg = self.msg_template.render(**self.kwargs)
        return msg

    def _repr_html_(self):
        msg = self.msg_template.render(**self.kwargs)
        return msg


class IpyExit(SystemExit):
    """Exit Exception for IPython.

    Exception temporarily redirects stderr to buffer.
    """

    def __init__(self):
        # print("exiting")  # optionally print some message to stdout, too
        # ... or do other stuff before exit
        sys.stderr = StringIO()

    def __del__(self):
        sys.stderr.close()
        sys.stderr = sys.__stderr__  # restore from backup


class AssumedCollatError(Exception):
    """docstring for AssumedCollatError"""

    def __init__(self, group_id, repline_num=1):
        self.group_id = group_id
        self.repline_num = repline_num
        self.message = (
            f"Could not locate Repline {repline_num} for "
            f"Group {repr(group_id)}. Please check Assumed Collateral."
        )

    def __str__(self):
        return self.message


class CollatError(Exception):
    """docstring for AssumedCollatError"""

    def __init__(self, group_id):
        self.group_id = group_id
        self.message = (
            f"Could not locate collateral for "
            f"Group {repr(group_id)}. Please check the Terms Sheet."
        )

    def __str__(self):
        return self.message


class PrepaymentBenchmarkError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, prepayment_benchmark, message):
        self.prepayment_benchmark = prepayment_benchmark
        self.message = message


class DateError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, date, message):
        self.date = date
        self.message = message


class PayRuleError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, pay_rule, error):
        self.pay_rule = pay_rule
        self.error = error
        if self.error == 'invalid':
            self.message = f"The pay rule {pay_rule} is not a valid pay rule."
        elif self.error == 'no_parse':
            self.message = (
                f"The pay rule | {pay_rule} | was not parsed successfully. "
                f"\n\t\tPlease check the syntax."
            )

    def __str__(self):
        return self.message
