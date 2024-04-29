#!/usr/bin/python3
""" Module for status"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
from models.city import City
from flask import jsonify


# Dictionary mapping model classes to their names
model_classes = {
    "amenities": storage.count(Amenity),
    "cities": storage.count(City),
    "places": storage.count(Place),
    "reviews": storage.count(Review),
    "states": storage.count(State),
    "users": storage.count(User),
}


@app_views.route("/status", methods=["GET"])
def status():
    """
    Returns the status of the application.
    ---
    responses:
      200:
        description: Status of the application.
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """
    Retrieves the number of each object by type.
    ---
    responses:
      200:
        description: Object count by type.
      500:
        description: Error occurred, unable to retrieve statistics.
    """
    # Use dictionary comprehension to create the stats dictionary
    stats = {
        cls_name: storage.count(cls) for cls_name, cls in model_classes.items()
    }
    return jsonify(stats)


@app_views.route("/nop", methods=["GET"])
def page_not_found():
    """
    Returns a 'Not Found' error response.
    ---
    responses:
      404:
        description: The requested resource was not found.
    """
    return jsonify({"error": "Not found"})