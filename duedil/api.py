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

from __future__ import unicode_literals


from .apiconst import COMPANY_TERM_FILTERS, COMPANY_RANGE_FILTERS, DIRECTOR_TERM_FILTERS, DIRECTOR_RANGE_FILTERS
from .search.pro import CompanySearchResult as ProCompanySearchResult, DirectorSearchResult
from .search.lite import CompanySearchResult as LiteCompanySearchResult

import os
import json

import requests
from requests.exceptions import HTTPError

try:  # pragma: no cover
    long
except NameError:  # pragma: no cover
    # Python 3
    long = int

try:  # pragma: no cover
    unicode
except NameError:  # pragma: no cover
    # Python 3
    basestring = unicode = str

API_URLS = {
    'pro': 'http://duedil.io/v3',
    'lite': 'http://api.duedil.com/open',
    'international': 'http://api.duedil.com/international',
}
API_KEY = os.environ.get('DUEDIL_API_KEY', None)


class Client(object):
    cache = None
    base_url = None

    def __init__(self, api_key=None, sandbox=False, cache=None):
        'Initialise the Client with which API to connect to and what cache to use'
        self.cache = cache
        self.set_api(api_key, sandbox)

    def set_api(self, api_key, sandbox):

        if not api_key:
            raise ValueError("Please provide a valid Duedil API key")
        self.api_key = api_key

        # if api_type not in API_URLS.keys():
        #     raise ValueError('Duedil API type must be "{}"'.format('", "'.join(API_URLS.keys())))
        # self.api_type = api_type
        self.base_url = API_URLS.get(self.api_type, 'lite')

        # Are we in a sandbox?
        self.sandbox = sandbox
        if self.sandbox:
            self.base_url = self.base_url + '/sandbox'

    def get(self, endpoint, data=None):
        return self._get(endpoint, data)

    def _get(self, endpoint, data=None):
        'this should become the private interface to all reequests to the api'

        result = None
        resp_format = 'json'
        data = data or {}

        url = "{base_url}/{endpoint}.{format}"
        prepared_url = url.format(base_url=self.base_url,
                                  endpoint=endpoint,
                                  format=resp_format)

        if self.cache:
            result = self.cache.get_url(prepared_url, url_params=data)

        if not result:
            params = data.copy()
            params['api_key'] = self.api_key
            response = requests.get(prepared_url, params=params)
            try:
                if not response.raise_for_status():
                    result = response.json()
                    if self.cache:
                        self.cache.set_url(prepared_url, result,
                                           url_params=params)
            except HTTPError:
                if response.status_code == 404:
                    pass
                else:
                    raise
        return result

    def _search(self, endpoint, result_klass, *args, **kwargs):
        query_params = self._build_search_string(*args, **kwargs)
        results = self._get(endpoint, data=query_params)
        return [result_klass(self, **r) for r in results.get('response',{}).get('data', {})]

    def _build_search_string(self, *args, **kwargs):
        raise NotImplementedError

    def search(self, *args, **kwargs):
        raise NotImplementedError


class LiteClient(Client):
    api_type = 'lite'

    def _build_search_string(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        #  this will need to be alter in all likely hood to do some validation
        return self._search('search', LiteCompanySearchResult, *args, **kwargs)


class ProClient(Client):
    api_type = 'pro'

    def _build_search_string(self, term_filters, range_filters=None,
                             order_by=None, limit=None, offset=None,
                             **kwargs):
        data = {}
        for arg, value in kwargs.items():
            try:
                assert(arg in term_filters + range_filters), "Not a valid query parameter"
            except AssertionError:
                raise TypeError
            if arg in term_filters:
                # this must be  a string
                assert(isinstance(value, basestring))
            elif arg in range_filters:
                # array of two numbers
                assert(isinstance(value, (list, tuple)))
                assert(len(value) == 2)
                for v in value:
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
        return self._search('companies',
                            ProCompanySearchResult,
                            COMPANY_TERM_FILTERS,
                            COMPANY_RANGE_FILTERS,
                            order_by=order_by,
                            limit=limit,
                            offset=offset,
                            **kwargs)

    def search_director(self, order_by=None, limit=None, offset=None, **kwargs):
        '''
        This “Director search endpoint” is similar to the
        “Company search endpoint”, though with some different ranges and
        terms.

        Searching by financial range will return directors who have a
        directorship at a company fulfilling that range.

        NB: The location filter is not available for director search.
        '''
        return self._search('directors',
                            DirectorSearchResult,
                            DIRECTOR_TERM_FILTERS,
                            DIRECTOR_RANGE_FILTERS,
                            order_by=order_by,
                            limit=limit,
                            offset=offset,
                            **kwargs)


class InternationalClient(Client):
    api_type = 'international'

    def _build_search_string(self, *args, **kwargs):
        pass
