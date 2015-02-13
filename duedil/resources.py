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

from __future__ import print_function, unicode_literals

import sys
import six

from .apiconst import (COMPANY_ALLOWED_ATTRIBUTES,
                       DIRECTOR_ALLOWED_ATTRIBUTES,
                       DIRECTORSHIPS_ALLOWED_ATTRIBUTES,
                       REGISTERED_ADDRESS_ALLOWED_ATTRIBUTES,
                       SERVICE_ADDRESS_ALLOWED_ATTRIBUTES)


class Resource(object):
    _allowed_attributes = None

    def __init__(self, *args, **kwargs):
        if not self._allowed_attributes:
            raise NotImplementedError(
                "Resources must include a list of allowed attributes")

    def _set_attributes(self, missing, **kwargs):
        for k, v in kwargs.items():
            if k not in self._allowed_attributes:
                print ("'%s'," % k)
            self.__setattr__(k, v)
        if missing:
            for allowed in self._allowed_attributes:
                if allowed not in kwargs:
                    self.__setattr__(allowed, None)


class LoadableResource(Resource):
    _endpoint = None

    def __init__(self, client, id=None, locale='uk',
                 **kwargs):
        self.id = id
        assert(locale in ['uk', 'roi'])
        self.locale = locale
        self.client = client
        self._set_attributes(missing=False, **kwargs)

    def __getattribute__(self, name):
        """
        lazily return attributes, only contact duedil if necessary
        """
        try:
            return super(LoadableResource, self).__getattribute__(name)
        except AttributeError:
            if name in self._allowed_attributes:
                self.load()
                return super(LoadableResource, self).__getattribute__(name)
            else:
                raise

    def _assign_attributes(self, data=None):
        assert(data['response'].get('id') == self.id)
        self._set_attributes(missing=True, **data['response'])

    def load(self):
        """
        get results from duedil
        """
        endpoint = self.endpoint
        if self.id:
            endpoint = endpoint.format(id=self.id)
        result = self.client.get(endpoint)
        self._assign_attributes(result)
        return result

    @property
    def endpoint(self):
        endpoint = self._endpoint
        if self.id:
            endpoint = endpoint.format(id=self.id)
        return endpoint


def resource_property(endpoint):
    def wrap(getter_fn):
        def inner(self, *args, **kwargs):
            return getter_fn(self, endpoint, *args, **kwargs)
        return inner
    return wrap


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
        return self.client.get(uri)

    def load_related(self, key, klass=None):
        internal_key = '_' + key.replace('-', '_')

        related = getattr(self, internal_key, None)

        if related is None:
            result = self._get(key)
            if result:
                response = result['response']
                if (
                    'data' in response and
                    isinstance(response['data'], (list, tuple))
                ):
                    related = []
                    for r in result['response']['data']:
                        r['locale'] = r.get('locale', self.locale)
                        related.append(
                            klass(self.client, **r) if klass else None
                        )
                    setattr(self, internal_key, related)
                elif result:
                    response['locale'] = response.get('locale', self.locale)
                    if klass:
                        related = klass(self.client, **response)
                    setattr(self, internal_key, related)
        return related


class ServiceAddress(Resource):
    _allowed_attributes = SERVICE_ADDRESS_ALLOWED_ATTRIBUTES


class RegisteredAddress(Resource):
    _allowed_attributes = REGISTERED_ADDRESS_ALLOWED_ATTRIBUTES


class DirectorShip(Resource):
    _allowed_attributes = DIRECTORSHIPS_ALLOWED_ATTRIBUTES


class Account(Resource):
    pass


class PreviousCompanyName(Resource):
    pass


class Industry(Resource):
    pass


class Shareholder(Resource):
    pass


class BankAccount(Resource):
    pass


class Mortgage(Resource):
    pass


class Document(Resource):
    pass


class Company(RelatedResourceMixin, LoadableResource):

    _endpoint = 'companies/{id}'
    _allowed_attributes = COMPANY_ALLOWED_ATTRIBUTES

    related_resources = {
        'service-addresses': ServiceAddress,
        'directors': 'Director',
        'parent': 'Company',
        'directors': 'Director',
        'directorships': DirectorShip,
        'accounts': Account,
        'previous-company-names': PreviousCompanyName,
        'industries': Industry,
        'shareholders': Shareholder,
        'bank-accounts': BankAccount,
        'mortgages': Mortgage,
        'subsidiaries': 'Company'
    }


class Director(LoadableResource):

    _endpoint = 'directors/{id}'

    _allowed_attributes = DIRECTOR_ALLOWED_ATTRIBUTES
    related_resources = {
        'companies': Company,
        'directorships': DirectorShip
    }


class LiteCompany(LoadableResource):
    _endpoint = "company/{id}"
    _allowed_attributes = [
        'duedil_url',
        # string the url of the full company profile on duedil.com
        'company_number',
        # string the company number
        'name',
        # string the company name
        'name_formated',
        # string a more readable version of the company name
        'registered_address',
        # obj Holds address information about the company
        # 'registered_address.string',
        # string Full registered address of the company, formatted as a
        # string.
        # 'registered_address.postcode',
        # string The postcode (if available) of the company
        # 'registered_address.full_address',
        # array array containing the individual address lines
        'category',
        # string The category of company eg "Public Limited Company"
        'status',
        # string a string describing the status of company eg "In
        # Liquidation"
        'locale',
        # string Either "United Kingdom" or "Republic of Ireland"
        'previous_names',
        # array a collection containing one or more previous name
        # objects
        # 'previous_names[].name',
        # string the raw previous name of the company
        # 'previous_names[].name_formatted',
        # string a more readable version of the previous name
        # 'previous_names[].ended_date',
        # string when the company ceased using this name [YYYY-MM-DD]
        'sic_codes',
        # array a collection containing one or more SIC code objects
        # 'sic_codes[].code',
        # string The SIC code
        # 'sic_codes[].description',
        # string Description of the SIC code
        # 'sic_codes[].type',
        # string Either "primary" or "secondary"
        'incorporation_date',
        # string when the company was incorporated. [YYYY-MM-DD]
        'accounts',
        # obj Information about the most recent accounts
        # 'accounts.accounts_date',
        # string Date of latest accounts. [YYYY-MM-DD]
        # 'accounts.type',
        # string The type of accounts filed. eg "Full"
        'returns',
        # obj information about the company's returns
        # 'returns.last_returns_date',
        # string Date of the last returns. [YYYY-MM-DD]
    ]

    def __init__(self, client, company_number=None, **kwargs):
        super(LiteCompany, self).__init__(client, id=company_number,
                                          **kwargs)

    def _assign_attributes(self, data=None):
        assert(data.get('company_number') == self.id)
        self._set_attributes(missing=True, **data)
