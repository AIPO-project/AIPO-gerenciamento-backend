import requests
from flask import request, jsonify
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token)
from datetime import timedelta

URL_TOKEN    = "https://suap.ifrn.edu.br/api/token/pair"
URL_DADOS    = "https://suap.ifrn.edu.br/api/rh/meus-dados"

# Função para inicializar o JWT no app
def init_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
    jwt = JWTManager(app)
    return jwt

# Função para obter o token de acesso
def get_token(matricula, senha):
    response = requests.post(URL_TOKEN, json={'username': matricula, 'password': senha})

    if response.status_code == 200:
        access_token = create_access_token(matricula)
        refresh_token = create_refresh_token(matricula)
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401
    
