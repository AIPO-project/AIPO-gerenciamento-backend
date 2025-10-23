from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.acesso_controller import (
    list_acessos, create_acesso, get_acesso, delete_acesso
)

bp_acessos = Blueprint("acessos", __name__)

@bp_acessos.route("/acessos", methods=["GET"])
@jwt_required()
def route_list_acessos():
    filters = {
        "usuario": request.args.get("usuario"),
        "sala": request.args.get("sala"),
        "date_from": request.args.get("date_from"),
        "date_to": request.args.get("date_to"),
    }
    return jsonify(list_acessos(filters))

@bp_acessos.route("/acessos", methods=["POST"])
@jwt_required()
def route_create_acesso():
    data = request.get_json() or {}
    return jsonify(create_acesso(data)), 201

@bp_acessos.route("/acessos/<int:acesso_id>", methods=["GET"])
@jwt_required()
def route_get_acesso(acesso_id):
    return jsonify(get_acesso(acesso_id))

@bp_acessos.route("/acessos/<int:acesso_id>", methods=["DELETE"])
@jwt_required()
def route_delete_acesso(acesso_id):
    return jsonify(delete_acesso(acesso_id)), 200
