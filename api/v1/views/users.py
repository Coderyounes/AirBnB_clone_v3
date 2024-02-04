#!/usr/bin/python3
""" RESTAPI Action For the State Object"""

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def all_users():
    """ Retreive All PLaces """
    all_users = []
    for user in storage.all(User).values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Reteive a Single User"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def remove_user(user_id):
    """ Remove a User via their ID"""
    user = storage.get(User, user_id)
    if user is not None:
        if user.id == user_id:
            storage.delete(user)
            storage.save()
            return jsonify({}), 200
        else:
            abort(404)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ Create a new User"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.json:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in request.json:
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**request.get_json())
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Update an Existing User"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if 'password' in data:
        user.password = data['password']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    storage.save()
    return jsonify(user.to_dict()), 200
