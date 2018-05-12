from flask_restplus import Resource
from .models import string_namespace, string, stringDAO
from . import api
from . import redis_store

@string_namespace.route('/')
class StringList(Resource):
    '''Shows a list of all string, and lets you POST to add new strings'''
    @string_namespace.doc('list_strings')
    @string_namespace.marshal_list_with(string)
    def get(self):
        '''List all strings'''
        print('here ', redis_store.get('test'))
        return stringDAO.strings

    @string_namespace.doc('create_string')
    @string_namespace.expect(string)
    @string_namespace.marshal_with(string, code=201)
    def post(self):
        '''Create a new string'''
        return stringDAO.create(api.payload), 201


@string_namespace.route('/<int:id>')
@string_namespace.response(404, 'String not found')
@string_namespace.param('id', 'The string identifier')
class Todo(Resource):
    '''Show a single string item and lets you delete them'''
    @string_namespace.doc('get_string')
    @string_namespace.marshal_with(string)
    def get(self, id):
        '''Fetch a given string'''
        return stringDAO.get(id)

    @string_namespace.doc('delete_string')
    @string_namespace.response(204, 'String deleted')
    def delete(self, id):
        '''Delete a string given its identifier'''
        stringDAO.delete(id)
        return '', 204

    @string_namespace.expect(string)
    @string_namespace.marshal_with(string)
    def put(self, id):
        '''Update a string given its identifier'''
        return stringDAO.update(id, api.payload)


