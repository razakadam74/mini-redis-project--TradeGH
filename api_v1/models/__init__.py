from flask_restplus import fields
from .. import api

# This namespace is the start of the path i.e., /strings
string_namespace = api.namespace('strings', description='Strings operations')

# Define the model so that the docs reflect what can be sent
string_model = api.model('String', {
    'key': fields.String(readOnly=True,
                         description='The unique id assigned internally by service'),
    'value': fields.String(required=True,
                          description='The string')
})

