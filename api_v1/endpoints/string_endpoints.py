from flask_restplus import Resource
from api_v1 import api, app
from flask import make_response, jsonify
from werkzeug.exceptions import NotFound
from flask_api import status  # HTTP Status Codes
from api_v1.utils import check_content_type
from api_v1.utils import DatabaseConnectionError, DataValidationError
from api_v1.models import string_namespace, string_model
from api_v1.models.string_model import String


######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = error.message or str(error)
    app.logger.info(message)
    return {'status': 400, 'error': 'Bad Request', 'message': message}, 400


@api.errorhandler(DatabaseConnectionError)
def database_connection_error(error):
    """ Handles Database Errors from connection attempts """
    message = error.message or str(error)
    app.logger.critical(message)
    return {'status': 500, 'error': 'Server Error', 'message': message}, 500


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """ Let them know the server is healthy """
    return make_response(jsonify(status=200, message='Healthy'), status.HTTP_200_OK)


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
        strings = String.all()
        results = [string.serialize() for string in strings]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW STRING
    # ------------------------------------------------------------------
    @string_namespace.doc('create_string')
    @string_namespace.expect(string_model)
    @string_namespace.response(400, 'The posted data was not valid')
    @string_namespace.response(201, 'String created successfully')
    @string_namespace.marshal_with(string_model, code=201)
    def post(self):
        """
        Creates a String
        This endpoint will create a String based the data in the body that is posted
        """
        check_content_type('application/json')
        string = String()
        app.logger.info('Payload = %s', api.payload)
        string.deserialize(api.payload)
        string.save()
        app.logger.info('String with new id [%s] saved!', string.id)
        # location_url = api.url_for(PetResource, id=string.id, _external=True)
        # return string.serialize(), status.HTTP_201_CREATED, {'Location': location_url}
        return string.serialize(), status.HTTP_201_CREATED


######################################################################
#  PATH: /strings/{id}
######################################################################
@string_namespace.route('/<int:id>')
@string_namespace.param('id', 'The String identifier')
class StringResource(Resource):
    """
    PetResource class

    Allows the manipulation of a single String
    GET /string{id} - Returns a String with the id
    PUT /string{id} - Update a String with the id
    DELETE /string{id} -  Deletes a String with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A STRING
    # ------------------------------------------------------------------
    @string_namespace.doc('get_strings')
    @string_namespace.response(404, 'String not found')
    @string_namespace.marshal_with(string_model)
    def get(self, id):
        """
        Retrieve a single String
        This endpoint will return a String based on it's id
        """
        app.logger.info("Request to Retrieve a string with id [%s]", id)
        string = String.find(id)
        if not string:
            raise NotFound("String with id '{}' was not found.".format(id))
        return string.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING STRING
    # ------------------------------------------------------------------
    @string_namespace.doc('update_strings')
    @string_namespace.response(404, 'String not found')
    @string_namespace.response(400, 'The posted String data was not valid')
    @string_namespace.expect(string_model)
    @string_namespace.marshal_with(string_model)
    def put(self, id):
        """
        Update a String
        This endpoint will update a String based the body that is posted
        """
        app.logger.info('Request to Update a string with id [%s]', id)
        check_content_type('application/json')
        string = String.find(id)
        if not string:
            # api.abort(404, "String with id '{}' was not found.".format(id))
            raise NotFound('String with id [{}] was not found.'.format(id))
        # data = request.get_json()
        data = api.payload
        app.logger.info(data)
        string.deserialize(data)
        string.id = id
        string.save()
        return string.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A STRING
    # ------------------------------------------------------------------
    @string_namespace.doc('delete_strings')
    @string_namespace.response(204, 'String deleted')
    def delete(self, id):
        """
        Delete a String

        This endpoint will delete a String based the id specified in the path
        """
        app.logger.info('Request to Delete a string with id [%s]', id)
        string = String.find(id)
        if string:
            string.delete()
        return '', status.HTTP_204_NO_CONTENT


######################################################################
# DELETE ALL STRING DATA (for testing only)
######################################################################
@app.route('/strings/reset', methods=['DELETE'])
def strings_reset():
    """ Removes all string from the database """
    String.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)
