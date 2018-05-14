from flask import Flask
from flask_restplus import Api
from werkzeug.contrib.fixers import ProxyFix
from flask_redis import FlaskRedis


#setting up flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

#loading configuration from config.py file
app.config.from_object('config')

#setting up redis extension database
redis_store = FlaskRedis(app)

#setting up restful plus api extension
api = Api(app, version='1.0', title='Mini Redis Server',
          description='A Mini Redis Server Take-Home Project specification for candidates for Engineering @ Trade',
          )


######################################################################
#  LOADING ENDPOINTS AND MODELS
######################################################################
from api_v1.endpoints import *
from api_v1.models import string_model
from api_v1.endpoints import string_endpoints, list_endpoints, map_endpoints
