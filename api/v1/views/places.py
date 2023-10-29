#!/usr/bin/python3
"""
Create a new view for Place objects
that handles all default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def places_city(city_id):
    """Retrieves the list of all Place objects of a City."""
    city_by_id = storage.get(City, city_id)
    if city_by_id is not None:
        return jsonify([place.to_dict() for place in city_by_id.places])
    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET'])
def get_place_id(place_id):
    """Retrieves a Place object by ID."""
    place_by_id = storage.get(Place, place_id)
    if place_by_id is not None:
        return jsonify(place_by_id.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_place_id(place_id):
    """Deletes a Place object by ID."""
    place_by_id = storage.get(Place, place_id)
    if place_by_id is not None:
        storage.delete(place_by_id)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """Create a new place in a city"""
    city_by_id = storage.get(City, city_id)
    if city_by_id is None:
        abort(404)
    json_req = request.get_json()
    if not json_req:
        abort(400, 'Not a JSON')
    if 'user_id' not in json_req:
        abort(400, 'Missing user_id')
    user_id = request.get_json()["user_id"]
    user_by_id = storage.get(User, user_id)
    if user_by_id is None:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    new_place = Place(**request.get_json())
    new_place.city_id = city_id
    new_place.user_id = user_by_id.id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['PUT'])
def put_place_id(place_id):
    """Updates a Place object by ID."""
    json_req = request.get_json()
    if not json_req:
        abort(400, 'Not a JSON')
    place_by_id = storage.get(Place, place_id)
    if place_by_id is not None:
        for attr, value in request.get_json().items():
            if (hasattr(place_by_id, attr) and
                    attr != 'id' and attr != 'created_at' and
                    attr != 'updated_at' and attr != 'user_id' and
                    attr != 'city_id'):
                setattr(place_by_id, attr, value)
        storage.save()
        return jsonify(place_by_id.to_dict()), 200
    abort(404)
