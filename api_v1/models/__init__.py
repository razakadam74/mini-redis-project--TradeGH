from flask_restplus import fields
from api_v1 import api

######################################################################
#  NAMESPACES
######################################################################
string_namespace = api.namespace('string', description='Strings Operations')
list_namespace = api.namespace('list', description='List Operations')
map_namespace =api.namespace('map', description='Map Operations')

######################################################################
#  MODELS
######################################################################
string_model = api.model('String', {
    'key': fields.String(readOnly=True, description='The unique id assigned to string'),
    'value': fields.String(required=True, description='The string')
})

list_model = api.model('List', {
    'key': fields.String(readOnly=True, description='The unique id assigned to list'),
    'value': fields.List(required=True, cls_or_instance=fields.String, description='The List')
})

list_model_append = api.model('ListAppend', {
    'key': fields.String(readOnly=True, description='The unique id assigned to list'),
    'value': fields.String(required=True, description='String to append')
})

list_model_pop = api.model('ListPop', {
    'key': fields.String(readOnly=True, description='The unique id assigned to list')
})


map_item = api.model('Item', {
    'key': fields.String(readOnly=True, description='The unique id assigned to string'),
    'value': fields.String(required=True, description='The string')
})

map_model = api.model('String', {
    'key': fields.String(readOnly=True, description='The unique id assigned to dict'),
    'value': fields.Nested(map_item, required=True, description='The string')
})


map_model_get = api.model('MapGet', {
    'key': fields.String(readOnly=True, description='The unique id assigned to list')
})