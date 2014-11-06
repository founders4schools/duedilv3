# -*- coding: utf-8 -*-
#
#  DuedilApiClient v3 Pro
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

import json
import urllib, urllib2

try:
    long
except NameError:
    # Python 3
    long = int

try:
    unicode
except NameError:
    # Python 3
    basestring = unicode = str

# Here are all the terms available in the companies filters parameter.

LOCALE = "locale" # string
# This terms accepts only the values uk or roi.

LOCATION = "location" # string
# This term accepts the name of a city and/or the address.

POSTCODE = "postcode" # string
# This term accepts a valid uk postcode.

SIC_CODE = "sic_code" # integer
# sic_code. This term accepts only the standard SIC 03 code

SIC_2007_CODE = "sic_2007_code" # integer
# sic_2007_code. This term accepts only the standard SIC 07 code

STATUS = "status" # string
# This term accepts only active, dissolved, in receivership or liquidation queries.

CURRENCY = "currency" # float
# This term accepts only the value eur or gbp

KEYWORDS = "keywords" # string
# Search keywords

NAME = "name" # string
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

EMPLOYEE_COUNT = "employee_count" # string
# Number of people employed by the company. NB: employee numbers not available for all companies. As such when searching for employee numbers, only companies with this data available will be searched.

TURNOVER = "turnover" # string
# The income a company receives from normal business activities. Internationally known as "revenue".

TURNOVER_DELTA_PERCENTAGE = "turnover_delta_percentage" # string
# Movement in turnover from previous year’s filing to latest filing.

GROSS_PROFIT = "gross_profit" # string
# Turnover minus the cost of sales. Gross profit doesn't include administrative, financial, or distribution costs.

GROSS_PROFIT_DELTA_PERCENTAGE = "gross_profit_delta_percentage" # string
# Movement in gross profit from previous year’s filing to latest filing.

COST_OF_SALES = "cost_of_sales" # string
# Costs attributable to the production of the goods or supply of services.

COST_OF_SALES_DELTA_PERCENTAGE = "cost_of_sales_delta_percentage" # string
# Movement in cost of sales from previous year’s filing to latest filing.

NET_ASSETS = "net_assets" # string
# Net assets refers to the value of a company's assets minus its liabilities.

NET_ASSETS_DELTA_PERCENTAGE = "net_assets_delta_percentage" # string
# percentage change between the latest filing's value and previous filing's value of net assets.

CURRENT_ASSETS = "current_assets" # string
# All assets belonging to a company that can be converted easily into cash and are expected to be used (sold or consumed) within a year.

CURRENT_ASSETS_DELTA_PERCENTAGE = "current_assets_delta_percentage" # string
# The change in the current assets value from the previous year’s filing to latest filing.

TOTAL_ASSETS = "total_assets" # string
# The sum of current and long-term assets owned by the company.

TOTAL_ASSETS_DELTA_PERCENTAGE = "total_assets_delta_percentage" # string
# The change in the total assets value from previous year’s filing to latest filing.

CASH = "cash" # string
# Included in current assets, cash refers to the amount held in current or deposit bank accounts, and is seen as a highly liquid form of current asset.

CASH_DELTA_PERCENTAGE = "cash_delta_percentage" # string
# Movement in cash from previous year’s filing to latest filing.

TOTAL_LIABILITIES = "total_liabilities" # string
# The total of all debts for which a company is liable; includes short-term and long-term liabilities.

TOTAL_LIABILITIES_DELTA_PERCENTAGE = "total_liabilities_delta_percentage" # string
# The change in the value of total liabilities from previous year’s filing to latest filing.

NET_WORTH = "net_worth" # string
# The amount by which assets exceed liabilities. Net worth is a concept applicable to businesses as a measure of how much an entity is worth.

NET_WORTH_DELTA_PERCENTAGE = "net_worth_delta_percentage" # string
# Movement in net worth from previous year’s filing to latest filing.

DEPRECIATION = "depreciation" # string
# A decrease in the value of company assets. Depreciation indicates how much of an asset's value has been used up.

