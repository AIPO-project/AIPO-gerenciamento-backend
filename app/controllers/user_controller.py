from app.models import Usuario, Acesso
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
    user = Usuario.query.filter_by(matricula=user_id).first_or_404()
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
# --- SALAS ---
def get_user_salas(matricula):
    user = Usuario.query.filter_by(matricula=matricula).first()
    if not user:
        abort(404, "Usuário não encontrado")

    salas = []
    for autorizacao in user.autorizacoes:
        if autorizacao.sala:  # verifica se o relacionamento está carregado
            salas.append({
                "id": autorizacao.sala.id,
                "nome": autorizacao.sala.nome,
                "codigo": autorizacao.sala.codigo,
                "local": autorizacao.sala.local,
            })

    return {"usuario": user.nome, "matricula": user.matricula, "salas": salas}

# --- ACESSOS ---
def get_user_acessos(matricula, limite=5):
    user = Usuario.query.filter_by(matricula=matricula).first()
    if not user:
        abort(404, "Usuário não encontrado")

    # Busca os últimos 'limite' acessos, ordenando do mais recente pro mais antigo
    acessos_query = (
        Acesso.query
        .filter_by(usuario=matricula)
        .order_by(Acesso.timestamp.desc())
        .limit(limite)
        .all()
    )

    acessos = []
    for acesso in acessos_query:
        acessos.append({
            "sala": acesso.sala_rel.nome if acesso.sala_rel else None,
            "local": acesso.sala_rel.local if acesso.sala_rel else None,
            "horario": acesso.timestamp.strftime("%d/%m/%Y %H:%M:%S") if acesso.timestamp else None,
            "autorizado": acesso.autorizado
        })

    return {
        "usuario": user.nome,
        "matricula": user.matricula,
        "acessos": acessos
    }
