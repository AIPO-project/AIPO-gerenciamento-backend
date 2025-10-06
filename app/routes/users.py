from flask import Blueprint, request, jsonify
from app.controllers.user_controller import (
    list_users, create_user, get_user, update_user, delete_user
)

bp_users = Blueprint("users", __name__)

@bp_users.route("/users", methods=["GET"])
def route_list_users():
    return jsonify(list_users())

@bp_users.route("/users", methods=["POST"])
def route_create_user():
    data = request.get_json() or {}
    return jsonify(create_user(data)), 201

@bp_users.route("/users/<int:user_id>", methods=["GET"])
def route_get_user(user_id):
    return jsonify(get_user(user_id))

@bp_users.route("/users/<int:user_id>", methods=["PUT", "PATCH"])
def route_update_user(user_id):
    data = request.get_json() or {}
    return jsonify(update_user(user_id, data))

@bp_users.route("/users/<int:user_id>", methods=["DELETE"])
def route_delete_user(user_id):
    return jsonify(delete_user(user_id)), 200