DEPRECIATION_DELTA_PERCENTAGE = "depreciation_delta_percentage" # string
# Movement in depreciation from previous year’s filing to latest filing.

TAXATION = "taxation" # string
# Amount set aside for taxation purposes.

RETAINED_PROFITS = "retained_profits" # string
# Profit kept in the company rather than paid out to shareholders as a dividend.

PROFIT_RATIO = "profit_ratio" # string
# The profit ratio measures the amount of profit generated by each £1 of sales. Calculated as net profit / turnover.

INVENTORY_TURNOVER_RATIO = "inventory_turnover_ratio" # string
# The number of times the stock is sold and replaced in a year (calculated as sales divided by stock).

NET_PROFITABILITY = "net_profitability" # string
# The amount of sales needed to generate £1 of net profit. Calculated as turnover / net profit.

RETURN_ON_CAPITAL_EMPLOYED = "return_on_capital_employed" # string
# The profit generated as a function of the capital invested in the business (calculated as net profit divided by capital employed).

CASH_TO_TOTAL_ASSETS_RATIO = "cash_to_total_assets_ratio" # string
# The percentage of the company's assets that are held as cash (calculated as cash divided by total assets).

GEARING = "gearing" # string
# The debt to equity ratio in the business (calculated as total long term liabilities divided by shareholder equity).

GROSS_MARGIN_RATIO = "gross_margin_ratio" # string
# The gross profitability generated by the business as a percentage of the turnover received before accounting for fixed costs and overheads (calculated as gross profit divided by turnover).

RETURN_ON_ASSETS_RATIO = "return_on_assets_ratio" # string
# The profit generated in a business as a function of the assets held (calculated as gross profit divided by total assets).

CURRENT_RATIO = "current_ratio" # string
# A measure of the company's short term solvency (calculated as current assets divided by current liabilities).

DEBT_TO_CAPITAL_RATIO = "debt_to_capital_ratio" # string
# A measure of the company's leverage (calculated as total liabilities divided by the total shareholder equity plus total liabilities).

CASH_TO_CURRENT_LIABILITIES_RATIO = "cash_to_current_liabilities_ratio" # string
# A measure of the company's ability to meet its short term obligations (calculated as cash divided by short term liabilities).

LIQUIDITY_RATIO = "liquidity_ratio" # string
# A measure of the company's ability to meet short term obligations by liquidating certain assets, excluding its stock (calculated as current assets less stock divided by current liabilities).

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


# This “Director search endpoint” is similar to the “Company search endpoint”, though with some different ranges and terms.

# Searching by financial range will return directors who have a directorship at a company fulfilling that range.

# NB: The location filter is not available for director search.


NAME = "name" # string
# This field must be a string that contains the director’s name.

GENDER = "gender" # string
# This term accepts only the value M or F

TITLE = "title" # string
# View all available titles.

NATIONALITY = "nationality" # string
# View all available nationalities.

SECRETARIAL = "secretarial" # boolean
# This is a boolean field; the values accepted are true or false

CORPORATE = "corporate" # boolean
# This is a boolean field; the values accepted are true or false

DISQUALIFIED = "disqualified" # string
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


AGE = "age" # string
# The age brackets of the director

DATA_OF_BIRTH = "data_of_birth" # dateTime
# The date of birth brackets of the director. The data must be in this format MM/DD/YYY

GROSS_PROFIT = "gross_profit" # float
# Turnover minus the cost of sales. Gross profit doesn't include administrative, financial, or distribution costs.

GROSS_PROFIT_DELTA_PERCENTAGE = "gross_profit_delta_percentage" # string
# Movement in gross profit from previous year’s filing to latest filing.

TURNOVER = "turnover" # string
# The income a company Receives from normal business activities. Internationally known as "revenue".

TURNOVER_DELTA_PERCENTAGE = "turnover_delta_percentage" # string
# Movement in turnover from previous year’s filing to latest filing.

