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

# import time
import unittest

import json

import requests_mock
from requests.exceptions import HTTPError

from duedil.api import LiteClient, ProClient, InternationalClient, Client
from duedil.cache import Cache
from duedil.resources.lite import Company as LiteCompany
from duedil.search.pro import CompanySearchResult, DirectorSearchResult

API_KEY = '12345'


class TestClient(Client):
    base_url = 'http://duedil.io/v3'


class ClientTestCase(unittest.TestCase):

    def test_no_api_type(self):
        with self.assertRaises(ValueError):
            Client(API_KEY, api_type=None)

    @requests_mock.mock()
    def test_get(self, m):

        client = TestClient(API_KEY)
        m.register_uri('GET',
                       ('http://duedil.io/v3/12345.json?api_key=' +
                        API_KEY),
                       json={'name': 'Duedil', 'id': '12345'})

        response = client.get('12345')

        self.assertEqual(response, {'name': 'Duedil', 'id': '12345'})

    @requests_mock.mock()
    def test_cached_get(self, m):
        cache = Cache()
        client = TestClient(API_KEY, cache=cache)
        url = 'http://duedil.io/v3/12345.json'
        m.register_uri('GET', (url + '?api_key=' + API_KEY),
                       json={'name': 'Duedil', 'id': '12345'})

        client.get('12345')

        self.assertEqual(cache.get_url(url),
                         {'name': 'Duedil', 'id': '12345'})

    @requests_mock.mock()
    def test_get_with_params(self, m):
        cache = Cache()
        client = TestClient(API_KEY, cache=cache)
        params = {'filters': {'name': 'Duedil Ltd'}}
        url = 'http://duedil.io/v3/12345.json'
        m.register_uri('GET', url, json={'name': 'Duedil', 'id': '12345'})

        client.get('12345', data=params)

        cached = cache.get_url('http://duedil.io/v3/12345.json',
                               url_params=params)
        self.assertEqual(cached, {'name': 'Duedil', 'id': '12345'})

    @requests_mock.mock()
    def test_404(self, m):
        client = TestClient(API_KEY)
        url = 'http://duedil.io/v3/12345.json'
        m.register_uri('GET', (url + '?api_key=' + API_KEY),
                       status_code=404, reason="Not Found")

        response = client.get('12345')
        self.assertIsNone(response)

    @requests_mock.mock()
    def test_other_http_error(self, m):
        client = TestClient(API_KEY)
        url = 'http://duedil.io/v3/12345.json'
        m.register_uri('GET', (url + '?api_key=' + API_KEY),
                       status_code=403, reason="Forbidden")

        with self.assertRaises(HTTPError):
            response = client.get('12345')
            self.assertIsNone(response)


class LiteClientTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_search(self, m):
        client = LiteClient(API_KEY)
        url = 'http://api.duedil.com/open/search'
        result = {
            'locale': 'uk',
            'url': 'http://api.duedil.com/open/uk/company/06999618',
            'company_number': '06999618',
            'name': 'Duedil Limited'
        }
        m.register_uri('GET', url,
                       json={'response': {'data': [result]}})

        companies = client.search('DueDil')
        for company in companies:
            self.assertIsInstance(company, LiteCompany)


class ProClientTestCase(unittest.TestCase):

    client = ProClient(API_KEY)

    def test_sandbox(self):
        self.assertEqual(self.client.base_url, 'http://duedil.io/v3')
        sandbox_client = ProClient(API_KEY, sandbox=True)
        self.assertEqual(sandbox_client.base_url,
                         'http://duedil.io/v3/sandbox')

    @requests_mock.mock()
    def test_search_company(self, m):
        result = {
            'locale': 'uk',
            'url': 'http://duedil.io/v3/uk/companies/06999618.json',
            'id': '06999618',
            'name': 'Duedil Limited'
        }
        url = 'http://duedil.io/v3/companies.json'
        m.register_uri('GET', url,
                       json={'response': {'data': [result]}})
        companies = self.client.search_company()
        self.assertEqual(len(companies), 1)
        self.assertIn('api_key=12345', m._adapter.last_request.query)
        for company in companies:
            self.assertIsInstance(company, CompanySearchResult)

    @requests_mock.mock()
    def test_search_director(self, m):
        result = {
            'url': 'http://duedil.io/v3/uk/directors/06999618',
            'id': '12345',
            'forename': 'John',
            'surname': 'Doe'
        }
        url = 'http://duedil.io/v3/directors.json'
        m.register_uri('GET', url,
                       json={'response': {'data': [result]}})
        directors = self.client.search_director()
        self.assertEqual(len(directors), 1)
        self.assertIn('api_key=12345', m._adapter.last_request.query)
        for director in directors:
            self.assertIsInstance(director, DirectorSearchResult)




class SearchQueryTestCase(unittest.TestCase):

    client = ProClient(API_KEY)
    url = 'http://duedil.io/v3/companies.json'

    @requests_mock.mock()
    def test_search_filter(self, m):
        m.register_uri('GET', self.url,
                       json={})
        self.client.search_company(name='DueDil')
        self.assertEqual(
            json.loads(m._adapter.last_request.qs['filters'][0]),
            {"name": "duedil"})

    @requests_mock.mock()
    def test_search_range(self, m):
        m.register_uri('GET', self.url,
                       json={})
        self.client.search_company(employee_count=(1, 100,))
        self.assertEqual(
            json.loads(m._adapter.last_request.qs['filters'][0]),
            {"employee_count": [1, 100]})

    @requests_mock.mock()
    def test_search_non_filter_or_range(self, m):
        m.register_uri('GET', self.url,
                       json={})
        with self.assertRaises(TypeError):
            self.client.search_company(non_filter="Not Implemented")

    @requests_mock.mock()
    def test_search_order(self, m):
        m.register_uri('GET', self.url,
                       json={})
        self.client.search_company(order_by={'field': 'name',
                                             'direction': 'asc'})
        self.assertEqual(
            json.loads(m._adapter.last_request.qs['orderby'][0]),
            {"direction": "asc", "field": "name"})

    @requests_mock.mock()
    def test_search_limit(self, m):
        m.register_uri('GET', self.url,
                       json={})
        self.client.search_company(limit=100)
        self.assertEqual(m._adapter.last_request.qs['limit'][0], '100')

    @requests_mock.mock()
    def test_search_offset(self, m):
        m.register_uri('GET', self.url,
                       json={})
        self.client.search_company(offset=50)
        self.assertEqual(m._adapter.last_request.qs['offset'][0], '50')


class I12ClientTestCase(unittest.TestCase):


    def test_sandbox(self):
        client = InternationalClient(API_KEY)
        self.assertEqual(client.base_url,
                         'http://api.duedil.com/international')
        sandbox_client = InternationalClient(API_KEY, sandbox=True)
        self.assertEqual(sandbox_client.base_url,
                         'http://api.duedil.com/international/sandbox')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ClientTestCase))
    suite.addTest(unittest.makeSuite(LiteClientTestCase))
    suite.addTest(unittest.makeSuite(ProClientTestCase))
    suite.addTest(unittest.makeSuite(I12ClientTestCase))
    suite.addTest(unittest.makeSuite(SearchQueryTestCase))
    return suite

if __name__ == '__main__':   # pragma: no cover
    unittest.main()
