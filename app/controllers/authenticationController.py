from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta
import requests

URL_TOKEN = "https://suap.ifrn.edu.br/api/token/pair"

class AuthController:
    @staticmethod
    def login():
        data = request.get_json()
        matricula = data.get("matricula")
        senha = data.get("senha")

        if not matricula or not senha:
            return jsonify({"message": "Matrícula e senha obrigatórias"}), 400

        try:
            # Tenta autenticar no SUAP
            response = requests.post(URL_TOKEN, json={'username': matricula, 'password': senha}, timeout=5)
        except requests.exceptions.RequestException as e:
            # Se houver erro de conexão ou timeout
            return jsonify({"message": "Erro ao conectar com o SUAP", "error": str(e)}), 500

        if response.status_code != 200:
            return jsonify({"message": "Credenciais inválidas"}), 401

        try:
            # Tenta ler o JSON retornado pelo SUAP
            token_data = response.json()
        except ValueError:
            return jsonify({"message": "Resposta inválida do SUAP"}), 500

        # Cria JWT local
        access_token = create_access_token(identity=matricula, expires_delta=timedelta(minutes=30))
        refresh_token = create_refresh_token(identity=matricula)

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200

    @staticmethod
    @jwt_required()
    def protected():
        user = get_jwt_identity()
        return jsonify({"message": f"Acesso permitido para {user}!"}), 200