COST_OF_SALES = "cost_of_sales" # string
# Costs attributable to the production of the goods or supply of services.

COST_OF_SALES_DELTA_PERCENTAGE = "cost_of_sales_delta_percentage" # string
# Movement in cost of sales from previous year’s filing to latest filing.

DEPRECIATION = "depreciation" # string
# A decrease in the value of company assets. Depreciation indicates how much of an asset's value has been used up.

DEPRECIATION_DELTA_PERCENTAGE = "depreciation_delta_percentage" # string
# Movement in depreciation from previous year’s filing to latest filing.

TAXATION = "taxation" # string
# Amount set aside for taxation purposes.

CASH = "cash" # string
# Included in current assets, cash refers to the amount held in current or deposit bank accounts, and is seen as a highly liquid form of current asset.

CASH_DELTA_PERCENTAGE = "cash_delta_percentage" # string
# Movement in cash from previous year’s filing to latest filing.

NET_WORTH = "net_worth" # string
# The amount by which assets exceed liabilities. Net worth is a concept applicable to businesses as a measure of how much an entity is worth.

NET_WORTH_DELTA_PERCENTAGE = "net_worth_delta_percentage" # string
# Movement in net worth from previous year’s filing to latest filing.

TOTAL_ASSETS = "total_assets" # string
# The sum of current and long-term assets owned by the company.

TOTAL_ASSETS_DELTA_PERCENTAGE = "total_assets_delta_percentage" # string
# The change in the total assets value from previous year’s filing to latest filing.

CURRENT_ASSETS = "current_assets" # string
# All assets belonging to a company that can be converted easily into cash and are expected to be used (sold or consumed) within a year.

CURRENT_ASSETS_DELTA_PERCENTAGE = "current_assets_delta_percentage" # string
# The change in the current assets value from the previous year’s filing to latest filing.

NET_ASSETS = "net_assets" # string
# Net assets refers to the value of a company's assets minus its liabilities.

NET_ASSETS_DELTA_PERCENTAGE = "net_assets_delta_percentage" # string
# Percentage change between the latest filing's value and previous filing's value of net assets.

TOTAL_LIABILITIES = "total_liabilities" # string
# The total of all debts for which a company is liable; includes short-term and long-term liabilities.

TOTAL_LIABILITIES_DELTA_PERCENTAGE = "total_liabilities_delta_percentage" # string
# The change in the value of total liabilities from previous year’s filing to latest filing.

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



class Company(object):

    allowed_attributes = [
        'trading_address_postcode',
        'directorships_closed_director',
        'sic_description',
        'sic2007code',
        'sic_codes_count',
        'accounts_retained_profit',
        'accounts_trade_creditors',
        'accounts_url',
        'company_type',
        'accounts_date',
        'accounts_liabilities_current',
        'reg_tps',
        'incorporation_date',
        'accounts_currency',
        'id',
        'latest_accounts_date',
        'accounts_paid_up_equity',
        'accounts_liabilities_total',
        'reg_address_postcode',
        'trading_address2',
        'trading_address3',
        'directorships_closed_secretary',
        'accounts_net_worth',
        'directorships_retired',
        'trading_address4',
        'last_update',
        'documents_url',
        'accounts_profit_after_tax',
        'directorships_closed',
        'accounts_audit_fees',
        'accounts_assets_net',
        'status',
        'credit_rating_latest_description',
        'description',
        'directors_url',
        'accounts_trade_debtors',
        'accounts_type',
        'accounts_filing_date',
        'accounts_pre_tax_profit',
        'directorships_retired_secretary',
        'accounts_turnover',
        'accounts_months',
        'trading_address1',
        'sic_code',
        'accounts_liabilities_misc_current',
        'name',
        'accounts_capital_employed',
        'reg_area_code',
        'latest_annual_return_date',
        'accounts_operating_profits',
        'accounts_assets_total_current',
        'reg_address4',
        'accounts_shareholder_funds',
        'directorships_url',
        'accounts_consolidated',
    ]



    def __init__(self, api_key, id, locale, sandbox=False, **kwargs):
        self.api_key = api_key
        self.id = id
        assert(locale in ['uk', 'roi'])
        self.locale = locale
        self.sandbox = sandbox
        if sandbox:
            self._url = 'http://duedil.io/v3/sandbox/%s/companies/%s' %(locale, id)
        else:
            self._url = 'http://duedil.io/v3/%s/companies/%s' %(locale, id)
        self._set_attributes(**kwargs)

    def _set_attributes(self, **kwargs):
        for k,v in kwargs.items():
            assert(k in self.allowed_attributes)
            self.__setattr__(k,v)

    def __getattribute__(self, name):
        try:
            return super( Company, self).__getattribute__(name)
        except AttributeError as e:
            if name in self.allowed_attributes:
                self.get()
            return super( Company, self).__getattribute__(name)

    def get(self, attr=None):
        if attr:
            pass
        else:
            data = {'api_key': self.api_key}
            result = json.load(urllib2.urlopen(self.url + '?' + urllib.urlencode(data)))
            assert(result['response'].pop('id') == self.id)
            self._set_attributes(**result['response'])
            return result


    @property
    def url(self):
        return self._url


    @property
    def registered_address(self):
        if self._registered_address:
            return self._registered_address
        else:
            self._registered_address = self._get('registered-address')

        '''
        previous-company-names
        industries
        shareholders
        bank-accounts
        accounts
        documents
        subsidiaries
        parent
        directors
        directorships
        mortgages
        service-addresses
        '''



