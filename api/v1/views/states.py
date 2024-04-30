#!/usr/bin/python3
"""States view for the API."""
from flask import jsonify, abort, request, redirect, url_for, make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id=None):
    """Retrieves a State object.
    Retrieves the list of all State objects.
    """
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())
    else:
        all_states = storage.all(State).values()
        return jsonify([state.to_dict() for state in all_states])


@app_views.route(
    "/states/<state_id>", methods=["DELETE"], strict_slashes=False
)
def delete(state_id):
    """Deletes a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create():
    """Creates a State."""
    data = request.get_json()
    if not data:
        abort(500, 'Not a JSON')
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update(state_id):
    """Updates a State object."""
    state = storage.get(State, state_id)
    data = request.get_json()
    if state is None:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
