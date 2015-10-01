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

# import json

import requests_mock
# from requests.exceptions import HTTPError

from duedil.resources import Resource, ProResource, RelatedResourceMixin
from duedil.resources.pro.company import Company
from duedil.resources.lite import Company as LiteCompany

API_KEY = '12345'


class TestResource(Resource):
    pass

class TestEndpointResource(Resource):
    attribute_names = ['name', 'id', 'category']

class TestAttrResource(Resource):
    attribute_names = ['name', 'id', 'category']
    path = 'test'

class TestAttrProResource(ProResource):
    attribute_names = ['name', 'id', 'category']
    path = 'test'


class TestProResource(ProResource):
    attribute_names = ['name', 'id']
    path = "resources"


class TestRelatedResource(Resource):
    attribute_names = ['name']


class TestRelatedProResource(ProResource):
    attribute_names = ['name']


class TestRelatedListResource(Resource):
    attribute_names = ['name']


class TestHasRelatedResources(RelatedResourceMixin, ProResource):
    path = 'test'
    related_resources = {
        'test-related': TestRelatedResource,
        'test-related-list': TestRelatedListResource,
        'test-string': 'resources.pro.company.Company',
        'test-loadable': TestRelatedProResource,
    }
    attribute_names = ['name']


class ResourceTestCase(unittest.TestCase):

    def test_resource_no_allowed_attributes(self):
        with self.assertRaises(NotImplementedError):
            TestResource(api_key=API_KEY, rid=123)

    def test_bad_endpoint(self):
        with self.assertRaises(ValueError):
            TestEndpointResource(api_key=API_KEY, rid=12345).endpoint

    @requests_mock.mock()
    def test_load_resource(self, m):
        m.register_uri('GET', 'http://duedil.io/v3/uk/test/12345.json',
                       json={"response":{'name': 'Duedil', 'id': 12345, 'category': 'thing'}})
        res = TestAttrProResource(api_key=API_KEY, rid=12345, load=True)
        self.assertEqual(res.category, 'thing')

    @requests_mock.mock()
    def test_resource_set_attribute(self, m):
        m.register_uri('GET', 'http://api.duedil.com/open/uk/test/12345.json',
                       json={'response': {'name': 'Duedil', 'id': 12345, 'category': None}})
        res = TestAttrResource(api_key=API_KEY, rid=12345, name="Duedil")

        self.assertEqual(res.rid, 12345)
        self.assertEqual(res.name, 'Duedil')
        self.assertFalse(hasattr(res, 'category'))

        res._set_attributes(True, name="Limited")
        self.assertTrue(hasattr(res, 'category'))
        self.assertIsNone(res.category)


class ProResourceTestCase(unittest.TestCase):


    @requests_mock.mock()
    def test_load_on_get(self, m):
        m.register_uri('GET', 'http://duedil.io/v3/uk/resources/12345.json',
                       json={'response': {'name': 'Duedil', 'id': 12345}})

        res = TestProResource(api_key=API_KEY, rid=12345)
        name = res.name
        self.assertEqual(name, 'Duedil')
        with self.assertRaises(AttributeError):
            getattr(res, 'not_name')


class RelatedResourceTestCase(unittest.TestCase):

    @requests_mock.mock()
    def test_load_related(self, m):
        m.register_uri(
            'GET', 'http://duedil.io/v3/uk/test/12345/test-related.json',
            json={'response': {
                'name': 'Duedil',
                'id': '67890'
            }})
        res = TestHasRelatedResources(api_key=API_KEY, rid=12345)
        related = res.test_related
        self.assertIsInstance(related, TestRelatedResource)

    @requests_mock.mock()
    def test_load_related_string(self, m):
        m.register_uri(
            'GET', 'http://duedil.io/v3/uk/test/12345/test-string.json',
            json={'response': {
                'name': 'Duedil',
                'id': '67890'
            }})
        res = TestHasRelatedResources(api_key=API_KEY, rid=12345)
        related = res.test_string
        self.assertIsInstance(related, Company)

    @requests_mock.mock()
    def test_load_related_loadable(self, m):
        m.register_uri(
            'GET', 'http://duedil.io/v3/uk/test/12345/test-loadable.json',
            json={'response': {
                'name': 'Duedil',
                'id': '67890'
            }})
        res = TestHasRelatedResources(api_key=API_KEY, rid=12345)
        related = res.test_loadable
        self.assertIsInstance(related, TestRelatedProResource)
        self.assertIs(related.client.api_key, API_KEY)

    @requests_mock.mock()
    def test_load_related_list(self, m):
        m.register_uri(
            'GET',
            'http://duedil.io/v3/uk/test/12345/test-related-list.json',
            json={'response': {'data': [{
                'name': 'Duedil',
                'id': '67890'
            }]}})
        res = TestHasRelatedResources(api_key=API_KEY, rid=12345)
        related = res.test_related_list
        self.assertIsInstance(related[0], TestRelatedListResource)



class LiteCompanyTestCase(unittest.TestCase):

    def test_company_number(self):
        company = LiteCompany(api_key=API_KEY, company_number=12345)
        self.assertEqual(company.rid, 12345)

    @requests_mock.mock()
    def test_load_company_number(self, m):
        m.register_uri('GET', 'http://api.duedil.com/open/uk/company/12345.json',
                       json={'name': 'Duedil',
                             'company_number': "12345"})

        company = LiteCompany(api_key=API_KEY, company_number=12345)
        self.assertEqual(company.name, 'Duedil')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ResourceTestCase))
    return suite

if __name__ == '__main__':   # pragma: no cover
    unittest.main()
