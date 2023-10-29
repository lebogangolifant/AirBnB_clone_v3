#!/usr/bin/python3
"""
Create a new view for Review object
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


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def review_places(place_id):
    """Retrieves the list of all Review objects of a Place."""
    place_by_id = storage.get(Place, place_id)
    if place_by_id is not None:
        return jsonify([review.to_dict() for review in place_by_id.reviews])
    abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['GET'])
def get_review_id(review_id):
    """Retrieves a Review object by ID."""
    review_by_id = storage.get(Review, review_id)
    if review_by_id is not None:
        return jsonify(review_by_id.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_review_id(review_id):
    """Deletes a Review object by ID."""
    review_by_id = storage.get(Review, review_id)
    if review_by_id is not None:
        storage.delete(review_by_id)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def post_review(place_id):
    """Creates a new Review object for a Place."""
    place_by_id = storage.get(Place, place_id)
    if place_by_id is None:
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
    if 'text' not in json_req:
        abort(400, 'Missing text')
    new_review = Review(**request.get_json())
    new_review.place_id = place_id
    new_review.user_id = user_by_id.id
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['PUT'])
def put_review_id(review_id):
    """Updates a Review object by ID."""
    json_req = request.get_json()
    if not json_req:
        abort(400, 'Not a JSON')
    review_by_id = storage.get(Review, review_id)
    if review_by_id is not None:
        for attr, value in request.get_json().items():
            if (hasattr(review_by_id, attr) and
                    attr != 'id' and attr != 'created_at' and
                    attr != 'updated_at' and attr != 'user_id' and
                    attr != 'place_id'):
                setattr(review_by_id, attr, value)
        storage.save()
        return jsonify(review_by_id.to_dict()), 200
    abort(404)
