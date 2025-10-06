from flask import Blueprint, request, jsonify
from app.controllers.autorizacao_controller import (
    list_autorizacoes, create_autorizacao, get_autorizacao, delete_autorizacao
)

bp_autorizacoes = Blueprint("autorizacoes", __name__)

@bp_autorizacoes.route("/autorizacoes", methods=["GET"])
def route_list_autorizacoes():
    return jsonify(list_autorizacoes())

@bp_autorizacoes.route("/autorizacoes", methods=["POST"])
def route_create_autorizacao():
    data = request.get_json() or {}
    return jsonify(create_autorizacao(data)), 201

@bp_autorizacoes.route("/autorizacoes/<int:auth_id>", methods=["GET"])
def route_get_autorizacao(auth_id):
    return jsonify(get_autorizacao(auth_id))

@bp_autorizacoes.route("/autorizacoes/<int:auth_id>", methods=["DELETE"])
def route_delete_autorizacao(auth_id):
    return jsonify(delete_autorizacao(auth_id)), 200
