#!/usr/bin/python3
""" RESTAPI Action For the State Object"""

from models.user import User
from models.city import City
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ Retreive All PLaces """
    allplace = storage.all("Place").values()
    place = []
    if not allplace:
        abort(404)
    for obj in allplace:
        if obj.city_id == city_id:
            place.append(obj.to_dict())
    if place == []:
        abort(404)
    else:
        return jsonify(place)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Reteive a Single Place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def remove_place(place_id):
    """ Remove a Place via their ID"""
    place = storage.get(Place, place_id)
    if place is not None:
        if place.id == place_id:
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Create a new Place"""
    city = storage.get(City, city_id)
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.json:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    if 'city_id' not in request.json:
        return make_response(jsonify({"error": "Missing city_id"}), 400)
    if city is None:
        abort(404)
    userid = request.get_json().get('user_id')
    user = storage.get(User, userid)
    if user is None:
        abort(404)
    new_place = Place(**request.get_json())
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update an Existing Place"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if 'name' in data:
        place.name = data['name']
    storage.save()
    return jsonify(place.to_dict()), 200
