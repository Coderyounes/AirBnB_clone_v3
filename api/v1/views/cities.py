#!/usr/bin/python3
""" RESTAPI Action For the State Object"""

from models.city import City
from models.state import State
import models
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities/', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ Retreive All States """
    db_cities = storage.all(City).values()
    all_cities = []
    for city in db_cities:
        if city.id == state_id:
            all_cities.append(city.to_dict())
        else:
            abort(404)
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_citie(city_id):
    """ Reteive a Single City"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def remove_city(city_id):
    """ Remove a City via their ID"""
    city = storage.get(City, city_id)
    if city is not None:
        if city.id == city_id:
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = storage.get(State, state_id)
    if state is not None:
        new_city = City(**request.get_json())
        new_city.state_id = state_id
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Update an Existing CIty"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if 'name' in data:
        city.name = data['name']
    storage.save()
    return jsonify(city.to_dict()), 200
