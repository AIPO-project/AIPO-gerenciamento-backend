from app.models import Usuario
from app.extensions import db
from flask import abort

def list_users():
    return [u.to_dict() for u in Usuario.query.all()]

def create_user(data):
    if not data.get("nome") or not data.get("matricula"):
        abort(400, "nome e matricula são obrigatórios")
    user = Usuario(
        nome=data.get("nome"),
        matricula=data.get("matricula"),
        tipoUsuario=data.get("tipoUsuario"),
        nivelGerencia=data.get("nivelGerencia"),
        chave=data.get("chave"),
        ativo=data.get("ativo", True),
    )
    db.session.add(user)
    db.session.commit()
    return user.to_dict()

def get_user(user_id):
    user = Usuario.query.get_or_404(user_id)
    return user.to_dict()

def update_user(user_id, data):
    user = Usuario.query.get_or_404(user_id)
    for field in ["nome", "matricula", "tipoUsuario", "nivelGerencia", "chave", "ativo"]:
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()
    return user.to_dict()

def delete_user(user_id):
    user = Usuario.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "deletado"}
