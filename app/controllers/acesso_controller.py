from app.models import Acesso, Usuario, Sala
from app.extensions import db
from flask import abort
from datetime import datetime

def list_acessos(filters=None):
    q = Acesso.query
    if filters:
        usuario = filters.get("usuario")
        sala = filters.get("sala")
        date_from = filters.get("date_from")
        date_to = filters.get("date_to")
        if usuario:
            q = q.filter_by(usuario=usuario)
        if sala is not None:
            try:
                q = q.filter_by(sala=int(sala))
            except ValueError:
                abort(400, "sala deve ser inteiro")
        if date_from:
            try:
                df = datetime.fromisoformat(date_from)
                q = q.filter(Acesso.timestamp >= df)
            except Exception:
                abort(400, "date_from deve ser ISO8601")
        if date_to:
            try:
                dt = datetime.fromisoformat(date_to)
                q = q.filter(Acesso.timestamp <= dt)
            except Exception:
                abort(400, "date_to deve ser ISO8601")
    return [a.to_dict() for a in q.all()]

def create_acesso(data):
    usuario = data.get("usuario")
    sala = data.get("sala")
    autorizado = data.get("autorizado", False)
    ts = data.get("timestamp")
    if not usuario or sala is None:
        abort(400, "usuario e sala são obrigatórios")
    if not Usuario.query.filter_by(matricula=usuario).first():
        abort(404, "usuario não encontrado")
    if not Sala.query.get(sala):
        abort(404, "sala não encontrada")
    if ts:
        try:
            timestamp = datetime.fromisoformat(ts)
        except Exception:
            abort(400, "timestamp deve ser ISO8601")
    else:
        timestamp = datetime.utcnow()
    acesso = Acesso(usuario=usuario, sala=sala, autorizado=bool(autorizado), timestamp=timestamp)
    db.session.add(acesso)
    db.session.commit()
    return acesso.to_dict()

def get_acesso(acesso_id):
    acesso = Acesso.query.get_or_404(acesso_id)
    return acesso.to_dict()

def delete_acesso(acesso_id):
    acesso = Acesso.query.get_or_404(acesso_id)
    db.session.delete(acesso)
    db.session.commit()
    return {"message": "deletado"}
