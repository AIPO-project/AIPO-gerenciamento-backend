from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.sala_controller import (
    list_salas, create_sala, get_sala, update_sala, delete_sala
)

bp_salas = Blueprint("salas", __name__)

@bp_salas.route("/salas", methods=["GET"])
@jwt_required()
def route_list_salas():
    return jsonify(list_salas())

@bp_salas.route("/salas", methods=["POST"])
@jwt_required()
def route_create_sala():
    data = request.get_json() or {}
    return jsonify(create_sala(data)), 201

@bp_salas.route("/salas/<int:sala_id>", methods=["GET"])
@jwt_required()
def route_get_sala(sala_id):
    return jsonify(get_sala(sala_id))

@bp_salas.route("/salas/<int:sala_id>", methods=["PUT", "PATCH"])
@jwt_required()
def route_update_sala(sala_id):
    data = request.get_json() or {}
    return jsonify(update_sala(sala_id, data))

@bp_salas.route("/salas/<int:sala_id>", methods=["DELETE"])
@jwt_required()
def route_delete_sala(sala_id):
    return jsonify(delete_sala(sala_id)), 200
