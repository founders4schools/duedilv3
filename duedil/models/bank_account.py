from __future__ import unicode_literals

from ..resources import Resource


class BankAccount(Resource):
    attribute_names = [
        'bank',
        # string Name of bank
        'sortCode',
        # string Bank sort code
        'count',
        # integer Number of accounts
        'id',
        # string Identifier for bank account
    ]
