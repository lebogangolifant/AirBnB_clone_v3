#!/usr/bin/python3
"""
Create a route /status on the object app_views
that returns a JSON
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """route /status on the object app_views that returns
    a JSON: status: OK"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """endpoint that retrieves the number of each objects by type"""
    return jsonify({"amenities": storage.count('Amenity'),
                    "cities": storage.count('City'),
                    "places": storage.count('Place'),
                    "reviews": storage.count('Review'),
                    "states": storage.count('State'),
                    "users": storage.count('User')})
