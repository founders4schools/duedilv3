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
from .search.international import CompanySearchResult as InternationalCompanySearchResult

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

        try:
            self.base_url = API_URLS.get(self.api_type, 'lite')
        except AttributeError:
            raise ValueError('Duedil API type must be "{}"'.format('", "'.join(API_URLS.keys())))


        # Are we in a sandbox?
        self.sandbox = sandbox
        if self.sandbox:
            self.base_url = self.base_url + '/sandbox'

    def get(self, endpoint, data=None):
        return self._get(endpoint, data)

    def _get(self, endpoint, data=None):
        'this should become the private interface to all reequests to the api'

        result = None
        data = data or {}

        if self.api_type == "pro":
            data_format = 'json'
            resp_format = '.{}'.format(data_format)
        else:
            resp_format = ''



        url = "{base_url}/{endpoint}{format}"
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

    def search(self, query):
        raise NotImplementedError


class LiteClient(Client):
    api_type = 'lite'

    def _build_search_string(self, *args, **kwargs):


    def search(self, query):
        #  this will need to be alter in all likely hood to do some validation
        return self._search('search', LiteCompanySearchResult, query=query)


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
                raise TypeError('%s must be one of %s' % (arg, ', '.join(term_filters+range_filters)))
            if arg in term_filters:
                # this must be  a string
                try:
                    assert(isinstance(value, basestring))
                except AssertionError:
                    raise TypeError('%s must be string type' % arg)
            elif arg in range_filters:
                # array of two numbers
                try:
                    assert(isinstance(value, (list, tuple)))
                except AssertionError:
                    raise TypeError('%s must be an array' % arg)
                try:
                    assert(len(value) == 2)
                except AssertionError:
                    raise ValueError('Argument %s can only be an array of length 2' % arg)
                for v in value:
                    try:
                        assert(isinstance(v, (int, long, float)))
                    except AssertionError:
                        raise TypeError('Value of %s must be numeric' % arg)
        data['filters'] = json.dumps(kwargs)
        if order_by:
            try:
                assert(isinstance(order_by, dict))
            except:
                raise TypeError('order_by must be dictionary')
            try:
                assert('field' in order_by)
            except AssertionError:
                raise ValueError("'field' must be a key in the order_by dictionary")
            try:
                assert(order_by['field'] in term_filters + range_filters)
            except AssertionError:
                raise TypeError("order_by['field'] must be one of %s" % (', '.join(term_filters+range_filters)))
            if order_by.get('direction'):
                try:
                    assert(order_by['direction'] in ['asc', 'desc'])
                except AssertionError:
                    raise ValueError('The direction must either be "asc" or "desc"')
            data['orderBy'] = json.dumps(order_by)
        if limit:
            try:
                assert(isinstance(limit, int))
            except AssertionError:
                raise TypeError('limit must be an integer')
            data['limit'] = limit
        if offset:
            try:
                assert(isinstance(offset, int))
            except AssertionError:
                raise TypeError('offset must be an integer')
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

    def search(self, *args, **kwargs):
        try:
            endpoint = '{}/search'.format(arg[0])
        except IndexError:
            # more validation could be done at this point
            raise TypeError('First argument must be the ISO 3166 country code of a supported country')
        return self._search(endpoint, InternationalCompanySearchResult, *args, **kwargs)
