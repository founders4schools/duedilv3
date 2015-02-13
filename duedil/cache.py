# -*- coding: utf-8 -*-
#
#  DuedilApiClient v3 Pro + Credit
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
#

import hashlib
import six

from collections import OrderedDict


class Cache(object):

    _raw_dict = {}

    def __init__(self, raw_dict={}):
        self._raw_dict = {}

    def _cache_key(self, key, url_params):
        cache_key = key
        if url_params:
            cache_key += six.text_type(OrderedDict(url_params))
        return hashlib.md5(six.b(key)).hexdigest()

    def get_url(self, url, url_params=None):
        cache_key = self._cache_key(url, url_params)
        return self._raw_dict.get(cache_key, None)

    def set_url(self, url, data, url_params=None):
        cache_key = self._cache_key(url, url_params)
        self._raw_dict[cache_key] = data
