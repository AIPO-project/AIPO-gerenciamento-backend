from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import requests
from app.extensions import db
from app.models import Usuario
from app.controllers.user_controller import (
    list_users, create_user, get_user, update_user, delete_user, get_user_salas, get_user_acessos
)

bp_users = Blueprint("users", __name__)

@bp_users.route("/users", methods=["GET"])
@jwt_required()
def route_list_users():
    return jsonify(list_users())

@bp_users.route("/users", methods=["POST"])
@jwt_required()
def route_create_user():
    data = request.get_json() or {}
    return jsonify(create_user(data)), 201

@bp_users.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def route_get_user(user_id):
    return jsonify(get_user(user_id))

@bp_users.route("/users/<int:user_id>/salas", methods=["GET"])
@jwt_required()
def route_get_salas_user(user_id):
    return jsonify(get_user_salas(user_id))

@bp_users.route("/users/<int:user_id>/acessos", methods=["GET"])
@jwt_required()
def route_get_acessos_user(user_id):
    return jsonify(get_user_acessos(user_id))

URL_DADOS = "https://suap.ifrn.edu.br/api/rh/meus-dados"

@bp_users.route("/users/<user_id>", methods=["PUT", "PATCH"])
@jwt_required()
def route_update_user(user_id):
    """
    Atualiza foto, nome e ativo do usuário com dados do SUAP.
    Valida que o user_id da rota bate com o usuário do SUAP.
    """

    data = request.get_json() or {}
    access_token = data.get("suap_token")
    if not access_token:
        return jsonify({"error": "Token do SUAP é obrigatório"}), 400

    # Busca dados do SUAP
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(URL_DADOS, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Não foi possível obter dados do SUAP"}), 400
    suap_dados = response.json()

    # Validação de segurança: conferir se o user_id bate com a matrícula do SUAP
    suap_matricula = suap_dados.get("matricula")
    user = Usuario.query.filter_by(matricula=user_id).first()
    if str(user.matricula) != str(suap_matricula):
        return jsonify({"error": "Você não tem permissão para atualizar este usuário"}), 403

    # Atualiza campos desejados
    user.foto = suap_dados.get("url_foto_150x200", user.foto)

    nome_usual = suap_dados.get("nome_usual", "")
    if nome_usual:
        # transforma para "Primeira letra maiúscula"
        user.nome = nome_usual.lower().capitalize()

    user.ativo = suap_dados.get("matricula_regular", user.ativo)

    db.session.commit()

    return jsonify({
        "id": user.id,
        "nome": user.nome,
        "foto": user.foto,
        "ativo": user.ativo
    })

@bp_users.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def route_delete_user(user_id):
    return jsonify(delete_user(user_id)), 200

