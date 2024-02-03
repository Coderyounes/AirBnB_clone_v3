#!/usr/bin/python3
""" RESTAPI Action For the State Object"""

from models.state import State
import models
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


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


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_state = State(**request.get_json())
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if 'name' in data:
        state.name = data['name']
    storage.save()
    return jsonify(state.to_dict()), 200
