#!/usr/bin/python3
"""Module that handles all default RestFul API actions for States"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Returns a list of all the states"""
    states = list(storage.all(State).values())
    state_list = []
    for state in states:
        state_dict = state.to_dict()
        state_list.append(state_dict)
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Returns the state requested

    state_id: id of the state to get"""
    states = list(storage.all(State).values())
    for state in states:
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state

    state_id: id of the state to delete"""
    states = list(storage.all(State).values())
    state = None
    for item in states:
        if item.id == state_id:
            state = item
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new state"""
    states = list(storage.all(State).values())
    state_dict = request.get_json(silent=True)
    if state_dict is None:
        return make_response("Not a JSON", 400)
    try:
        state_name = state_dict['name']
    except KeyError:
        return make_response("Missing name", 400)
    state = State(name=state_name)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a state

    state_id: id of the state to update"""
    states = list(storage.all(State).values())
    state_dict = request.get_json(silent=True)
    if state_dict is None:
        return make_response("Not a JSON", 400)
    for state in states:
        if state.id == state_id:
            for k, v in state_dict.items():
                if k != 'id' and k != 'created_at' and k != 'updated_at':
                    setattr(state, k, v)
            storage.save()
            return jsonify(state.to_dict()), 200
    abort(404)
