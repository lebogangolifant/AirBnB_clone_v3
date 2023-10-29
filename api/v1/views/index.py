#!/usr/bin/python3
"""
Create a route /status on the object app_views
that returns a JSON
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """route /status on the object app_views that returns
    a JSON: status: OK"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Retrieves the number of each object by type."""
    return jsonify({"amenities": storage.count('Amenity'),
                    "cities": storage.count('City'),
                    "places": storage.count('Place'),
                    "reviews": storage.count('Review'),
                    "states": storage.count('State'),
                    "users": storage.count('User')})
