#!/usr/bin/python3
"""Module that handles all default RestFul API actions for amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Returns a list of all the amenities"""
    amenities = list(storage.all(Amenity).values())
    amenity_list = []
    for amenity in amenities:
        amenity_dict = amenity.to_dict()
        amenity_list.append(amenity_dict)
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Returns the amenity requested

    amenity_id: id of the amenity to get"""
    amenities = list(storage.all(Amenity).values())
    for amenity in amenities:
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity

    amenity_id: id of the amenity to delete"""
    amenities = list(storage.all(Amenity).values())
    amenity = None
    for item in amenities:
        if item.id == amenity_id:
            amenity = item
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new amenity"""
    amenities = list(storage.all(Amenity).values())
    amenity_dict = request.get_json(silent=True)
    if amenity_dict is None:
        return make_response("Not a JSON", 400)
    try:
        amenity_name = amenity_dict['name']
    except KeyError:
        return make_response("Missing name", 400)
    amenity = Amenity(name=amenity_name)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an amenity

    amenity_id: id of the amenity to update"""
    amenities = list(storage.all(Amenity).values())
    amenity_dict = request.get_json(silent=True)
    if amenity_dict is None:
        return make_response("Not a JSON", 400)
    for amenity in amenities:
        if amenity.id == amenity_id:
            for k, v in amenity_dict.items():
                if k != 'id' and k != 'created_at' and k != 'updated_at':
                    setattr(amenity, k, v)
            storage.save()
            return jsonify(amenity.to_dict()), 200
    abort(404)
