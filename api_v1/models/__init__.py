from flask_restplus import fields
from api_v1 import api

######################################################################
#  NAMESPACES
######################################################################
string_namespace = api.namespace('strings', description='Strings operations')
list_namespace = api.namespace('list', description='List operations')

######################################################################
#  MODELS
######################################################################
string_model = api.model('String', {
    'key': fields.String(readOnly=True,
                         description='The unique id assigned to string'),
    'value': fields.String(required=True,
                           description='The string')
})

list_model = api.model('List', {
    'key': fields.String(readOnly=True, description='The unique id assigned to list'),
    'value': fields.List(required=True, cls_or_instance=fields.String, description='The List')
})
