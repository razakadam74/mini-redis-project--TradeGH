import logging
import pickle
from cerberus import Validator
from api_v1.utils import DataValidationError
from api_v1 import redis_store


######################################################################
# Map Model for database
#   This class must be initialized with use_db(redis) before using
#   where redis is a value connection to a Redis database
######################################################################

class Map(object):
    logger = logging.getLogger(__name__)
    schema = {
        'key': {'type': 'string', 'required': True},
        'value': {'type': 'dict', 'required': True}
    }
    __validator = Validator(schema)

    def __init__(self, key=None, value=None):
        """ Constructor """
        self.key = key
        self.value = value

    def save(self):
        """ Saves a map_object in the database """
        if self.value is None:
            raise DataValidationError('value attribute is not set')
        if self.key is None:
            raise DataValidationError('key attribute is not set')
        redis_store.set(Map.generate_key(self.key), pickle.dumps(self.serialize()))

    def delete(self):
        """ Deletes a Map from the database """
        redis_store.delete(Map.generate_key(self.key))

    def add_map_item(self, payload):
        key = payload.get('key', None)
        if not key:
            raise DataValidationError('key attribute is not found')
        value = payload.get('value', None)
        if not value:
            raise DataValidationError('value attribute is not found')
        self.value[key] = value
        self.save()
        return self


    def serialize(self):
        """ serializes a Map into a dictionary """
        return {
            "key": self.key,
            "value": self.value
        }

    def deserialize(self, data):
        """ deserializes a Map my marshalling the data """
        if isinstance(data, dict) and Map.__validator.validate(data):
            self.key = data['key']
            self.value = data['value']
        else:
            raise DataValidationError('Invalid map_object data: ' + str(Map.__validator.errors))
        return self

    @staticmethod
    def check_if_api_payload_is_valid(value):
        if not value:
            raise DataValidationError('map key and value is not found')
        if not value.get('key', None):
            raise DataValidationError('key attribute is not found')
        if not value.get('value', None):
            raise DataValidationError('value attribute is not found')
        return True

    ######################################################################

    #  S T A T I C   D A T A B S E   M E T H O D S
    ######################################################################
    @staticmethod
    def __next_index():
        """ Increments the index and returns it """
        return redis_store.incr(Map.__name__.lower() + '-index')

    @staticmethod
    def generate_key(value):
        """ Creates a Redis key using class value and value """
        return '{}:{}'.format(Map.__name__.lower(), value)

    @staticmethod
    def remove_all():
        """ Removes all Lists from the database """
        redis_store.flushall()

    @staticmethod
    def all():
        """ Query that returns all strings """
        # results = [Map.from_dict(redis.hgetall(key)) for key in redis.keys() if key != 'index']
        results = []
        for key in redis_store.keys(Map.generate_key('*')):
            data = pickle.loads(redis_store.get(key))
            map_object = Map(data['key']).deserialize(data)
            results.append(map_object)
        return results

######################################################################
#  EXTRA STATIC  M E T H O D S
######################################################################

    @staticmethod
    def append(payload):
        key = payload.get('key', None)
        value = payload.get('value', None)
        if not key:
            raise DataValidationError('key attribute is not found')
        if not value:
            raise DataValidationError('value attribute is not found')
        map_object = Map.find(key)
        if map_object:
            map_object.value.append(value)
            map_object.save()
            return map_object
        raise DataValidationError('key attribute is not found')


    ######################################################################
    #  F I N D E R   M E T H O D S
    ######################################################################

    @staticmethod
    def find(key):
        """ Query that finds Lists by their key """
        key = Map.generate_key(key)
        if redis_store.exists(key):
            data = pickle.loads(redis_store.get(key))
            map_object = Map(key=data['key'], value=data['value']).deserialize(data)
            return map_object
        return None
