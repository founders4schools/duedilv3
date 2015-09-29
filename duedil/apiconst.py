# -*- coding: utf-8 -*-
#
#  DuedilApiConstanstants v3
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

# Here are all the terms available in the companies filters parameter.

LOCALE = "locale"  # string
# This terms accepts only the values uk or roi.

LOCATION = "location"  # string
# This term accepts the name of a city and/or the address.

POSTCODE = "postcode"  # string
# This term accepts a valid uk postcode.

SIC_CODE = "sic_code"  # integer
# sic_code. This term accepts only the standard SIC 03 code

SIC_2007_CODE = "sic_2007_code"  # integer
# sic_2007_code. This term accepts only the standard SIC 07 code

STATUS = "status"  # string
# This term accepts only active, dissolved, in receivership or liquidation
# queries.

CURRENCY = "currency"  # float
# This term accepts only the value eur or gbp

KEYWORDS = "keywords"  # string
# Search keywords

NAME = "name"  # string
# The name of the company you’re looking for. This field must be a string.

COMPANY_TERM_FILTERS = [
    LOCALE,
    LOCATION,
    POSTCODE,
    SIC_CODE,
    SIC_2007_CODE,
    STATUS,
    CURRENCY,
    KEYWORDS,
    NAME,
]


# Here are all the ranges available in the filters parameter.
# These ranges must have an integer value.

EMPLOYEE_COUNT = "employee_count"  # string
# Number of people employed by the company. NB: employee numbers not
# available for all companies. As such when searching for employee
# numbers, only companies with this data available will be searched.

TURNOVER = "turnover"  # string
# The income a company receives from normal business activities.
# Internationally known as "revenue".

TURNOVER_DELTA_PERCENTAGE = "turnover_delta_percentage"  # string
# Movement in turnover from previous year’s filing to latest filing.

GROSS_PROFIT = "gross_profit"  # string
# Turnover minus the cost of sales. Gross profit doesn't include
# administrative, financial, or distribution costs.

GROSS_PROFIT_DELTA_PERCENTAGE = "gross_profit_delta_percentage"  # string
# Movement in gross profit from previous year’s filing to latest filing.

COST_OF_SALES = "cost_of_sales"  # string
# Costs attributable to the production of the goods or supply of services.

COST_OF_SALES_DELTA_PERCENTAGE = "cost_of_sales_delta_percentage"  # string
# Movement in cost of sales from previous year’s filing to latest filing.

NET_ASSETS = "net_assets"  # string
# Net assets refers to the value of a company's assets minus its liabilities.

NET_ASSETS_DELTA_PERCENTAGE = "net_assets_delta_percentage"  # string
# percentage change between the latest filing's value and previous
# filing's value of net assets.

CURRENT_ASSETS = "current_assets"  # string
# All assets belonging to a company that can be converted easily into cash
# and are expected to be used (sold or consumed) within a year.

CURRENT_ASSETS_DELTA_PERCENTAGE = "current_assets_delta_percentage"  # string
# The change in the current assets value from the previous year’s filing
# to latest filing.

TOTAL_ASSETS = "total_assets"  # string
# The sum of current and long-term assets owned by the company.

TOTAL_ASSETS_DELTA_PERCENTAGE = "total_assets_delta_percentage"  # string
# The change in the total assets value from previous year’s filing to
# latest filing.

CASH = "cash"  # string
# Included in current assets, cash refers to the amount held in current or
# deposit bank accounts, and is seen as a highly liquid form of current
# asset.

CASH_DELTA_PERCENTAGE = "cash_delta_percentage"  # string
# Movement in cash from previous year’s filing to latest filing.

TOTAL_LIABILITIES = "total_liabilities"  # string
# The total of all debts for which a company is liable; includes
# short-term and long-term liabilities.

# string
TOTAL_LIABILITIES_DELTA_PERCENTAGE = "total_liabilities_delta_percentage"
# The change in the value of total liabilities from previous year’s filing
# to latest filing.

NET_WORTH = "net_worth"  # string
# The amount by which assets exceed liabilities. Net worth is a concept
# applicable to businesses as a measure of how much an entity is worth.

NET_WORTH_DELTA_PERCENTAGE = "net_worth_delta_percentage"  # string
# Movement in net worth from previous year’s filing to latest filing.

DEPRECIATION = "depreciation"  # string
# A decrease in the value of company assets. Depreciation indicates how
# much of an asset's value has been used up.

DEPRECIATION_DELTA_PERCENTAGE = "depreciation_delta_percentage"  # string
# Movement in depreciation from previous year’s filing to latest filing.

TAXATION = "taxation"  # string
# Amount set aside for taxation purposes.