class Client(object):

    last_company_response = {}
    last_director_response = {}

    def __init__(self, api_key, sandbox=False):
        self.api_key = api_key
        self.sandbox = sandbox
        if sandbox:
            self._url = 'http://duedil.io/v3/sandbox'
        else:
            self._url = 'http://duedil.io/v3'

    @property
    def url(self):
        return self._url

    def search_company(self, order_by=None, limit=None, offset=None, **kwargs):
        '''
        Conduct advanced searches across all companies registered in UK & Ireland.
        Apply any combination of 44 different filters

        The parameter filters supports two different types of queries:
            * the “range” type (ie, a numeric range) and
            * the “terms” type (for example, an individual company name).

        For the range filter, you have to pass an array;
        for the terms filter, you just pass a string.

        The range type is used when you want to limit the results to a particular range of results.

        You can order the results based on the ranges using the parameter orderBy.
        '''
        data = {'api_key': self.api_key}
        assert(kwargs)
        for arg in kwargs:
            assert(arg in COMPANY_TERM_FILTERS + COMPANY_RANGE_FILTERS)
            if arg in COMPANY_TERM_FILTERS:
                # this must be  a string
                assert(isinstance(kwargs[arg], basestring))
            elif arg in COMPANY_RANGE_FILTERS:
                # array of two numbers
                assert(isinstance(kwargs[arg], (list,tuple)))
                assert(len(kwargs[arg]) == 2)
                for v in kwargs[arg]:
                    assert(isinstance(v, (int, long, float)))
        data['filters'] = json.dumps(kwargs)
        if order_by:
            assert(isinstance(order_by, dict))
            assert('field' in order_by)
            assert(order_by['field'] in COMPANY_TERM_FILTERS + COMPANY_RANGE_FILTERS)
            if order_by.get('direction'):
                assert(order_by['direction'] in ['asc', 'desc'])
            data['orderBy'] = json.dumps(order_by)
        if limit:
            assert(isinstance(limit, int))
            data['limit'] = limit
        if offset:
            assert(isinstance(offset, int))
            data['offset'] = offset
        results = json.load(urllib2.urlopen('%s/companies?%s'
                %(self.url, urllib.urlencode(data))))
        self.last_company_response = results
        return results



    def search_director(self, **kwargs):
        '''
        This “Director search endpoint” is similar to the
        “Company search endpoint”, though with some different ranges and
        terms.

        Searching by financial range will return directors who have a
        directorship at a company fulfilling that range.

        NB: The location filter is not available for director search.
        '''







