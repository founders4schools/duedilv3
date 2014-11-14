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

from __future__ import print_function

import json

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    from urllib.parse import urlencode, urlsplit
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    from urllib import urlencode
    from urlparse import urlsplit

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


def locale_from_url(url):
    path = urlsplit(url).path.split('/')
    return [a for a in path if a in ['uk', 'roi']][0]


class _DueDilObj(object):

    def __init__(self, api_key, sandbox=False, **kwargs):
        self.api_key = api_key
        self.sandbox = sandbox
        self._set_attributes(missing=False, **kwargs)

    def _set_attributes(self, missing, **kwargs):
        for k, v in kwargs.items():
            if k not in self._allowed_attributes:
                print ("'%s'," % k)
            # assert(k in self._allowed_attributes)
            self.__setattr__(k, v)
        if missing:
            for allowed in self._allowed_attributes:
                if allowed not in kwargs:
                    self.__setattr__(allowed, None)


class ServiceAddress(_DueDilObj):

    _allowed_attributes = [
        # 'id',
        # string
        'last_update',
        # dateTime Date of last update
        'address1',
        # string Address part 1
        'address2',
        # string Address part 2
        'address3',
        # string Address part 3
        'address4',
        # string Address part 4
        'address5',
        # string Address part 5
        'postcode',
        # string Postcode
        'postal_area',
        # string Area code
    ]


class _EndPoint(_DueDilObj):

    def __init__(self, api_key, id, locale, sandbox=False, **kwargs):
        self.id = id
        assert(locale in ['uk', 'roi'])
        self.locale = locale
        super(_EndPoint, self).__init__(api_key, sandbox, **kwargs)

    def _get(self, endpoint):
        data = {'api_key': self.api_key}
        req = urlopen('%s/%s?%s'
                      % (self.url, endpoint, urlencode(data)))
        result = json.loads(req.read().decode('utf-8'))
        return result

    def __getattribute__(self, name):
        """
        lazily return attributes, only contact duedil if necessary
        """
        try:
            return super(_EndPoint, self).__getattribute__(name)
        except AttributeError:
            if name in self._allowed_attributes:
                self.get()
                return super(_EndPoint, self).__getattribute__(name)
            else:
                raise

    def get(self):
        """
        get results from duedil
        """
        data = {'api_key': self.api_key, 'nullValue': None}
        req = urlopen('%s?%s'
                      % (self.url, urlencode(data)))
        result = json.loads(req.read().decode('utf-8'))
        assert(result['response'].pop('id') == self.id)
        self._set_attributes(missing=True, **result['response'])
        return result

    @property
    def url(self):
        return self._url


class RegisteredAddress(_EndPoint):

    _name = 'registered-address'
    _allowed_attributes = [
        # 'id',
        # string The registered ID of the company
        'last_update',
        # dateTime Date of last update
        'company',
        # string Company registration number
        'address1',
        # string Address part 1
        'address2',
        # string Address part 2
        'address3',
        # string Address part 3
        'address4',
        # string Address part 4
        'postcode',
        # string Postcode
        'phone',
        # string phone number
        'tps',
        # string TPS
        'website',
        # string Website
        'po_box',
        # string PO box number
        'care_of',
        # string Care of
        'email',
        # string Email address
        'area_code',
        # string Area code
    ]

    def __init__(self, api_key, id, locale, sandbox=False, **kwargs):
        super(RegisteredAddress, self).__init__(api_key, id, locale, sandbox,
                                                **kwargs)
        if sandbox:
            url = 'http://duedil.io/v3/sandbox/%s/companies/%s/%s'
            self._url = url % (locale, id, self._name)
        else:
            url = 'http://duedil.io/v3/%s/companies/%s/%s'
            self._url = url % (locale, id, self._name)


