from app.models import Autorizacao, Usuario, Sala
from app.extensions import db
from flask import abort

def list_autorizacoes():
    return [a.to_dict() for a in Autorizacao.query.all()]

def create_autorizacao(data):
    id_usuario = data.get("id_usuario")
    id_sala = data.get("id_sala")
    if id_usuario is None or id_sala is None:
        abort(400, "id_usuario e id_sala são obrigatórios")
    if not Usuario.query.get(id_usuario):
        abort(404, "usuario não encontrado")
    if not Sala.query.get(id_sala):
        abort(404, "sala não encontrada")
    auth = Autorizacao(id_usuario=id_usuario, id_sala=id_sala)
    db.session.add(auth)
    db.session.commit()
    return auth.to_dict()

def get_autorizacao(auth_id):
    auth = Autorizacao.query.get_or_404(auth_id)
    return auth.to_dict()

def delete_autorizacao(auth_id):
    auth = Autorizacao.query.get_or_404(auth_id)
    db.session.delete(auth)
    db.session.commit()
    return {"message": "deletado"}
