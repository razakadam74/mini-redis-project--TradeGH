from flask_restplus import fields
from api_v1 import api

######################################################################
#  NAMESPACES
######################################################################
string_namespace = api.namespace('string', description='Strings Operations')
list_namespace = api.namespace('list', description='List Operations')
map_namespace = api.namespace('map', description='Map Operations')

######################################################################
#  MODELS
######################################################################

#model for string endpoint operations
string_model = api.model('String', {
    'key': fields.String(readOnly=True, description='The unique id assigned to string'),
    'value': fields.String(required=True, description='The string value')
})

#model for general list endpoint operations
list_model = api.model('List', {
    'key': fields.String(readOnly=True, description='The unique id assigned to list'),
    'value': fields.List(required=True, cls_or_instance=fields.String, description='The List of strings')
})

#model for appending to list operation
list_model_append = api.model('ListAppend', {
    'key': fields.String(readOnly=True, description='The unique id assigned to list'),
    'value': fields.String(required=True, description='String to append')
})

#model for popping out of a list operation
list_model_pop = api.model('ListPop', {
    'key': fields.String(readOnly=True, description='The unique id assigned to list')
})

#model for value of a map(dict)
map_value_model = api.model('Map_value', {
    'key': fields.String(readOnly=True, description='The unique id assigned to map'),
    'value': fields.String(required=True, description='The string')
})

#model for map item of a map(dict)
map_item = api.model('Item', {
    'key': fields.String(readOnly=True, description='The unique id assigned to dict'),
    'value': fields.Nested(map_value_model, required=True, description='Map key and values')
})

#model for general Map of a map(dict)
map_model = api.model('Map_model', {
    'key': fields.String(readOnly=True, description='The unique id assigned to dict'),
    'value': fields.List(fields.Nested(map_item), required=True, description='Map item')
})

#model for getting a string value from a map
map_model_get = api.model('MapGet', {
    'key': fields.String(readOnly=True, description='The unique id assigned to map')
})


#model for SEARCH-KEYS query
search_model = api.model('SearchString', {
    'search_term' : fields.String(readOnly=True, description='The search term')
})