RETAINED_PROFITS = "retained_profits"  # string
# Profit kept in the company rather than paid out to shareholders as a
# dividend.

PROFIT_RATIO = "profit_ratio"  # string
# The profit ratio measures the amount of profit generated by each £1 of
# sales. Calculated as net profit / turnover.

INVENTORY_TURNOVER_RATIO = "inventory_turnover_ratio"  # string
# The number of times the stock is sold and replaced in a year (calculated
# as sales divided by stock).

NET_PROFITABILITY = "net_profitability"  # string
# The amount of sales needed to generate £1 of net profit. Calculated as
# turnover / net profit.

RETURN_ON_CAPITAL_EMPLOYED = "return_on_capital_employed"  # string
# The profit generated as a function of the capital invested in the
# business (calculated as net profit divided by capital employed).

CASH_TO_TOTAL_ASSETS_RATIO = "cash_to_total_assets_ratio"  # string
# The percentage of the company's assets that are held as cash (calculated
# as cash divided by total assets).

GEARING = "gearing"  # string
# The debt to equity ratio in the business (calculated as total long term
# liabilities divided by shareholder equity).

GROSS_MARGIN_RATIO = "gross_margin_ratio"  # string
# The gross profitability generated by the business as a percentage of the
# turnover received before accounting for fixed costs and overheads
# (calculated as gross profit divided by turnover).

RETURN_ON_ASSETS_RATIO = "return_on_assets_ratio"  # string
# The profit generated in a business as a function of the assets held
# (calculated as gross profit divided by total assets).

CURRENT_RATIO = "current_ratio"  # string
# A measure of the company's short term solvency (calculated as current
# assets divided by current liabilities).

DEBT_TO_CAPITAL_RATIO = "debt_to_capital_ratio"  # string
# A measure of the company's leverage (calculated as total liabilities
# divided by the total shareholder equity plus total liabilities).

# string
CASH_TO_CURRENT_LIABILITIES_RATIO = "cash_to_current_liabilities_ratio"
# A measure of the company's ability to meet its short term obligations
# (calculated as cash divided by short term liabilities).

LIQUIDITY_RATIO = "liquidity_ratio"  # string
# A measure of the company's ability to meet short term obligations by
# liquidating certain assets, excluding its stock (calculated as current
# assets less stock divided by current liabilities).

COMPANY_RANGE_FILTERS = [
    EMPLOYEE_COUNT,
    TURNOVER,
    TURNOVER_DELTA_PERCENTAGE,
    GROSS_PROFIT,
    GROSS_PROFIT_DELTA_PERCENTAGE,
    COST_OF_SALES,
    COST_OF_SALES_DELTA_PERCENTAGE,
    NET_ASSETS,
    NET_ASSETS_DELTA_PERCENTAGE,
    CURRENT_ASSETS,
    CURRENT_ASSETS_DELTA_PERCENTAGE,
    TOTAL_ASSETS,
    TOTAL_ASSETS_DELTA_PERCENTAGE,
    CASH,
    CASH_DELTA_PERCENTAGE,
    TOTAL_LIABILITIES,
    TOTAL_LIABILITIES_DELTA_PERCENTAGE,
    NET_WORTH,
    NET_WORTH_DELTA_PERCENTAGE,
    DEPRECIATION,
    DEPRECIATION_DELTA_PERCENTAGE,
    TAXATION,
    RETAINED_PROFITS,
    PROFIT_RATIO,
    INVENTORY_TURNOVER_RATIO,
    NET_PROFITABILITY,
    RETURN_ON_CAPITAL_EMPLOYED,
    CASH_TO_TOTAL_ASSETS_RATIO,
    GEARING,
    GROSS_MARGIN_RATIO,
    RETURN_ON_ASSETS_RATIO,
    CURRENT_RATIO,
    DEBT_TO_CAPITAL_RATIO,
    CASH_TO_CURRENT_LIABILITIES_RATIO,
    LIQUIDITY_RATIO,
]


# This “Director search endpoint” is similar to the “Company search
# endpoint”, though with some different ranges and terms.

# Searching by financial range will return directors who have a
# directorship at a company fulfilling that range.

# NB: The location filter is not available for director search.


NAME = "name"  # string
# This field must be a string that contains the director’s name.

GENDER = "gender"  # string
# This term accepts only the value M or F

TITLE = "title"  # string
# View all available titles.

NATIONALITY = "nationality"  # string
# View all available nationalities.

SECRETARIAL = "secretarial"  # boolean
# This is a boolean field; the values accepted are true or false

CORPORATE = "corporate"  # boolean
# This is a boolean field; the values accepted are true or false

