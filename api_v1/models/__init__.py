from .models import StringDAO
from flask_restplus import fields
from .. import api


string_namespace = api.namespace('Strings', description='String operations')

string = api.model('String', {
    'id': fields.Integer(readOnly=True, description='The string unique identifier'),
    'string': fields.String(required=True, description='The string')
})


stringDAO = StringDAO()

