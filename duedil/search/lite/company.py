

from ...resources import Resource


class CompanySearchResult(Resource):
    attribute_names = [
        'locale'
        'name'
        'name_formatted'
        'link'
    ]

    def __init__(self, client, company_number=None, **kwargs):
        super(CompanySearchResult, self).__init__(client, id=company_number, **kwargs)
