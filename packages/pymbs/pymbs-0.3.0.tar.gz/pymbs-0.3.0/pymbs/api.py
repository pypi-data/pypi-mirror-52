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

from copy import deepcopy
import decimal
import json
import os
from typing import NoReturn, Optional, Union

from IPython.display import display, HTML
import pandas as pd

from pymbs import core
from pymbs.config import config
from pymbs.enums import ALL_GROUPS, ExitCode
from pymbs.exceptions import handle_gracefully
from pymbs.log import get_logger
from pymbs.tranche import IndexRate, Tranche
from pymbs.utils import TSDecimalDecoder, DecimalEncoder

__all__ = ['load_deal', 'load_assumed_collat', 'load_model', 'run_collat_cf',
           'run_wals', 'show_wals', 'load_tranches', 'disperse_cf']

logger = get_logger(__name__)

pd.set_option('display.max_rows', config.max_rows)
pd.set_option('precision', config.precision)


def load_deal(series_id: str) -> dict:
    """Load the Terms Sheet for the REMIC Series name provided.

    The Terms Sheet is essential for modeling the deal. If this function is
    not called at the start, most of the other functions will fail.

    Within the project_dir, specified in the user's configuration file, it is
    expected that there will be one subdirectory for each REMIC Series name.
    Inside the Series directory, it is expected that the Terms Sheet will be
    a file named ``series_ts.json``, where 'series' refers to the actual
    Series name.

    Args:
        series_id: The REMIC Series id. Note that this value is passed
        as a string, so it need not be strictly an integer value, i.e. 'T-074'.
        The value *must* be the same as the name of the deal directory, which
        is a subdirectory of the project_directory.

    Returns:
        A dictionary object, representing the Terms Sheet.  All numerical
        values related to the model and represented as Strings in the Terms
        Sheet will be converted to a Python Decimal type in the dictionary
        that is returned.

        If the Terms Sheet file is not located, returns Exit Code 66.

    Example:
        Given: REMIC Series Name is ``'2618'``

        Path: ``/project_dir/2618/2618_ts.json``
    """
    ts_json = os.path.join(
        config.project_dir, f"{series_id}", f"{series_id}_ts.json"
    )
    try:
        with open(ts_json, 'r') as tsj:
            config.terms_sheet = json.load(tsj, cls=TSDecimalDecoder)
    except FileNotFoundError:
        handle_gracefully(
            config._ipython_active,
            logger,
            'no_terms',
            series_id=series_id,
            json_file=ts_json,
            exit_code=ExitCode.EX_NOINPUT
        )

    return config.terms_sheet


def load_assumed_collat(
        group_id: Optional[Union[str, int]] = ALL_GROUPS) -> pd.DataFrame:
    """Load the Assumed Collateral replines from the Terms Sheet.

    This assumes that the Terms Sheet has already been loaded, using the
    ``load_deal()`` function.

    This will *only* load Assumed Collateral. PyMBS does not yet have the
    ability to handle Known Collateral or Securitzed Collateral. It can
    however handle multiple Assumed replines per group.
    """
    assumed_collat = core._load_assumed_collat(group_id)

    return assumed_collat


def load_model() -> dict:
    """Load the structured cash flow model from the Terms Sheet, supplemented
    by the model file.

    The Terms sheet does NOT include the pay rule waterfall or specific
    benchmark interest rate information used by the model. These are provided
    in a separate JSON file.

    Within the project_dir, specified in the user's configuration file, it is
    expected that there will be one subdirectory for each REMIC Series name.
    Inside the Series directory, it is expected that the Model File named as
    provided as argument to this function will exist.

    Args:
        model_json: The name of the model file inside the Series directory.

    Returns:
        A dictionary object, representing the structured cash flow model.

        If the Model file is not located, returns Exit Code 66.

    Example:
        Given: ``model_json = 2618_model.json``

        Path: ``/project_dir/2618/2618_model.json``
    """
    if not config.terms_sheet:
        handle_gracefully(
            config._ipython_active,
            logger,
            'no_deal',
            exit_code=ExitCode.EX_CONFIG
        )
    else:
        ts = config.terms_sheet
    series_id = ts['deal']['series_id']
    model_json = os.path.join(
        config.project_dir, f"{series_id}", f"{series_id}_model.json"
    )
    try:
        with open(model_json, 'r') as mj:
            mf = json.load(mj, parse_float=decimal.Decimal)
    except FileNotFoundError:
        handle_gracefully(
            config._ipython_active,
            logger,
            'no_model_file',
            series_id=series_id,
            json_file=model_json,
            exit_code=ExitCode.EX_NOINPUT
        )
    groups = deepcopy(ts['groups'])

    indices = {}
    for group in groups:
        tranches = {}
        if group != "R":
            groups[group]['collat_cf'] = {}
            groups[group]['waterfall'] = []
            groups[group]['waterfall'].extend(mf['waterfall'][group])
        for tranche in groups[group]['tranches']:
            tranche_obj = Tranche(
                group_id=group,
                **tranche,
                dated_date=ts['deal']['issue_date'],
                next_payment_date=groups[group]['first_payment_date']
            )
            tranches[tranche['class_id']] = tranche_obj
        groups[group]['tranches'] = tranches
    for index in mf['indices']:
        indices[index['name']] = IndexRate(**index)
    config.model['groups'] = groups
    config.model['indices'] = indices

    return config.model


