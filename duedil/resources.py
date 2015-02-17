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

import sys
import six
import json

from .api import api_client


class Resource(object):
    attribute_names = None
    locale = 'uk'
    id = None
    path = None

    def __init__(self, id=None, locale=None, load=False, **kwargs):
        if not self.attribute_names:
            raise NotImplementedError(
                "Resources must include a list of allowed attributes")

        self.id = id
        self.locale = locale if locale else None

        if load:
            self.load()

        if kwargs:
            self._set_attributes(**kwargs)

    def _set_attributes(self, missing=False, **kwargs):
        for k, v in kwargs.items():
            if k in self.attribute_names:
                self.__setattr__(k, v)

        if missing is True:
            for allowed in self.attribute_names:
                if allowed not in kwargs:
                    self.__setattr__(allowed, None)

    def load(self):
        result = api_client.get(self.endpoint)
        self._set_attributes(**result)

    @property
    def endpoint(self):
        if not self.path:
            raise ValueError(
                "{model} does not have a path to load specified".format(
                    model=self.__class__.__name__))
        endpoint = '{locale}/{path}'.format(locale=self.locale,
                                            path=self.path)
        if self.id:
            endpoint += '/{id}'.format(id=self.id)
        return endpoint


def resource_property(endpoint):
    def wrap(getter_fn):
        def inner(self, *args, **kwargs):
            return getter_fn(self, endpoint, *args, **kwargs)
        return inner
    return wrap


def _build_search_string(self, term_filters, range_filters,
                         order_by=None, limit=None, offset=None,
                         **kwargs):
    data = {}

    for arg in kwargs:
        if arg in term_filters:
            # this must be a string
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


class SearchableResourceMeta(type):
    term_filters = None
    range_filters = None
    search_path = None

    def search(klass, order_by=None, limit=None, offset=None, **kwargs):
        data = _build_search_string(klass.term_filters,
                                    klass.range_filters,
                                    order_by=order_by, limit=limit,
                                    offset=offset, **kwargs)
        results_raw = api_client.get(klass.search_path, data=data)
        results = []
        for r in results_raw['response']['data']:
            results.append(
                klass(**r)
            )
        return results


class RelatedResourceMeta(type):

    def __init__(klass, name, bases, ns):
        related_resources = ns.get('related_resources') or {}

        for ep in related_resources.keys():

            @resource_property(ep)
            def getter(self, endpoint):
                resource = self.related_resources[endpoint]

                if isinstance(resource, six.string_types):
                    resource = getattr(sys.modules[__name__], resource)

                return self.load_related(endpoint, resource)

            attr_name = ep.replace('-', '_')
            setattr(klass, attr_name,
                    property(getter, None, None, attr_name))


class RelatedResourceMixin(six.with_metaclass(RelatedResourceMeta, object)):
    related_resources = None

    def _get(self, resource):
        uri = '{endpoint}/{resource}'.format(endpoint=self.endpoint,
                                             resource=resource)
        return api_client.get(uri)

    def load_related(self, key, klass=None):
        internal_key = '_' + key.replace('-', '_')

        related = getattr(self, internal_key, None)

        if related is None:
            result = self._get(key)
            if result:
                response = result['response']
                related = None
                if (
                    'data' in response and
                    isinstance(response['data'], (list, tuple))
                ):
                    related = []
                    for r in result['response']['data']:
                        r['locale'] = r.get('locale', self.locale)
                        related.append(
                            klass(**r) if klass else None
                        )
                elif result:
                    response['locale'] = response.get('locale', self.locale)
                    if klass:
                        related = klass(**response)
                setattr(self, internal_key, related)
        return related
