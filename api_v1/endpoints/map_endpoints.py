from flask_restplus import Resource
from api_v1 import api, app
from werkzeug.exceptions import NotFound
from flask_api import status  # HTTP Status Codes
from api_v1.utils import check_content_type
from api_v1.models import map_namespace, map_model, map_model_get, map_item, map_value_model
from api_v1.models.map_model import Map


######################################################################
#  MAPS  WITH REDIS ENDPOINTS
######################################################################

######################################################################
#  PATH: /map
######################################################################
@map_namespace.route('/', strict_slashes=False)
class MapCollection(Resource):
    """ Handles all interactions with collections of Map """

    # ------------------------------------------------------------------
    # MAP ALL MAPS
    # ------------------------------------------------------------------
    @map_namespace.doc('list_maps')
    @map_namespace.marshal_list_with(map_model)
    def get(self):
        """
        Return all Map values in the database
        This endpoint will return all the map objects in the database
        """
        maps = Map.all()
        results = [map_object.serialize() for map_object in maps]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW MAP
    # ------------------------------------------------------------------
    @map_namespace.doc('append a new map to maps')
    @map_namespace.expect(map_model)
    @map_namespace.response(400, 'The posted data was not valid')
    @map_namespace.response(201, 'Map created successfully')
    @map_namespace.marshal_with(map_model, code=201)
    def post(self):
        """
        Instantiate or overwrite a Map identified by key with value value
        This endpoint will create a Map based the data in the body that is posted
        """
        check_content_type('application/json')
        map_object = Map()
        app.logger.info('Payload = %s', api.payload)
        map_object.deserialize(api.payload)
        map_object.save()
        app.logger.info('Map with new key [%s] saved!', map_object.key)
        return map_object.serialize(), status.HTTP_201_CREATED


######################################################################
#  PATH: /map/{key}
######################################################################
@map_namespace.route('/<string:key>')
@map_namespace.param('key', 'The Map identifier')
class MapResource(Resource):
    """
    MapResource class

    Allows the manipulation of a single Map
    GET /map_object{key} - Returns a Map with the key
    PUT /map_object{key} - Update a Map with the key
    DELETE /map_object{key} -  Deletes a Map with the key
    """

    # ------------------------------------------------------------------
    # RETRIEVE A MAP
    # ------------------------------------------------------------------
    @map_namespace.doc('get_string')
    @map_namespace.response(404, 'Map not found')
    @map_namespace.marshal_with(map_model)
    def get(self, key):
        """
        Return the Map value identified by key
        This endpoint will return a Map based on it's key
        """
        app.logger.info("Request to Retrieve a map_object with key [%s]", key)
        map_object = Map.get_value_with_key(key)
        if not map_object:
            raise NotFound("Map with key '{}' was not found.".format(key))
        return map_object.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A MAP TO AN IDENTIFIED MAP
    # ------------------------------------------------------------------
    @map_namespace.doc('add_item_to_map')
    @map_namespace.response(404, 'Map not found')
    @map_namespace.marshal_with(map_model)
    @map_namespace.expect(map_item)
    def post(self, key):
        """
        Add the mapping mapkey -> mapvalue to the Map identified by key.
        This endpoint will return a Map based on it's key
        """
        app.logger.info("Request to Retrieve a map_object with key [%s]", key)
        map_object = Map.append(key, api.payload)
        # map_object = Map.find(key)
        # if not map_object:
        #     raise NotFound("Map with key '{}' was not found.".format(key))
        # # map_object.add_map_item(api.payload)
        # # return map_object.serialize(), status.HTTP_200_OK
        return map_object, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING MAP
    # ------------------------------------------------------------------
    @map_namespace.doc('update_strings')
    @map_namespace.response(404, 'Map not found')
    @map_namespace.response(400, 'The posted Map data was not valid')
    @map_namespace.expect(map_model)
    @map_namespace.marshal_with(map_model)
    def put(self, key):
        """
        Update the Map identified by key
        This endpoint will update a Map based the body that is posted
        """
        app.logger.info('Request to Update a map_object with key [%s]', key)
        check_content_type('application/json')
        map_object = Map.get_value_with_key(key)
        if not map_object:
            # api.abort(404, "Map with key '{}' was not found.".format(key))
            raise NotFound('Map with key [{}] was not found.'.format(key))
        # data = request.get_json()
        data = api.payload
        app.logger.info(data)
        map_object.deserialize(data)
        map_object.key = key
        map_object.save()
        return map_object.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A MAP
    # ------------------------------------------------------------------
    @map_namespace.doc('delete_strings')
    @map_namespace.response(204, 'Map deleted')
    def delete(self, key):
        """
        Delete the Map identified by key
        This endpoint will delete a Map based the key specified in the path
        """
        app.logger.info('Request to Delete a map_object with key [%s]', key)
        map_object = Map.get_value_with_key(key)
        if map_object:
            map_object.delete()
        return 'Map deleted', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /map/{key}/{inner_key}
######################################################################
@map_namespace.route('/<string:key>/<string:inner_key>')
@map_namespace.param('key', 'The Map identifier')
@map_namespace.param('inner_key', 'The Inner Map identifier')
class MapOtherResource(Resource):
    """ Handles all interactions with a particular Map """

    # ------------------------------------------------------------------
    # Return the String identified by mapkey from within the
    # Map identified by key.
    # ------------------------------------------------------------------
    @map_namespace.doc('get_mapkey value')
    # @map_namespace.marshal_list_with(map_model_get)
    # @map_namespace.expect(map_model_get)
    def get(self, key, inner_key):
        """
        Return the String identified by map key from within the Map identified by key.
        This endpoint will return the String identified by mapkey from within the Map identified by key.
        """
        app.logger.info('Request to Update a map_object with key [%s]', key)
        # check_content_type('application/json')
        map_object = Map.find(key)
        if not map_object:
            raise NotFound("Map with key '{}' was not found.".format(key))
        item = map_object.get_value_with_key(inner_key)
        # item  = map_object.value.get(inner_key, None)
        if not item:
            # map_object.value[0]['key']
            raise NotFound("Item with key '{}' was not found in '{}' Map.".format(inner_key, key))
        return item, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A MAP
    # ------------------------------------------------------------------
    @map_namespace.doc('delete_strings')
    @map_namespace.response(204, 'Map deleted')
    def delete(self, key, inner_key):
        """
        Delete the value identified by map key from the Map identified by key.
        This endpoint will delete a Map with the Map based the key specified in the path
        """
        app.logger.info('Request to Delete a map_object with key [%s]', key)
        map_object = Map.find(key)
        if not map_object:
            raise NotFound("Map with key '{}' was not found.".format(key))
        map_object.delete_item_from_map(inner_key)
        return 'Map deleted', status.HTTP_204_NO_CONTENT