class DirectorShip(_EndPoint):

    _name = 'directorships'
    _allowed_attributes = [
        'id',
        # string Director ID
        'last_update',
        # dateTime Date last updated
        'active',
        # boolean Active (true/false)
        'status',
        # string Status
        'founding',
        # boolean Founding director (true/false)
        'appointment_date',
        # dateTime Date appointed
        'function',
        # string Function
        'function_code',
        # integer Function code
        'position',
        # string Position
        'position_code',
        # string Position code
        'companies_url',
        # string Link to companies
        'directors_uri',
        # string Link to director profile
        'service_address_uri',
        # string Link to service address
        'address1',
        # string Address line 1
        'address2',
        # string Address line 2
        'address3',
        # string Address line 3
        'address4',
        # string Address line 4
        'address5',
        # string Address line 5
        'postal_area',
        # string Postal area
        'postcode',
        # string Postcode
        # undocumented:
        'owning_company',
        'resignation_date',
        'secretary',
    ]

    def __init__(self, api_key, id, locale, sandbox=False, **kwargs):
        super(DirectorShip, self).__init__(api_key, id, locale, sandbox,
                                           **kwargs)
        if sandbox:
            url = 'http://duedil.io/v3/sandbox/%s/directors/%s/%s'
            self._url = url % (locale, id, self._name)
        else:
            url = 'http://duedil.io/v3/%s/directors/%s/%s'
            self._url = url % (locale, id, self._name)


class Director(_EndPoint):

    _service_addresses = None
    _companies = None
    _directorships = None

    _allowed_attributes = [
        # 'id',
        # string Director ID
        'last_update',
        # dateTime Date last updated
        'open_directorships_count',
        # integer Number of open directorships
        'open_trading_directorships_count',
        # integer Number of open trading directorships
        'open_trading_director_directorships_count',
        # integer Of which a director
        'open_trading_secretary_directorships_count',
        # integer Of which a secretary
        'closed_directorships_count',
        # integer Number of closed directorships
        'retired_directorships_count',
        # integer Number of retired directorships
        'director_directorships_count',
        # integer Number of directorships (director)
        'open_director_directorships_count',
        # integer Number of open directorships (director)
        'closed_director_directorships_count',
        # integer Number of closed directorships (director)
        'secretary_directorships_count',
        # integer Number of secretary directorships
        'open_secretary_directorships_count',
        # integer Number of open secretary directorships
        'closed_secretary_directorships_count',
        # integer Number of closed secretary directorships
        'retired_secretary_directorships_count',
        # integer Number of retired decretary directorships
        'forename',
        # string Forename
        'surname',
        # string Surname
        'date_of_birth',
        # dateTime Date of Birth
        'directorships_url',
        # string Link to directorships
        'companies_url',
        # string Link to companies
        'director_url',
        # string Link to director profile
        # undocumented:
        'middle_name',
        'title',
        'postal_title',
        'nationality',
        'nation_code',
    ]

    def __init__(self, api_key, id, locale, sandbox=False, **kwargs):
        super(Director, self).__init__(api_key, id, locale, sandbox,
                                       **kwargs)
        if sandbox:
            self._url = 'http://duedil.io/v3/sandbox/%s/directors/%s' % (
                locale, id)
        else:
            self._url = 'http://duedil.io/v3/%s/directors/%s' % (locale, id)

    @property
    def service_addresses(self):
        if self._service_addresses:
            return self._service_addresses
        else:
            results = self._get('service-addresses')
            address_list = []
            for r in results['response']['data']:
                address_list.append(
                    ServiceAddress(self.api_key,
                                   sandbox=self.sandbox,
                                   **r)
                )
            self._service_addresses = address_list
        return self._service_addresses

    @property
    def companies(self):
        if self._companies:
            return self._companies
        else:
            results = self._get('companies')
            company_list = []
            for r in results['response']['data']:
                company_list.append(
                    Company(self.api_key, locale=self.locale,
                            sandbox=self.sandbox, **r)
                )
            self._companies = company_list
        return self._companies

    @property
    def directorships(self):
        if self._directorships:
            return self._directorships
        else:
            results = self._get('directorships')
            directorships_list = []
            for r in results['response']['data']:
                directorships_list.append(
                    DirectorShip(self.api_key, locale=self.locale,
                                 sandbox=self.sandbox, **r)
                )
            self._directorships = directorships_list
        return self._directorships


