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

import json

import six

import requests
from requests.exceptions import HTTPError

from .apiconst import (COMPANY_RANGE_FILTERS, COMPANY_TERM_FILTERS,
                       DIRECTOR_RANGE_FILTERS, DIRECTOR_TERM_FILTERS)
from .resources import Company, Director, LiteCompany


class Client(object):
    cache = None
    base_url = None

    def __init__(self, api_key, cache=None, **kwargs):
        self.api_key = api_key
        self.cache = cache

        if not self.base_url:
            raise NotImplementedError("Implementors must provide a `base_url`")

    def get(self, endpoint, data=None):

        result = None

        data = data or {}

        url = "{base_url}/{endpoint}.json"
        prepared_url = url.format(base_url=self.base_url,
                                  endpoint=endpoint)

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
                                           url_params=data)
            except HTTPError:
                if response.status_code == 404:
                    pass
                else:
                    raise

        return result


class LiteClient(Client):
    base_url = 'http://api.duedil.com/open'

    def search(self, name):
        data = {'q': name}
        results = self.get('search', data=data)
        companies = []
        for r in results['response']['data']:
            r['locale'] = 'uk'
            companies.append(
                LiteCompany(self, cache=self.cache, **r)
            )
        return companies


class ProClient(Client):
    base_url = 'http://duedil.io/v3'

    last_company_response = {}
    last_director_response = {}

    def __init__(self, api_key, sandbox=False, locale='uk', **kwargs):
        super(ProClient, self).__init__(api_key, **kwargs)

        self.sandbox = sandbox
        if sandbox:
            self.base_url += '/sandbox'

        self.base_url += '/' + locale

    def _build_search_string(self, term_filters, range_filters,
                             order_by=None, limit=None, offset=None,
                             **kwargs):
        data = {}

        for arg in kwargs:
            if arg in term_filters:
                # this must be  a string
                assert(isinstance(kwargs[arg], six.string_types))
            elif arg in range_filters:
                # array of two numbers
                assert(isinstance(kwargs[arg], (list, tuple)))
                assert(len(kwargs[arg]) == 2)
                for v in kwargs[arg]:
                    assert(isinstance(v, (float, six.integer_types)))
            else:
                raise TypeError(
                    "{arg} is not available as a filter".format(arg=arg))

        if kwargs:
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
        companies = []
        data = self._build_search_string(COMPANY_TERM_FILTERS,
                                         COMPANY_RANGE_FILTERS,
                                         order_by=order_by, limit=limit,
                                         offset=offset, **kwargs)
        results = self.get('companies', data=data)
        if 'response' in results and 'data' in results['response']:
            self.last_company_response = results
            for r in results['response']['data']:
                companies.append(
                    Company(
                        self, **r)
                )
        return companies

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
        results = self.get('directors', data=data)
        directors = []
        for r in results['response']['data']:
            directors.append(
                Director(
                    self, **r)
            )
        return directors


# TODO
class I12Client(Client):
    base_url = 'http://api.duedil.com/international'

    def __init__(self, api_key, sandbox=False, **kwargs):
        super(I12Client, self).__init__(api_key, **kwargs)

        self.sandbox = sandbox
        if sandbox:
            self.base_url += '/sandbox'
