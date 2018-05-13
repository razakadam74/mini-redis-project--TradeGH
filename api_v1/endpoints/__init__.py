from api_v1 import app, api
from api_v1.utils import DatabaseConnectionError, DataValidationError
from api_v1.models.str_model import String
from flask import make_response, jsonify
from flask_api import status  # HTTP Status Codes


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
# DELETE ALL STRING DATA (for testing only)
######################################################################
@app.route('/strings/reset', methods=['DELETE', 'GET'])
def strings_reset():
    """ Removes all string from the database """
    String.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)
