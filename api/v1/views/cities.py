#!/usr/bin/python3
"""
create a new view for City objects
that handles all default RESTful API actions
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


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def cities_state(state_id):
    """Retrieves the list of all City objects of a State."""
    state_by_id = storage.get(State, state_id)
    if state_by_id is not None:
        return jsonify([city.to_dict() for city in state_by_id.cities])
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def get_city_id(city_id):
    """Retrieves a City object by ID."""
    city_by_id = storage.get(City, city_id)
    if city_by_id is not None:
        return jsonify(city_by_id.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_city_id(city_id):
    """Deletes a City object by ID."""
    city_by_id = storage.get(City, city_id)
    if city_by_id is not None:
        storage.delete(city_by_id)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['POST'])
def post_city(state_id):
    """Creates a new City object."""
    state_by_id = storage.get(State, state_id)
    if state_by_id is None:
        abort(404)
    json_req = request.get_json()
    if not json_req:
        abort(400, 'Not a JSON')
    if 'name' not in json_req:
        abort(400, 'Missing name')
    new_city = City(**request.get_json())
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("cities/<city_id>", strict_slashes=False, methods=['PUT'])
def put_city_id(city_id):
    """Updates a City object by ID."""
    json_req = request.get_json()
    if not json_req:
        abort(400, 'Not a JSON')
    city_by_id = storage.get(City, city_id)
    if city_by_id is not None:
        for attr, value in request.get_json().items():
            setattr(city_by_id, attr, value)
        storage.save()
        return jsonify(city_by_id.to_dict()), 200
    abort(404)
