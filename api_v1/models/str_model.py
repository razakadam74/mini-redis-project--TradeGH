import logging
import pickle
from cerberus import Validator
from api_v1.utils import DataValidationError
from api_v1 import redis_store


######################################################################
# String Model for database
######################################################################

class String(object):
    logger = logging.getLogger(__name__)
    schema = {
        'key': {'type': 'string', 'required': True},
        'value': {'type': 'string', 'required': True}
        }
    __validator = Validator(schema)

    def __init__(self, key = None, value=None):
        """ Constructor """
        self.key = key
        self.value = value

    def save(self):
        ''' Saves a string in the database '''
        self.validate_inputs()
        redis_store.set(String.generate_key(self.key), pickle.dumps(self.serialize()))

    def validate_inputs(self):
        '''Check that key and value are set'''
        if self.value is None:
            raise DataValidationError('value attribute is not set')
        if self.key is None:
            raise DataValidationError('key attribute is not set')

    def delete(self):
        """ Deletes a String from the database """
        redis_store.delete(String.generate_key(self.key))

    def serialize(self):
        """ serializes a String into a dictionary """
        return {
            "key": self.key,
            "value": self.value
        }

    def deserialize(self, data):
        """ deserializes a String my marshalling the data """
        if isinstance(data, dict) and String.__validator.validate(data):
            self.key = data['key']
            self.value = data['value']
        else:
            raise DataValidationError('Invalid string data: ' + str(String.__validator.errors))
        return self


    ######################################################################

    #  S T A T I C   D A T A B S E   M E T H O D S
    ######################################################################
    @staticmethod
    def __next_index():
        """ Increments the index and returns it """
        return redis_store.incr(String.__name__.lower() + '-index')

    @staticmethod
    def generate_key(value):
        """ Creates a Redis key using class value and value """
        return '{}:{}'.format(String.__name__.lower(), value)

    @staticmethod
    def remove_all():
        """ Removes all from the database """
        """ Removes all from the database """
        redis_store.flushall()

    @staticmethod
    def all():
        """ Query that returns all strings """
        # results = [String.from_dict(redis.hgetall(key)) for key in redis.keys() if key != 'index']
        results = []
        for key in redis_store.keys(String.generate_key('*')):
            data = pickle.loads(redis_store.get(key))
            string = String(data['key']).deserialize(data)
            results.append(string)
        return results

    ######################################################################
    #  F I N D E R   M E T H O D S
    ######################################################################

    @staticmethod
    def find(key):
        """ Query that finds Strings by their key """
        key = String.generate_key(key)
        if redis_store.exists(key):
            data = pickle.loads(redis_store.get(key))
            string = String(key=data['key'], value= data['value']).deserialize(data)
            return string
        return None

    @staticmethod
    def search(search_term):
        strings = []
        for key in redis_store.keys(String.generate_key('*')):
            data = pickle.loads(redis_store.get(key))
            string = String(data['key']).deserialize(data)
            strings.append(string)

        results = []
        for string in strings:
            if string.get('key', None).find(search_term) != -1:
                results.append(string)
        return results


