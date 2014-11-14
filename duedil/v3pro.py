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

from .apiconst import (COMPANY_ALLOWED_ATTRIBUTES, COMPANY_RANGE_FILTERS,
                       COMPANY_TERM_FILTERS, DIRECTOR_ALLOWED_ATTRIBUTES,
                       DIRECTOR_RANGE_FILTERS, DIRECTOR_TERM_FILTERS,
                       DIRECTORSHIPS_ALLOWED_ATTRIBUTES,
                       REGISTERED_ADDRESS_ALLOWED_ATTRIBUTES,
                       SERVICE_ADDRESS_ALLOWED_ATTRIBUTES)

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

    _allowed_attributes = SERVICE_ADDRESS_ALLOWED_ATTRIBUTES


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
    _allowed_attributes = REGISTERED_ADDRESS_ALLOWED_ATTRIBUTES

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
    _allowed_attributes = DIRECTORSHIPS_ALLOWED_ATTRIBUTES

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

    _name = 'director'
    _service_addresses = None
    _companies = None
    _directorships = None

    _allowed_attributes = DIRECTOR_ALLOWED_ATTRIBUTES

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
    _allowed_attributes = COMPANY_ALLOWED_ATTRIBUTES

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
