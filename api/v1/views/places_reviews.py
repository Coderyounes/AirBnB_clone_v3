#!/usr/bin/python3
""" RESTFUL API Action for review"""

from models.review import Review
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    place = storage.get(Place, place_id)
    reviews = []
    if not place:
        abort(404)
    for obj in place.reviews:
        reviews.append(obj.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def single_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    pass
