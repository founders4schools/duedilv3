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

import unittest

from .v3pro import Client, Company #, Director
from .v3pro import COMPANY_TERM_FILTERS, COMPANY_RANGE_FILTERS

try:
    from .secrets import PRO_API_KEY as API_KEY
    SANDBOX = False
except ImportError:
    API_KEY = 'x425dum7jp2jxuz7e3ktaqmx'
    SANDBOX = True


class ClientTestCase(unittest.TestCase):

    def test_url(self):
        client = Client('abcdef')
        self.assertEqual(client.url, 'http://duedil.io/v3')
        client = Client('abcdef', True)
        self.assertEqual(client.url, 'http://duedil.io/v3/sandbox')
        client = Client('abcdef', False)
        self.assertEqual(client.url, 'http://duedil.io/v3')

    def test_key(self):
        client = Client('abcdef')
        self.assertEqual(client.api_key, 'abcdef')


class SearchCompaniesTestCase(unittest.TestCase):

    client = Client(API_KEY, SANDBOX)

    def test_kwargs(self):
        # you have to search for something
        with self.assertRaises(AssertionError):
            self.client.search_company()
        # search terms are strings
        with self.assertRaises(AssertionError):
            self.client.search_company(bla=2)
        # search ranges have a upper and lower
        # numerical value
        with self.assertRaises(AssertionError):
            self.client.search_company(name=1)
        with self.assertRaises(AssertionError):
            self.client.search_company(employee_count=1)
        with self.assertRaises(AssertionError):
            self.client.search_company(employee_count=[1,2,3])
        with self.assertRaises(AssertionError):
            self.client.search_company(employee_count=[2,'100'])
        # and this one must pass:
        self.client.search_company(name='ex')

    def test_order_by(self):
        with self.assertRaises(AssertionError):
            self.client.search_company(name='ex', order_by='None')
        #hmm does not seem to work on sandbox
        #self.client.search_company(order_by={'field': 'turnover', 'direction':'desc'},
        #    name='ex')

    def test_limit(self):
        with self.assertRaises(AssertionError):
            self.client.search_company(name='ex', limit='0')
        self.client.search_company(name='ex', limit=1)

    def test_offset(self):
        with self.assertRaises(AssertionError):
            self.client.search_company(name='ex', offset='0')
        self.client.search_company(name='ex', offset=0)

    def test_results(self):
        companies, raw = self.client.search_company(name='ex')
        self.assertIsInstance(companies[0], Company)
        self.assertIsInstance(raw, dict)

class SearchDirectorsTestCase(unittest.TestCase):

    client = Client(API_KEY, SANDBOX)



class CompanyTestCase(unittest.TestCase):

    if SANDBOX:
        company_id = '325401bd2f2ea29373c533eb1587e5fcab36f13b'
    else:
        company_id = '06999618'

    def test_get(self):
        company = Company(API_KEY, self.company_id, 'uk', SANDBOX)
        self.assertEqual(len(company.__dict__), 5)
        company.get()
        self.assertEqual(len(company.__dict__), 130)

    def test_init(self):
        company = Company(API_KEY, self.company_id, 'uk', SANDBOX, name='DUEDIL LIMITED')
        self.assertEqual(company.name, 'DUEDIL LIMITED')
        self.assertEqual(company.id, self.company_id)
        self.assertEqual(company.locale, 'uk')

    def test_lazy_load(self):
        company = Company(API_KEY, self.company_id, 'uk', SANDBOX)
        self.assertEqual(len(company.__dict__), 5)
        self.assertNotEqual(company.name, 0)
        self.assertEqual(len(company.__dict__), 130)

class DirectorTestCase(unittest.TestCase):

    pass


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ClientTestCase))
    suite.addTest(unittest.makeSuite(SearchCompaniesTestCase))
    suite.addTest(unittest.makeSuite(SearchDirectorsTestCase))
    suite.addTest(unittest.makeSuite(CompanyTestCase))
    suite.addTest(unittest.makeSuite(DirectorTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
