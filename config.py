'''
This is the configuration file for the app
All settings and configuration variables are set here
'''
import os
# import warnings

# from flask.exthook import ExtDeprecationWarning

# #suppress depreciated errors
# warnings.simplefilter('ignore', ExtDeprecationWarning)


# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))



# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.urandom(100)


# Secret key for signing cookies
SECRET_KEY = os.urandom(100)

DEFAULT_RENDERERS = [
    'flask.ext.api.renderers.JSONRenderer',
    'flask.ext.api.renderers.BrowsableAPIRenderer',
]

#redis settings
REDIS_URL = "redis://:@localhost:6379/0"

# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379
# REDIS_DB = 0

#
# REDIS_PASSWORD = ''
# REDIS_SOCKET_TIMEOUT = ''
# REDIS_CONNECTION_POOL = ''
# REDIS_CHARSET = ''
# REDIS_ERRORS = ''
# REDIS_DECODE_RESPONSES = ''
# REDIS_UNIX_SOCKET_PATH = ''


##Swagger UI

SWAGGER_UI_JSONEDITOR = True