DISQUALIFIED = "disqualified"  # string
# This is a boolean field; the values accepted are true or false

DIRECTOR_TERM_FILTERS = [
    NAME,
    GENDER,
    TITLE,
    NATIONALITY,
    SECRETARIAL,
    CORPORATE,
    DISQUALIFIED,
]


AGE = "age"  # string
# The age brackets of the director

DATA_OF_BIRTH = "data_of_birth"  # dateTime
# The date of birth brackets of the director. The data must be in this
# format MM/DD/YYY

GROSS_PROFIT = "gross_profit"  # float
# Turnover minus the cost of sales. Gross profit doesn't include
# administrative, financial, or distribution costs.

GROSS_PROFIT_DELTA_PERCENTAGE = "gross_profit_delta_percentage"  # string
# Movement in gross profit from previous year’s filing to latest filing.

TURNOVER = "turnover"  # string
# The income a company Receives from normal business activities.
# Internationally known as "revenue".

TURNOVER_DELTA_PERCENTAGE = "turnover_delta_percentage"  # string
# Movement in turnover from previous year’s filing to latest filing.

COST_OF_SALES = "cost_of_sales"  # string
# Costs attributable to the production of the goods or supply of services.

COST_OF_SALES_DELTA_PERCENTAGE = "cost_of_sales_delta_percentage"  # string
# Movement in cost of sales from previous year’s filing to latest filing.

DEPRECIATION = "depreciation"  # string
# A decrease in the value of company assets. Depreciation indicates how
# much of an asset's value has been used up.

DEPRECIATION_DELTA_PERCENTAGE = "depreciation_delta_percentage"  # string
# Movement in depreciation from previous year’s filing to latest filing.

TAXATION = "taxation"  # string
# Amount set aside for taxation purposes.

CASH = "cash"  # string
# Included in current assets, cash refers to the amount held in current or
# deposit bank accounts, and is seen as a highly liquid form of current
# asset.

CASH_DELTA_PERCENTAGE = "cash_delta_percentage"  # string
# Movement in cash from previous year’s filing to latest filing.

NET_WORTH = "net_worth"  # string
# The amount by which assets exceed liabilities. Net worth is a concept
# applicable to businesses as a measure of how much an entity is worth.

NET_WORTH_DELTA_PERCENTAGE = "net_worth_delta_percentage"  # string
# Movement in net worth from previous year’s filing to latest filing.

TOTAL_ASSETS = "total_assets"  # string
# The sum of current and long-term assets owned by the company.

TOTAL_ASSETS_DELTA_PERCENTAGE = "total_assets_delta_percentage"  # string
# The change in the total assets value from previous year’s filing to
# latest filing.

CURRENT_ASSETS = "current_assets"  # string
# All assets belonging to a company that can be converted easily into cash
# and are expected to be used (sold or consumed) within a year.

CURRENT_ASSETS_DELTA_PERCENTAGE = "current_assets_delta_percentage"  # string
# The change in the current assets value from the previous year’s filing
# to latest filing.

NET_ASSETS = "net_assets"  # string
# Net assets refers to the value of a company's assets minus its liabilities.

NET_ASSETS_DELTA_PERCENTAGE = "net_assets_delta_percentage"  # string
# Percentage change between the latest filing's value and previous
# filing's value of net assets.

TOTAL_LIABILITIES = "total_liabilities"  # string
# The total of all debts for which a company is liable; includes
# short-term and long-term liabilities.

# string
TOTAL_LIABILITIES_DELTA_PERCENTAGE = "total_liabilities_delta_percentage"
# The change in the value of total liabilities from previous year’s filing
# to latest filing.

DIRECTOR_RANGE_FILTERS = [
    AGE,
    DATA_OF_BIRTH,
    GROSS_PROFIT,
    GROSS_PROFIT_DELTA_PERCENTAGE,
    TURNOVER,
    TURNOVER_DELTA_PERCENTAGE,
    COST_OF_SALES,
    COST_OF_SALES_DELTA_PERCENTAGE,
    DEPRECIATION,
    DEPRECIATION_DELTA_PERCENTAGE,
    TAXATION,
    CASH,
    CASH_DELTA_PERCENTAGE,
    NET_WORTH,
    NET_WORTH_DELTA_PERCENTAGE,
    TOTAL_ASSETS,
    TOTAL_ASSETS_DELTA_PERCENTAGE,
    CURRENT_ASSETS,
    CURRENT_ASSETS_DELTA_PERCENTAGE,
    NET_ASSETS,
    NET_ASSETS_DELTA_PERCENTAGE,
    TOTAL_LIABILITIES,
    TOTAL_LIABILITIES_DELTA_PERCENTAGE,
]
