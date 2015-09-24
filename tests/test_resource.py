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

from duedil.resources import Resource, LoadableResource, RelatedResourceMixin
from duedil.models import LiteCompany, Company
from duedil.api import Client

API_KEY = '12345'


class TestResource(Resource):
    pass


class TestAttrResource(Resource):
    attribute_names = ['name', 'id', 'category']


class TestLoadableResource(LoadableResource):
    attribute_names = ['name', 'id']
    _endpoint = "resources/{id}"


class TestRelatedResource(Resource):
    attribute_names = ['name']


class TestRelatedLoadableResource(LoadableResource):
    attribute_names = ['name']


class TestRelatedListResource(Resource):
    attribute_names = ['name']


class TestHasRelatedResources(RelatedResourceMixin, LoadableResource):
    _endpoint = 'test/{id}'
    related_resources = {
        'test-related': TestRelatedResource,
        'test-related-list': TestRelatedListResource,
        'test-string': 'Company',
        'test-loadable': TestRelatedLoadableResource,
    }
    attribute_names = ['name']


class TestClient(Client):
    base_url = 'http://duedil.io/v3'


class ResourceTestCase(unittest.TestCase):

    client = TestClient(API_KEY)

    def test_resource_no_allowed_attributes(self):
        with self.assertRaises(NotImplementedError):
            TestResource(self.client)

    def test_resource_set_attribute(self):
        res = TestAttrResource(self.client, name="Duedil")

        self.assertIsNone(res.id)
        self.assertEqual(res.name, 'Duedil')
        self.assertFalse(hasattr(res, 'category'))

        res._set_attributes(True, name="Limited")
        self.assertTrue(hasattr(res, 'category'))
        self.assertIsNone(res.category)


class LoadableResourceTestCase(unittest.TestCase):

    client = TestClient(API_KEY)

    @requests_mock.mock()
    def test_load_on_get(self, m):
        m.register_uri('GET', 'http://duedil.io/v3/resources/12345.json',
                       json={'response': {'name': 'Duedil', 'id': 12345}})

        res = TestLoadableResource(self.client, id=12345)
        name = res.name
        self.assertEqual(name, 'Duedil')
        with self.assertRaises(AttributeError):
            getattr(res, 'not_name')


class RelatedResourceTestCase(unittest.TestCase):

    client = TestClient(API_KEY)

    @requests_mock.mock()
    def test_load_related(self, m):
        m.register_uri(
            'GET', 'http://duedil.io/v3/test/12345/test-related.json',
            json={'response': {
                'name': 'Duedil'
            }})
        res = TestHasRelatedResources(self.client, id=12345)
        related = res.test_related
        self.assertIsInstance(related, TestRelatedResource)

    @requests_mock.mock()
    def test_load_related_string(self, m):
        m.register_uri(
            'GET', 'http://duedil.io/v3/test/12345/test-string.json',
            json={'response': {
                'name': 'Duedil'
            }})
        res = TestHasRelatedResources(self.client, id=12345)
        related = res.test_string
        self.assertIsInstance(related, Company)

    @requests_mock.mock()
    def test_load_related_loadable(self, m):
        m.register_uri(
            'GET', 'http://duedil.io/v3/test/12345/test-loadable.json',
            json={'response': {
                'name': 'Duedil'
            }})
        res = TestHasRelatedResources(self.client, id=12345)
        related = res.test_loadable
        self.assertIsInstance(related, TestRelatedLoadableResource)
        self.assertIs(related.client, self.client)

    @requests_mock.mock()
    def test_load_related_list(self, m):
        m.register_uri(
            'GET',
            'http://duedil.io/v3/test/12345/test-related-list.json',
            json={'response': {'data': [{
                'name': 'Duedil'
            }]}})
        res = TestHasRelatedResources(self.client, id=12345)
        related = res.test_related_list
        self.assertIsInstance(related[0], TestRelatedListResource)



class LiteCompanyTestCase(unittest.TestCase):

    client = TestClient(API_KEY, api_type='lite')

    def test_company_number(self):
        company = LiteCompany(self.client, company_number=12345)
        self.assertEqual(company.id, 12345)

    @requests_mock.mock()
    def test_load_company_number(self, m):
        m.register_uri('GET', 'http://api.duedil.com/open/uk/company/12345.json',
                       json={'name': 'Duedil',
                             'company_number': "12345"})

        company = LiteCompany(self.client, company_number=12345)
        self.assertEqual(company.name, 'Duedil')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ResourceTestCase))
    return suite

if __name__ == '__main__':   # pragma: no cover
    unittest.main()
