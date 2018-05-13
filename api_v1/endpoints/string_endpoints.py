from flask_restplus import Resource
from api_v1 import api, app
from werkzeug.exceptions import NotFound
from flask_api import status  # HTTP Status Codes
from api_v1.utils import check_content_type
from api_v1.models import string_namespace, string_model
from api_v1.models.str_model import String


######################################################################
#  STRINGS  WITH REDIS ENDPOINTS
######################################################################

######################################################################
#  PATH: /strings
######################################################################
@string_namespace.route('/', strict_slashes=False)
class StringCollection(Resource):
    """ Handles all interactions with collections of String """

    # ------------------------------------------------------------------
    # LIST ALL STRINGS
    # ------------------------------------------------------------------
    @string_namespace.doc('list_strings')
    @string_namespace.marshal_list_with(string_model)
    def get(self):
        """
        Return a list of all String values
        This endpoint will create a String based the data in the body that is posted
        """
        strings = String.all()
        results = [string.serialize() for string in strings]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW STRING
    # ------------------------------------------------------------------
    @string_namespace.doc('append_string_to_list')
    @string_namespace.expect(string_model)
    @string_namespace.response(400, 'The posted data was not valid')
    @string_namespace.response(201, 'String created successfully')
    @string_namespace.marshal_with(string_model, code=201)
    def post(self):
        """
        Instantiate or overwrite a String identified by key with value value
        This endpoint will create a String based the data in the body that is posted
        """
        check_content_type('application/json')
        string = String()
        app.logger.info('Payload = %s', api.payload)
        string.deserialize(api.payload)
        string.save()
        app.logger.info('String with new key [%s] saved!', string.key)
        # location_url = api.url_for(PetResource, key=string.key, _external=True)
        # return string.serialize(), status.HTTP_201_CREATED, {'Location': location_url}
        return string.serialize(), status.HTTP_201_CREATED


######################################################################
#  PATH: /strings/{key}
######################################################################
@string_namespace.route('/<string:key>')
@string_namespace.param('key', 'The String identifier')
class StringResource(Resource):
    """
    StringResource class

    Allows the manipulation of a single String
    GET /string{key} - Returns a String with the key
    PUT /string{key} - Update a String with the key
    DELETE /string{key} -  Deletes a String with the key
    """

    # ------------------------------------------------------------------
    # RETRIEVE A STRING
    # ------------------------------------------------------------------
    @string_namespace.doc('get_string')
    @string_namespace.response(404, 'String not found')
    @string_namespace.marshal_with(string_model)
    def get(self, key):
        """
        Return the String value identified by key
        This endpoint will return a String based on it's key
        """
        app.logger.info("Request to Retrieve a string with key [%s]", key)
        string = String.find(key)
        if not string:
            raise NotFound("String with key '{}' was not found.".format(key))
        return string.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING STRING
    # ------------------------------------------------------------------
    @string_namespace.doc('update_strings')
    @string_namespace.response(404, 'String not found')
    @string_namespace.response(400, 'The posted String data was not valid')
    @string_namespace.expect(string_model)
    @string_namespace.marshal_with(string_model)
    def put(self, key):
        """
        Update the value of the String identified by key
        This endpoint will update a String based the body that is posted
        """
        app.logger.info('Request to Update a string with key [%s]', key)
        check_content_type('application/json')
        string = String.find(key)
        if not string:
            # api.abort(404, "String with key '{}' was not found.".format(key))
            raise NotFound('String with key [{}] was not found.'.format(key))
        # data = request.get_json()
        data = api.payload
        app.logger.info(data)
        string.deserialize(data)
        string.key = key
        string.save()
        return string.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A STRING
    # ------------------------------------------------------------------
    @string_namespace.doc('delete_strings')
    @string_namespace.response(204, 'String deleted')
    def delete(self, key):
        """
        Delete the String identified by key
        This endpoint will delete a String based the key specified in the path
        """
        app.logger.info('Request to Delete a string with key [%s]', key)
        string = String.find(key)
        if string:
            string.delete()
        return 'String deleted', status.HTTP_204_NO_CONTENT



