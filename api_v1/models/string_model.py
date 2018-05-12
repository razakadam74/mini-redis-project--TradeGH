import logging
import pickle
from cerberus import Validator
from api_v1.utils import DatabaseConnectionError, DataValidationError
from api_v1 import redis_store


######################################################################
# Pet Model for database
#   This class must be initialized with use_db(redis) before using
#   where redis is a value connection to a Redis database
######################################################################

class String(object):
    logger = logging.getLogger(__name__)
    schema = {
        'id': {'type': 'integer'},
        'name': {'type': 'string', 'required': True}
        }
    __validator = Validator(schema)

    def __init__(self, id=0, name=None):
        """ Constructor """
        self.id = int(id)
        self.name = name

    def save(self):
        """ Saves a string in the database """
        if self.name is None:   # name is the only required field
            raise DataValidationError('name attribute is not set')
        if self.id == 0:
            self.id = String.__next_index()
        redis_store.set(String.key(self.id), pickle.dumps(self.serialize()))

    def delete(self):
        """ Deletes a Pet from the database """
        redis_store.delete(String.key(self.id))


    def serialize(self):
        """ serializes a Pet into a dictionary """
        return {
            "id": self.id,
            "name": self.name
        }

    def deserialize(self, data):
        """ deserializes a Pet my marshalling the data """
        if isinstance(data, dict) and String.__validator.validate(data):
            self.name = data['name']
        else:
            raise DataValidationError('Invalid pet data: ' + str(String.__validator.errors))
        return self


    ######################################################################

    #  S T A T I C   D A T A B S E   M E T H O D S
    ######################################################################
    @staticmethod
    def __next_index():
        """ Increments the index and returns it """
        return redis_store.incr(String.__name__.lower() + '-index')

    @staticmethod
    def key(value):
        """ Creates a Redis key using class name and value """
        return '{}:{}'.format(String.__name__.lower(), value)

    @staticmethod
    def remove_all():
        """ Removes all Pets from the database """
        redis_store.flushall()

    @staticmethod
    def all():
        """ Query that returns all Pets """
        # results = [Pet.from_dict(redis.hgetall(key)) for key in redis.keys() if key != 'index']
        results = []
        for key in redis_store.keys(String.key('*')):
            data = pickle.loads(redis_store.get(key))
            string = String(data['id']).deserialize(data)
            results.append(string)
        return results

    ######################################################################
    #  F I N D E R   M E T H O D S
    ######################################################################

    @staticmethod
    def find(id):
        """ Query that finds Pets by their id """
        key = String.key(id)
        if redis_store.exists(key):
            data = pickle.loads(redis_store.get(key))
            pet = String(data['id']).deserialize(data)
            return pet
        return None
