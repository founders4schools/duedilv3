from __future__ import unicode_literals

from ..resources import Resource


class PreviousCompanyName(Resource):
    attribute_names = [
        'id',
        # string The registered ID of the company
        'last_update',
        # dateTime Date of last update
        'name',
        # string The previous company name
        'endedDate',
        # string The date this company stopped using this name
    ]
