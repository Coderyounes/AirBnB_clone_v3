#!/usr/bin/python3
""" Flask App """
from api.v1.views import app_views
from flask import jsonify
from models.engine.db_storage import classes
import models


@app_views.route('/status', strict_slashes=False)
def status():
    """
        FUNCTION RETURN DATA IN JSON
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
        FUNCTION RETURN CURRENT CLASS STATS
    """
    res = {}
    for key in classes.keys():
        res[key] = models.storage.count(classes[key])

    return jsonify(res)
