
from ...resources import Resource


class DirectorSearchResult(Resource):
    attribute_names = [
        'name',
        'locale',
        'date_of_birth',
        'director_url',
        'directorships_url',
        'companies_url',
    ]
