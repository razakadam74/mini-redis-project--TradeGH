from flask import Flask
from flask_restplus import Api
from werkzeug.contrib.fixers import ProxyFix
from flask_redis import FlaskRedis

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


app.config.from_object('config')

redis_store = FlaskRedis(app)

api = Api(app, version='1.0', title='Mini Redis Server',
    description='A Mini Redis Server Take-Home Project specification for candidates for Engineering @ Trade',
)




from .models import *
from .controller import *

