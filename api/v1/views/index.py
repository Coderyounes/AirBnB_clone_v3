#!/usr/bin/python3
""" Flask App """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
        FUNCTION RETURN DATA IN JSON
    """
    return jsonify({"status": "OK"})