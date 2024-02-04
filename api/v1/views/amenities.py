#!/usr/bin/python3
""" RESTAPI Action For the State Object"""

from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities():
    """ Retreive All States """
    all_amenities = []
    for amenity in storage.all(Amenity).values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Reteive a Single Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def remove_amenity(amenity_id):
    """ Remove a Amenity via their ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """ Create a new Amenity"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Update an Existing Amenity"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if 'name' in data:
        amenity.name = data['name']
    storage.save()
    return jsonify(amenity.to_dict()), 200
