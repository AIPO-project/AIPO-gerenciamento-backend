from app import app
from app.controllers.usuarioController import UsuarioController
from flask import request, jsonify

@app.route("/api/usuario", methods=["GET"])
def listar_usuarios():
    usuarios = UsuarioController.listar_usuarios()
    lista = [
        {
            "id": u.id,
            "nome": u.nome,
            "matricula": u.matricula,
            "tipoUsuario": u.tipoUsuario,
            "nivelGerencia": u.nivelGerencia,
            "chave": u.chave,
            "ativo": u.ativo
        }
        for u in usuarios
    ]
    return jsonify(lista)

@app.route("/api/usuario/<matricula>", methods=["GET"])
def buscar_usuario(matricula):
    usuario = UsuarioController.buscar_por_matricula(matricula)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404
    u = usuario
    return jsonify({
        "id": u.id,
        "nome": u.nome,
        "matricula": u.matricula,
        "tipoUsuario": u.tipoUsuario,
        "nivelGerencia": u.nivelGerencia,
        "chave": u.chave,
        "ativo": u.ativo
    })

@app.route("/api/usuario/<matricula>", methods=["PUT"])
def atualizar_usuario(matricula):
    print(f"Atualizando usuário com matrícula: {matricula}")
    usuario = UsuarioController.buscar_por_matricula(matricula)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    data = request.get_json()
    print(f"Dados recebidos para atualização: {data}")
    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    # Atualiza os campos que vierem no JSON
    usuario.nome = data.get("nome", usuario.nome)
    usuario.chave = data.get("chave", usuario.chave)

    try:
        UsuarioController.atualizar_usuario(matricula, usuario)
        return jsonify({"message": "Usuário atualizado com sucesso"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