def run_collat_cf(
        group_id: Optional[Union[str, int]] = ALL_GROUPS,
        repline_num: Optional[int] = -1) -> dict:
    """Run cash flows from Assumed Collateral replines specified in the
    Terms Sheet. A Pandas DataFrame is created for each cash flow prepayment
    scenario, as specified in the Prepayment Scenarios JSON file.

    The Terms sheet does NOT include the pay rule waterfall or specific
    benchmark interest rate information used by the model. These are provided
    in a separate JSON file.

    Within the project_dir, specified in the user's configuration file, it is
    expected that there will be one subdirectory for each REMIC Series name.
    Inside the Series directory, it is expected that the Model File named as
    provided as argument to this function will exist.

    Args:
        group_id: The number of the Group for which to run the cash flows.
                  By default, this value is set to 'ALL_GROUPS', which will
                  run cash flows for all of the groups in the deal at the
                  Prepayment Scenarios specified for each group.

        repline_num: Optionally, the user may specify running the cash flows
                     for a specific repline in a specific group, if the group
                     has more than one assumed repline. As with ``group_id``,
                     the ``repline_num`` is set to -1 by default, which will
                     run cash flows for ALL replines associated with a group.
                     When run together, the cash flows for each repline will
                     be aggregated into one final cash flow which is the one
                     that is returned for the group.

    Returns:
        A dictionary object, containing a Pandas Dataframe for the cash flow
        calculated at each Prepayment Scenario.

    Example:
        Path: ``/project_dir/2618/2618_pps.json``

    TODO: Run collateral cash flows for known collateral.

    TODO: Run collateral cash flows for securitzed collateral.
    """
    group_id = str(group_id)
    cash_flows = {}
    if group_id == ALL_GROUPS:
        for group in config.terms_sheet['groups']:
            if group != 'R':
                cf = core._run_collat_cf(group, repline_num)
                cash_flows[group] = cf
    else:
        cf = core._run_collat_cf(group_id, repline_num)
        cash_flows[group_id] = cf

    return cash_flows


def run_residual_cf() -> pd.DataFrame:
    """Not yet implemented.
    """
    pass


def run_wals(
        group_id: Optional[Union[str, int]] = ALL_GROUPS,
        precision: Optional[int] = config.round_precision) -> str:
    """Get the WALs as a dictionary and return them as JSON
    """
    _wals = core._get_wals(group_id, precision)
    wals = json.dumps(_wals, cls=DecimalEncoder, separators=(',', ':'))

    return wals


def show_wals(
        group_id: Optional[Union[str, int]] = ALL_GROUPS,
        precision: Optional[int] = config.round_precision) -> NoReturn:
    """Get the WALs as a Pandas DataFrame and display them in
    a Jupyter Notebook.
    """
    wals = core._get_wals(group_id, precision, data_frame_flag=True)
    display(HTML("<p><pre>\n</pre></p>"))
    for group in wals.keys():
        display(wals[group])
        display(HTML("<p><pre>\n\n</pre></p>"))


def load_tranches(
        group_id: Optional[Union[str, int]] = ALL_GROUPS) -> pd.DataFrame:
    """Load the tranches for the deal, or for the group specified, into a
    Pandas Dataframe for easy display in the Jupyter Notebook.

    Args:
        group_id: The number of the Group for which to load the tranches.
                  By default, this value is set to 'ALL_GROUPS', which will
                  load the tranches for all of the groups in the deal. As per
                  convention, the Residual tranches will appear in
                  Group '0'.

    Returns:
        A Pandas Dataframe showing Tranche details for each tranche queried.
    """
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
    tranches = None

    if group_id == ALL_GROUPS:
        for group in ts['groups']:
            if tranches is None:
                tranches = pd.DataFrame(
                    ts['groups'][group]['tranches']
                )
                tranches.insert(0, "group_id", group)
            else:
                tr = pd.DataFrame(ts['groups'][group]['tranches'])
                tr.insert(0, "group_id", group)
                tranches = tranches.append(
                    tr,
                    ignore_index=True
                )
    else:
        tranches = pd.DataFrame(ts['groups'][group_id]['tranches'])
        tranches.insert(0, "group_id", group_id)

    tranches.index = range(1, len(tranches) + 1)

    return tranches


def disperse_cf(
        model: dict,
        group_id: Optional[Union[str, int]] = ALL_GROUPS) -> NoReturn:
    """Make all payments of Interest and Principal, based on the rules
    enumerated in the model.

    Args:
        model: The structured cash flow model containing the payment rules
               waterfall for the group(s)

        group_id: The number of the Group for which to load the tranches.
                  By default, this value is set to 'ALL_GROUPS', which will
                  load the tranches for all of the groups in the deal. As per
                  convention, the Residual tranches will appear in
                  Group '0'.
    """
    group_id = str(group_id)
    if group_id == ALL_GROUPS:
        for group in model['groups']:
            cash_flows = run_collat_cf(group)
            model['groups'][group]['collat_cf'].update(cash_flows)
            tranches = core._get_regular_tranches(model, group)
            core._make_payments(model, group, cash_flows, tranches)
    else:
        cash_flows = run_collat_cf(group_id)
        model['groups'][group_id]['collat_cf'].update(cash_flows)
        tranches = core._get_regular_tranches(model, group_id)
        core._make_payments(model, group_id, cash_flows, tranches)
