#!/usr/bin/python3
"""RESTful API Application"""

from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def _storage(self):
    """Closes the database when the app context is torn down."""
    storage.close()


    @app.errorhandler(404)
    def not_found(error):
        """Custom 404 error response."""
        return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)

