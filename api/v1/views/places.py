#!/usr/bin/python3
"""Module that handles all default RestFul API actions for places"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Returns a list of all the places"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    place_list = []
    for place in city.places:
        place_dict = place.to_dict()
        place_list.append(place_dict)
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Returns the place requested

    place_id: id of the place to get"""
    places = list(storage.all(Place).values())
    for place in places:
        if place.id == place_id:
            return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place

    place_id: id of the place to delete"""
    places = list(storage.all(Place).values())
    place = None
    for item in places:
        if item.id == place_id:
            place = item
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    place_dict = request.get_json(silent=True)
    if place_dict is None:
        return make_response("Not a JSON", 400)

    try:
        place_user_id = place_dict['user_id']
    except KeyError:
        return make_response("Missing user_id", 400)
    user = storage.get("User", place_user_id)
    if user is None:
        abort(404)

    try:
        place_name = place_dict['name']
    except KeyError:
        return make_response("Missing name", 400)

    place = Place(name=place_name, user_id=place_user_id, city_id=city_id)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a place

    place_id: id of the place to update"""
    places = list(storage.all(Place).values())
    place_dict = request.get_json(silent=True)
    if place_dict is None:
        return make_response("Not a JSON", 400)
    for place in places:
        if place.id == place_id:
            for k, v in place_dict.items():
                if k != 'id' and k != 'created_at' and k != 'updated_at'\
                        and k != 'user_id' and k != 'city_id':
                    setattr(place, k, v)
            storage.save()
            return jsonify(place.to_dict()), 200
    abort(404)
