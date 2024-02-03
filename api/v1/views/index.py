#!/usr/bin/python3
""" Flask App """
from api.v1.views import app_views
from flask import jsonify
from models.engine.db_storage import classes
import models
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


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
    classes = [Amenity, City, Place, Review, State, User]
    db_table = ["amenities", "cities", "places", "reviews", "states", "users"]
    res = {}
    for i in range(len(db_table)):
        res[db_table[i]] = models.storage.count(classes[i])

    return jsonify(res)
