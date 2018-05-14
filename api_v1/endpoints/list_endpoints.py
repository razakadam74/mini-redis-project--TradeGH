from flask_restplus import Resource
from api_v1 import api, app
from werkzeug.exceptions import NotFound
from flask_api import status  # HTTP Status Codes
from api_v1.utils import check_content_type
from api_v1.models import list_namespace, list_model, list_model_append, list_model_pop
from api_v1.models.list_model import List


######################################################################
#  LISTS  WITH REDIS ENDPOINTS
######################################################################

######################################################################
#  PATH: /lists
######################################################################
@list_namespace.route('/', strict_slashes=False)
class ListCollection(Resource):
    """ Handles all interactions with collections of List """

    # ------------------------------------------------------------------
    # LIST ALL LISTS
    # ------------------------------------------------------------------
    @list_namespace.doc('list_list')
    @list_namespace.marshal_list_with(list_model)
    def get(self):
        """
        Return a list of all list of Strings
        This endpoint will return all the list of strings in the database
        """
        lists = List.all()
        results = [list.serialize() for list in lists]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW LIST
    # ------------------------------------------------------------------
    @list_namespace.doc('append_list_to_list<String>')
    @list_namespace.expect(list_model)
    @list_namespace.response(400, 'The posted data was not valid')
    @list_namespace.response(201, 'List created successfully')
    @list_namespace.marshal_with(list_model, code=201)
    def post(self):
        """
        Instantiate or overwrite a List identified by key with value value
        This endpoint will create a List based the data in the body that is posted
        """
        check_content_type('application/json')
        list = List()
        app.logger.info('Payload = %s', api.payload)
        list.deserialize(api.payload)
        list.save()
        app.logger.info('List with new key [%s] saved!', list.key)
        return list.serialize(), status.HTTP_201_CREATED


######################################################################
#  PATH: /lists/{key}
######################################################################
@list_namespace.route('/<string:key>')
@list_namespace.param('key', 'The List identifier')
class ListResource(Resource):
    """
    ListResource class

    Allows the manipulation of a single List
    GET /list{key} - Returns a List with the key
    PUT /list{key} - Update a List with the key
    DELETE /list{key} -  Deletes a List with the key
    """

    # ------------------------------------------------------------------
    # RETRIEVE A LIST
    # ------------------------------------------------------------------
    @list_namespace.doc('get_string')
    @list_namespace.response(404, 'List not found')
    @list_namespace.marshal_with(list_model)
    def get(self, key):
        """
        Return the List value identified by key
        This endpoint will return a List based on it's key
        """
        app.logger.info("Request to Retrieve a list with key [%s]", key)
        list = List.find(key)
        if not list:
            raise NotFound("List with key '{}' was not found.".format(key))
        return list.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING LIST
    # ------------------------------------------------------------------
    @list_namespace.doc('update_strings')
    @list_namespace.response(404, 'List not found')
    @list_namespace.response(400, 'The posted List data was not valid')
    @list_namespace.expect(list_model)
    @list_namespace.marshal_with(list_model)
    def put(self, key):
        """
        Update the List identified by key
        This endpoint will update a List based the body that is posted
        """
        app.logger.info('Request to Update a list with key [%s]', key)
        check_content_type('application/json')
        list = List.find(key)
        if not list:
            # api.abort(404, "List with key '{}' was not found.".format(key))
            raise NotFound('List with key [{}] was not found.'.format(key))
        # data = request.get_json()
        data = api.payload
        app.logger.info(data)
        list.deserialize(data)
        list.key = key
        list.save()
        return list.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A LIST
    # ------------------------------------------------------------------
    @list_namespace.doc('delete_strings')
    @list_namespace.response(204, 'List deleted')
    def delete(self, key):
        """
        Delete the List identified by key
        This endpoint will delete a List based the key specified in the path
        """
        app.logger.info('Request to Delete a list with key [%s]', key)
        list = List.find(key)
        if list:
            list.delete()
        return 'List deleted', status.HTTP_204_NO_CONTENT


@list_namespace.route('/append')
class ListExtraMethods(Resource):

    # ------------------------------------------------------------------
    # ADD A NEW STRING TO LIST
    # ------------------------------------------------------------------
    @list_namespace.doc('append a new string to list')
    @list_namespace.expect(list_model_append)
    @list_namespace.response(400, 'The posted data was not valid')
    @list_namespace.response(201, 'String added successfully')
    @list_namespace.marshal_with(list_model, code=201)
    def post(self):
        """
        Append a String value to the end of the List identified by key
        This endpoint will create a List based the data in the body that is posted
        """
        check_content_type('application/json')
        app.logger.info('Payload = %s', api.payload)
        list = List.append(api.payload)
        app.logger.info('List with new key [%s] saved!', list.key)
        return list.serialize(), status.HTTP_201_CREATED


@list_namespace.route('/pop')
class ListExtraMethods(Resource):
    # ------------------------------------------------------------------
    # POP LAST ITEM IN THE LIST
    # ------------------------------------------------------------------
    @list_namespace.doc('pop the last item in the list of string with key')
    @list_namespace.response(404, 'List not found')
    @list_namespace.response(400, 'The posted List data was not valid')
    @list_namespace.expect(list_model_pop)
    # @list_namespace.marshal_with(list_model_pop)
    def put(self):
        """
        Remove the last element in the List identified by key, and return that element.
        This endpoint will update a List based the body that is posted
        """
        check_content_type('application/json')
        app.logger.info('Payload = %s', api.payload)
        item = List.pop(api.payload)
        return item, status.HTTP_200_OK