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

import os

import requests
from requests.exceptions import HTTPError

API_PRO_URL = 'http://duedil.io/v3'
API_LITE_URL = 'http://api.duedil.com/open'
API_INTERNATIONAL_URL = 'http://api.duedil.com/international'

API_KEY = os.environ.get('DUEDIL_API_KEY', None)


class Client(object):
    cache = None
    base_url = None

    def __init__(self, api_key, cache=None, api_type='pro', sandbox=False):
        self.api_key = api_key
        self.cache = cache
        self.sandbox = sandbox
        self.set_api(api_type)

    def set_api(self, api_type, api_key=None):
        if api_type not in ('pro', 'lite', 'international'):
            raise ValueError(
                'Duedil API must be "pro", "lite", and "international"')

        if api_type == 'pro':
            self.base_url = API_PRO_URL
        elif api_type == 'lite':
            self.base_url = API_LITE_URL
        elif api_type == 'international':
            self.base_url = API_INTERNATIONAL_URL

        if self.sandbox:
            self.base_url = self.base_url + '/sandbox'

        if api_key:
            self.api_key = api_key

    def get(self, endpoint, data=None):

        if not self.api_key:
            raise ValueError("Please provide a valid Duedil API key")

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
                                           url_params=params)
            except HTTPError:
                if response.status_code == 404:
                    pass
                else:
                    raise

        return result

api_client = Client(API_KEY)
