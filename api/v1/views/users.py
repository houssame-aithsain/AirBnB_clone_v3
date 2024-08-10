#!/usr/bin/python3
"""
this module creates a new view for User objects that handles all default
"""
from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'])
def get_users():
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
