from flask import request, abort
from flask_api import status    # HTTP Status Codes

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 'Content-Type must be {}'.format(content_type))


######################################################################
# Custom Exceptions
######################################################################
class DataValidationError(ValueError):
    '''Error class for validating user input'''
    pass

class DatabaseConnectionError(ConnectionError):
    '''Error class for database connection'''
    pass

