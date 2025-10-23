from .extensions import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=False)
    matricula = db.Column(db.String(45), nullable=False, unique=True)
    tipoUsuario = db.Column(db.String(45))
    nivelGerencia = db.Column(db.String(45))
    chave = db.Column(db.String(45), unique=True)
    ativo = db.Column(db.Boolean, default=True)
    foto = db.Column(db.String(255))

    # Relacionamentos
    autorizacoes = db.relationship("Autorizacao", back_populates="usuario", cascade="all, delete-orphan")
    acessos = db.relationship("Acesso", back_populates="usuario_rel", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "matricula": self.matricula,
            "tipoUsuario": self.tipoUsuario,
            "nivelGerencia": self.nivelGerencia,
            "chave": self.chave,
            "ativo": self.ativo,
            "foto": self.foto,
        }


class Sala(db.Model):
    __tablename__ = "salas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45))
    codigo = db.Column(db.String(45))
    fechadura = db.Column(db.String(45), nullable=False, unique=True)
    local = db.Column(db.String(45))
    ativo = db.Column(db.Boolean, default=True)
    

    # Relacionamentos
    autorizacoes = db.relationship("Autorizacao", back_populates="sala", cascade="all, delete-orphan")
    acessos = db.relationship("Acesso", back_populates="sala_rel", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "codigo": self.codigo,
            "fechadura": self.fechadura,
            "local": self.local,
            "ativo": self.ativo,
        }


class Autorizacao(db.Model):
    __tablename__ = "autorizacao"

    id = db.Column(db.BigInteger, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    id_sala = db.Column(db.Integer, db.ForeignKey("salas.id", ondelete="CASCADE"), nullable=False)

    # Relacionamentos
    usuario = db.relationship("Usuario", back_populates="autorizacoes")
    sala = db.relationship("Sala", back_populates="autorizacoes")

    def to_dict(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "id_sala": self.id_sala,
        }


class Acesso(db.Model):
    __tablename__ = "acessos"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(45), db.ForeignKey("usuarios.matricula", onupdate="CASCADE"), nullable=False)
    sala = db.Column(db.Integer, db.ForeignKey("salas.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    autorizado = db.Column(db.Boolean, nullable=False, default=False)

    # Relacionamentos
    usuario_rel = db.relationship("Usuario", back_populates="acessos", foreign_keys=[usuario])
    sala_rel = db.relationship("Sala", back_populates="acessos")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "sala": self.sala,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "autorizado": self.autorizado,
        }