class Company(_EndPoint):

    _name = 'company'
    _service_addresses = None
    _directorships = None
    _directors = None
    _registered_address = None
    _allowed_attributes = [
        # this is filled by __init__ and must match this value 'id',
        # integer The registered company number (ID) of the company
        'last_update',
        # dateTime Date last updated
        'name',
        # string The registered company name
        'description',
        # string A description of the company filed with the registrar
        'status',
        # string The status of the company
        'incorporation_date',
        # dateTime The date the company was incorporated
        'latest_annual_return_date',
        # dateTime Date of most recent annual return
        'latest_accounts_date',
        # dateTime Date of most recent filed accounts
        'company_type',
        # string The company type
        'accounts_type',
        # string Type of accounts
        'sic_code',
        # integer Standard Industry Classification (SIC) code
        'previous_company_names_url',
        # string Link to previous company names
        'shareholdings_url',
        # string Link to shareholders information
        'accounts_account_status',
        # integer Accounts status
        'accounts_accounts_format',
        # integer Accounts format
        'accounts_assets_current',
        # integer Current assets
        'accounts_assets_intangible',
        # integer Intangible assets
        'accounts_assets_net',
        # integer Net assets
        'accounts_assets_other_current',
        # integer Other current assets
        'accounts_assets_tangible',
        # integer Tangible assets
        'accounts_url',
        # string Link to company accounts
        'accounts_assets_total_current',
        # integer Total current assets
        'accounts_assets_total_fix',
        # integer Total fixed assets
        'accounts_audit_fees',
        # integer Audit fees
        'accounts_bank_overdraft',
        # integer Bank overdraft
        'accounts_bank_overdraft_lt_loans',
        # integer Bank overdraft & long term loans
        'accounts_capital_employed',
        # integer Capital employed
        'accounts_cash',
        # integer Cash
        'accounts_consolidated',
        # boolean Accounts consolidated (Y/N)
        'accounts_cost_of_sales',
        # integer Cost of sales
        'accounts_currency',
        # string Accounts currency
        'accounts_date',
        # dateTime Accounts date
        'accounts_depreciation',
        # integer Depreciation
        'accounts_directors_emoluments',
        # integer Directors' emoluments
        'accounts_dividends_payable',
        # integer Dividends payable
        'accounts_gross_profit',
        # integer Gross profit
        'accounts_increase_in_cash',
        # integer Increase in cash
        'accounts_interest_payments',
        # integer Interest payments
        'accounts_liabilities_current',
        # integer Current liabilities
        'accounts_liabilities_lt',
        # integer Long term liabilities
        'accounts_liabilities_misc_current',
        # integer Miscellaneous current liabilities
        'accounts_liabilities_total',
        # integer Total liabilities
        'accounts_lt_loans',
        # integer Long term loans
        'accounts_months',
        # integer Months included in accounts
        'accounts_net_cashflow_before_financing',
        # integer Net cashflow before financing
        'accounts_net_cashflow_from_financing',
        # integer Net cashflow from financing
        'accounts_net_worth',
        # integer Net worth
        'accounts_no_of_employees',
        # integer Number of employees
        'accounts_operating_profits',
        # integer Operating profits
        'accounts_operations_net_cashflow',
        # integer Net cashflow
        'accounts_paid_up_equity',
        # integer Paid-up equity
        'accounts_pandl_account_reserve',
        # integer Account reserve
        'accounts_pre_tax_profit',
        # integer Pre-tax profit
        'accounts_profit_after_tax',
        # integer Profit after tax
        'accounts_retained_profit',
        # integer Retained profit
        'accounts_shareholder_funds',
        # integer Shareholder funds
        'accounts_short_term_loans',
        # integer Short term loans
        'accounts_stock',
        # integer Stock
        'accounts_sundry_reserves',
        # integer Sundry reserves
        'accounts_taxation',
        # integer Taxation
        'accounts_trade_creditors',
        # integer Trade creditors
        'accounts_turnover',
        # integer Turnover
        'accounts_wages',
        # integer Wages
        'accounts_working_capital',
        # integer Working capital
        'directors_url',
        # string Link to company directors
        'directorships_url',
        # string Link to directorships
        'directorships_open',
        # integer Number of open directorships
        'directorships_open_secretary',
        # integer Number of current directorships with Company Secretary status
        'directorships_open_director',
        # integer Number of current directorships with Director status
        'directorships_retired',
        # integer Number of retired directorships
        'directorships_retired_secretary',
        # integer Of which secretaries
        'directorships_retired_director',
        # integer Of which directors
        'subsidiaries_url',
        # string Link to company subsidiaries
        'documents_url',
        # string Link to original company documents
        'accounts_filing_date',
        # dateTime Accounts filing date
        'ftse_a',
        # integer FTSE listing category
        'mortgage_partial_outstanding_count',
        # integer Number of partially outstanding mortgages
        'mortgage_partial_property_satisfied_count',
        # integer Number of partially satified mortgages
        'mortgage_partial_property_count',
        # integer Number of partial mortgages
        'mortgages_url',
        # string Link to mortgages
        'mortgages_outstanding_count',
        # integer Number of outstanding mortgages
        'mortgages_satisfied_count',
        # integer Number of satisfied mortgages
        'reg_address1',
        # string Registered address street
        'reg_address2',
        # string Registered address town
        'reg_address3',
        # string Registered address county
        'reg_address4',
        # string Registered address country
        'reg_address_postcode',
        # string Registered address postcode
        'reg_area_code',
        # string Registered address area code
        'reg_phone',
        # string Registered phone number
        'reg_tps',
        # boolean Telephone Preference Service (TPS) notification (Y/N)
        'reg_web',
        # string Registered web address
        'sic2007code',
        # integer 2007 Standard Industry Classification (SIC) code
        'trading_address1',
        # string Trading address street
        'trading_address2',
        # string Trading address town
        'trading_address3',
        # string Trading address county
        'trading_address_postcode',
        # string Trading address postcode

        # in addition to the above values I found the following:
        'charity_number',
        'liquidation_status',
        'directorships_closed_director',
        'sic_description',
        'sic_codes_count',
        'trading_address4',
        'directorships_closed',
        'credit_rating_latest_description',
        'accounts_trade_debtors',
        'directorships_closed_secretary',
        'accounts_accountants',
        'accounts_auditors',
        'accounts_contingent_liability',
        'accounts_exports',
        'accounts_qualification_code',
        'accounts_revaluation_reserve',
        'accounts_solicitors',
        'bank_accounts_url',
        'next_annual_return_date',
        'preference_shareholdings_count',
        'preference_shares_issued',
        'reg_address_town',
        'reg_address_towncode',
        'reg_care_of',
        'reg_email',
        'trading_phone',
        'trading_phone_std',
        # from the search we also get:
        'company_url',
        'turnover',
        'turnover_delta_percentage',
    ]

    def __init__(self, api_key, id, locale, sandbox=False, **kwargs):
        super(Company, self).__init__(api_key, id, locale, sandbox,
                                      **kwargs)
        if sandbox:
            self._url = 'http://duedil.io/v3/sandbox/%s/companies/%s' % (
                locale, id)
        else:
            self._url = 'http://duedil.io/v3/%s/companies/%s' % (locale, id)

    @property
    def directors(self):
        if self._directors:
            return self._directors
        else:
            results = self._get('directors')
            director_list = []
            for r in results['response']['data']:
                director_list.append(
                    Director(self.api_key, locale=self.locale,
                             sandbox=self.sandbox, **r)
                )
            self._directors = director_list
        return self._directors

    @property
    def registered_address(self):
        if self._registered_address:
            return self._registered_address
        else:
            results = self._get('registered-address')
            address_data = results['response']
            self._registered_address = RegisteredAddress(self.api_key,
                                                         locale=self.locale,
                                                         sandbox=self.sandbox,
                                                         **address_data)
            return self._registered_address

    @property
    def service_addresses(self):
        if self._service_addresses:
            return self._service_addresses
        else:
            results = self._get('service-addresses')
            address_list = []
            for r in results['response']['data']:
                address_list.append(
                    ServiceAddress(self.api_key,
                                   sandbox=self.sandbox,
                                   **r)
                )
            self._service_addresses = address_list
        return self._service_addresses

    @property
    def directorships(self):
        if self._directorships:
            return self._directorships
        else:
            results = self._get('directorships')
            directorships_list = []
            for r in results['response']['data']:
                directorships_list.append(
                    DirectorShip(self.api_key, locale=self.locale,
                                 sandbox=self.sandbox, **r)
                )
            self._directorships = directorships_list
        return self._directorships

    '''
    previous-company-names
    industries
    shareholders
    bank-accounts
    accounts
    documents
    subsidiaries
    parent
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

    def _build_search_string(self, term_filters, range_filters,
                             order_by=None, limit=None, offset=None,
                             **kwargs):
        data = {'api_key': self.api_key}
        assert(kwargs)
        for arg in kwargs:
            assert(arg in term_filters + range_filters)
            if arg in term_filters:
                # this must be  a string
                assert(isinstance(kwargs[arg], basestring))
            elif arg in COMPANY_RANGE_FILTERS:
                # array of two numbers
                assert(isinstance(kwargs[arg], (list, tuple)))
                assert(len(kwargs[arg]) == 2)
                for v in kwargs[arg]:
                    assert(isinstance(v, (int, long, float)))
        data['filters'] = json.dumps(kwargs)
        if order_by:
            assert(isinstance(order_by, dict))
            assert('field' in order_by)
            assert(
                order_by['field'] in term_filters + range_filters)
            if order_by.get('direction'):
                assert(order_by['direction'] in ['asc', 'desc'])
            data['orderBy'] = json.dumps(order_by)
        if limit:
            assert(isinstance(limit, int))
            data['limit'] = limit
        if offset:
            assert(isinstance(offset, int))
            data['offset'] = offset
        return data

    def search_company(self, order_by=None, limit=None, offset=None, **kwargs):
        '''
        Conduct advanced searches across all companies registered in
        UK & Ireland.
        Apply any combination of 44 different filters

        The parameter filters supports two different types of queries:
            * the “range” type (ie, a numeric range) and
            * the “terms” type (for example, an individual company name).

        For the range filter, you have to pass an array;
        for the terms filter, you just pass a string.

        The range type is used when you want to limit the results to a
        particular range of results.

        You can order the results based on the ranges using the
        parameter orderBy.
        '''
        data = self._build_search_string(COMPANY_TERM_FILTERS,
                                         COMPANY_RANGE_FILTERS,
                                         order_by=order_by, limit=limit,
                                         offset=offset, **kwargs)
        req = urlopen('%s/companies?%s'
                      % (self.url, urlencode(data)))
        results = json.loads(req.read().decode('utf-8'))
        self.last_company_response = results
        companies = []
        for r in results['response']['data']:
            companies.append(
                Company(self.api_key, sandbox=self.sandbox, **r)
            )
        return companies, results

    def search_director(self, order_by=None, limit=None, offset=None,
                        **kwargs):
        '''
        This “Director search endpoint” is similar to the
        “Company search endpoint”, though with some different ranges and
        terms.

        Searching by financial range will return directors who have a
        directorship at a company fulfilling that range.

        NB: The location filter is not available for director search.
        '''
        data = self._build_search_string(DIRECTOR_TERM_FILTERS,
                                         DIRECTOR_RANGE_FILTERS,
                                         order_by=order_by, limit=limit,
                                         offset=offset, **kwargs)
        print ('%s/directors?%s' % (self.url, urlencode(data)))
        req = urlopen('%s/directors?%s'
                      % (self.url, urlencode(data)))
        results = json.loads(req.read().decode('utf-8'))
        directors = []
        for r in results['response']['data']:
            directors.append(
                Director(self.api_key, sandbox=self.sandbox, **r)
            )
        return directors, results
