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

# import unittest
#
# from duedil.cache import Cache
#
#
# class CacheTestCase(unittest.TestCase):
#     cache = Cache()
#
#     def test_get_cached(self):
#         url = 'http://duedil.io/v3/uk/companies/06999618'
#         data = {'name': 'Duedil Limited', 'company_number': '06999618'}
#
#         self.cache.set_url(url, data)
#
#         self.assertEqual(data, self.cache.get_url(url))
#
#     def test_get_uncached(self):
#         url = 'http://duedil.io/v3/uk/companies/07071234'
#
#         self.assertIsNone(self.cache.get_url(url))
#
#
# def test_suite():
#     suite = unittest.TestSuite()
#     suite.addTest(unittest.makeSuite(CacheTestCase))
#     return suite
#
# if __name__ == '__main__':
#     unittest.main()
