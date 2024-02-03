#!/usr/bin/python3
""" RESTAPI Action For the State Object"""

from models.state import State
import models
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ Retreive All States """
    all_states = []
    for state in storage.all(State).values():
        all_states.append(state.to_dict())
    return jsonify(all_states)
