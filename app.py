from flask import Flask, jsonify, request
from crud import conexaoBD, read, createUpdateDelete
from auth import get_token, init_jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
init_jwt(app)
CORS(app)

@app.route("/api")
def index():
    return "Home page"

@app.route("/api/users", methods=['GET'])
@jwt_required()
def get_users():
    conexaoBD()

    usuarios = read("SELECT * FROM usuarios", None)
    
    data = []

    for usuario in usuarios:
        usuario = {
            'id': usuario['id'],
            'nome': usuario['nome'],    
            'matricula': usuario['matricula'],
            'tipoUsuario': usuario['tipoUsuario'],
            'nivelGerencia': usuario['nivelGerencia'],
            'chave': usuario['chave'],
            'ativo': usuario['ativo']
        }
        data.append(usuario)

    return jsonify(data)


@app.route("/api/users/<matricula>", methods=['GET'])
@jwt_required()
def get_user(matricula):
    try:
        conexaoBD()
        
        usuario = read("SELECT * FROM usuarios WHERE matricula = %s", (matricula,))
        usuario = usuario[0] if usuario else None

        data = {
            'id': usuario['id'],
            'nome': usuario['nome'],    
            'matricula': usuario['matricula'],
            'tipoUsuario': usuario['tipoUsuario'],
            'nivelGerencia': usuario['nivelGerencia'],
            'chave': usuario['chave'],
            'ativo': usuario['ativo']
        }
        
        return jsonify(data)
    except:
        return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route("/api/salas", methods=['GET'])
@jwt_required()
def get_salas():
    try:
        conexaoBD()
        list = []
        salas = read("SELECT * FROM salas", None)
        for sala in salas: 
            data = {
                'nome': sala['nome'],
                'codigo': sala['codigo'],
                'fechadura': sala['fechadura'],
                'local': sala['local'],
                'ativo': sala['ativo']
            }
            list.append(data)

        return jsonify(list)
    except:
        return jsonify({'message': 'Não há salas cadastradas'}), 404

@app.route("/api/salas/<matricula>", methods=['GET'])
@jwt_required()
def get_salasPorUsuario(matricula):
    try:
        conexaoBD()
        list = []
        salas = read("SELECT s.nome, s.id, s.local, s.fechadura, s.codigo, s.ativo FROM salas AS s, usuarios AS u, autorizacao AS a WHERE s.id = a.id_sala AND u.id = a.id_usuario AND u.matricula = %s", (matricula,))
        for sala in salas: 
            data = {
                'nome': sala['nome'],
                'codigo': sala['codigo'],
                'fechadura': sala['fechadura'],
                'local': sala['local'],
                'ativo': sala['ativo']
            }
            list.append(data)

        return jsonify(list)
    except:
        return jsonify({'message': 'Não há salas cadastradas para o usuario'}), 404

@app.route("/api/login", methods=['GET', 'POST'])
def login():
    data = request.json
    USERNAME = data.get('matricula')
    PASSWORD = data.get('senha')

    response = get_token(USERNAME, PASSWORD)

    return response
    
