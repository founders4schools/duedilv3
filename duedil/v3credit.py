# -*- coding: utf-8 -*-
#
#  DuedilApiClient v3 Pro + Credit
#  @copyright 2014 Christian Ledermann
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#

from .v3pro import Client as ProClient
from .v3pro import (COMPANY_FILTERS, COMPANY_RANGE_FILTERS,
                    DIRECTOR_FILTERS, DIRECTOR_RANGE_FILTERS)

from .v3pro import (
        AGE,
        CASH,
        CASH_DELTA_PERCENTAGE,
        CASH_TO_CURRENT_LIABILITIES_RATIO,
        CASH_TO_TOTAL_ASSETS_RATIO,
        CORPORATE,
        COST_OF_SALES,
        COST_OF_SALES_DELTA_PERCENTAGE,
        CURRENCY,
        CURRENT_ASSETS,
        CURRENT_ASSETS_DELTA_PERCENTAGE,
        CURRENT_RATIO,
        DATA_OF_BIRTH,
        DEBT_TO_CAPITAL_RATIO,
        DEPRECIATION,
        DEPRECIATION_DELTA_PERCENTAGE,
        DISQUALIFIED,
        EMPLOYEE_COUNT,
        GEARING,
        GENDER,
        GROSS_MARGIN_RATIO,
        GROSS_PROFIT,
        GROSS_PROFIT_DELTA_PERCENTAGE,
        INVENTORY_TURNOVER_RATIO,
        KEYWORDS,
        LIQUIDITY_RATIO,
        LOCALE,
        LOCATION,
        NAME,
        NATIONALITY,
        NET_ASSETS,
        NET_ASSETS_DELTA_PERCENTAGE,
        NET_PROFITABILITY,
        NET_WORTH,
        NET_WORTH_DELTA_PERCENTAGE,
        POSTCODE,
        PROFIT_RATIO,
        RETAINED_PROFITS,
        RETURN_ON_ASSETS_RATIO,
        RETURN_ON_CAPITAL_EMPLOYED,
        SECRETARIAL,
        SIC_2007_CODE,
        SIC_CODE,
        STATUS,
        TAXATION,
        TITLE,
        TOTAL_ASSETS,
        TOTAL_ASSETS_DELTA_PERCENTAGE,
        TOTAL_LIABILITIES,
        TOTAL_LIABILITIES_DELTA_PERCENTAGE,
        TURNOVER,
        TURNOVER_DELTA_PERCENTAGE
        )

class Client(ProClient):

    def __init__(self, api_key, sandbox=False):
        self.api_key = api_key
        if sandbox:
            self._url = 'http://duedil.io/v3/sandbox'
        else:
            self._url = 'http://duedil.io/v3-credit'

