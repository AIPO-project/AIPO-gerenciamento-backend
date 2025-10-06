from app.models import Sala
from app.extensions import db
from flask import abort

def list_salas():
    return [s.to_dict() for s in Sala.query.all()]

def create_sala(data):
    if not data.get("fechadura"):
        abort(400, "fechadura é obrigatória")
    sala = Sala(
        nome=data.get("nome"),
        codigo=data.get("codigo"),
        fechadura=data.get("fechadura"),
        local=data.get("local"),
        ativo=data.get("ativo", True),
    )
    db.session.add(sala)
    db.session.commit()
    return sala.to_dict()

def get_sala(sala_id):
    sala = Sala.query.get_or_404(sala_id)
    return sala.to_dict()

def update_sala(sala_id, data):
    sala = Sala.query.get_or_404(sala_id)
    for field in ["nome", "codigo", "fechadura", "local", "ativo"]:
        if field in data:
            setattr(sala, field, data[field])
    db.session.commit()
    return sala.to_dict()

def delete_sala(sala_id):
    sala = Sala.query.get_or_404(sala_id)
    db.session.delete(sala)
    db.session.commit()
    return {"message": "deletado"}
