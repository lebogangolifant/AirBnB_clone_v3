#!/usr/bin/python3
"""
Create a new view for User object
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


@app_views.route("/users", strict_slashes=False,
                 methods=['GET'])
def users():
    """Retrieves the list of all User objects."""
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['GET'])
def get_user_id(user_id):
    """Retrieves a User object by ID."""
    user_by_id = storage.get(User, user_id)
    if user_by_id is not None:
        return jsonify(user_by_id.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_user_id(user_id):
    """Deletes a User object by ID."""
    user_by_id = storage.get(User, user_id)
    if user_by_id is not None:
        storage.delete(user_by_id)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/users", strict_slashes=False,
                 methods=['POST'])
def post_user():
    """Creates a new User object."""
    json_req = request.get_json()
    if not json_req:
        abort(400, 'Not a JSON')
    if 'email' not in json_req:
        abort(400, 'Missing email')
    if 'password' not in json_req:
        abort(400, 'Missing password')
    new_user = User(**request.get_json())
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False,
                 methods=['PUT'])
def put_user_id(user_id):
    """Updates a User object by ID."""
    json_req = request.get_json()
    if not json_req:
        abort(400, 'Not a JSON')
    user_by_id = storage.get(User, user_id)
    if user_by_id is not None:
        for attr, value in request.get_json().items():
            if (hasattr(user_by_id, attr) and
                    attr != 'id' and attr != 'created_at' and
                    attr != 'updated_at') and attr != 'email':
                setattr(user_by_id, attr, value)
        storage.save()
        return jsonify(user_by_id.to_dict()), 200
    abort(404)
