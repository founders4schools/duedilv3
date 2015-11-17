'Accounts'
from __future__ import unicode_literals

from .... import ProResource, RelatedResourceMixin
import six
import sys


class UnknownAccountTypeException(Exception):
    pass


# need to deal with pagination...
class Account(RelatedResourceMixin, ProResource):
    'Abstraction of Accounts resource in duedil v3 pro api'
    attribute_names = [
        'uri',
        'date',
        'type'
    ]
    account_classes = {
        'financial': 'pro.company.accounts.financial.AccountDetailsFinancial',
        'gaap': 'pro.company.accounts.gaap.AccountDetailsGAAP',
        'ifrs': 'pro.company.accounts.ifrs.AccountDetailsIFRS',
        'insurance': 'pro.company.accounts.insurance.AccountDetailsInsurance',
        'statutory': 'pro.company.accounts.statutory.AccountDetailsStatutory',
    }
    full_endpoint = True

    @property
    def path(self):
        return self.uri.split('/', 5)[-1].rsplit('/', 1)[0]

    @property
    def details(self):
        resource = self.account_classes[self.type]

        if isinstance(resource, six.string_types):
            module, resource = resource.rsplit('.', 1)
            resource = getattr(sys.modules['duedil.resources.%s' % module], resource)
        return self.load_related('details', resource, self.full_endpoint)
