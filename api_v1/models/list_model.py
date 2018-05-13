import logging
import pickle
from cerberus import Validator
from api_v1.utils import DataValidationError
from api_v1 import redis_store


######################################################################
# List Model for database
#   This class must be initialized with use_db(redis) before using
#   where redis is a value connection to a Redis database
######################################################################

class List(object):
    logger = logging.getLogger(__name__)
    schema = {
        'key': {'type': 'string', 'required': True},
        'value': {'type': 'list', 'required': True}
        }
    __validator = Validator(schema)

    def __init__(self, key = None, value=None):
        """ Constructor """
        self.key = key
        self.value = value

    def save(self):
        """ Saves a list in the database """
        if self.value is None:
            raise DataValidationError('value attribute is not set')
        if self.key is None:
            raise DataValidationError('key attribute is not set')
        redis_store.set(List.generate_key(self.key), pickle.dumps(self.serialize()))

    def append(self, data):
        if isinstance(data, str):
            pass

    def pop(self):
        pass

    def delete(self):
        """ Deletes a List from the database """
        redis_store.delete(List.generate_key(self.key))

    def serialize(self):
        """ serializes a List into a dictionary """
        return {
            "key": self.key,
            "value": self.value
        }

    def deserialize(self, data):
        """ deserializes a List my marshalling the data """
        if isinstance(data, dict) and List.__validator.validate(data):
            self.key = data['key']
            self.value = data['value']
        else:
            raise DataValidationError('Invalid list data: ' + str(List.__validator.errors))
        return self



    ######################################################################

    #  S T A T I C   D A T A B S E   M E T H O D S
    ######################################################################
    @staticmethod
    def __next_index():
        """ Increments the index and returns it """
        return redis_store.incr(List.__name__.lower() + '-index')

    @staticmethod
    def generate_key(value):
        """ Creates a Redis key using class value and value """
        return '{}:{}'.format(List.__name__.lower(), value)

    @staticmethod
    def remove_all():
        """ Removes all Lists from the database """
        redis_store.flushall()

    @staticmethod
    def all():
        """ Query that returns all strings """
        # results = [List.from_dict(redis.hgetall(key)) for key in redis.keys() if key != 'index']
        results = []
        for key in redis_store.keys(List.generate_key('*')):
            data = pickle.loads(redis_store.get(key))
            list = List(data['key']).deserialize(data)
            results.append(list)
        return results

    ######################################################################
    #  F I N D E R   M E T H O D S
    ######################################################################

    @staticmethod
    def find(key):
        """ Query that finds Lists by their key """
        key = List.generate_key(key)
        if redis_store.exists(key):
            data = pickle.loads(redis_store.get(key))
            list = List(key=data['key'], value= data['value']).deserialize(data)
            return list
        return None
