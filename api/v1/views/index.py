#!/usr/bin/python3
'''
Route that returns a JSON file with the status
'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def display_status():
    return jsonify({"status": "OK"})
