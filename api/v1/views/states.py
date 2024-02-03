#!/usr/bin/python3
""" RESTAPI Action For the State Object"""

from models.state import State
import models
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ Retreive All States """
    all_states = []
    for state in storage.all(State).values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def remove_state(state_id):
    state = storage.get(State, state_id)
    if state is not None:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)
    else:
        abort(404)
