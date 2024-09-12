# Handles API token authentication
from functools import wraps
from flask import request, jsonify
from app.config import Config


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != "Bearer " + Config.API_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated
