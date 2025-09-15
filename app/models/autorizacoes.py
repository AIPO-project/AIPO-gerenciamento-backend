from __future__ import annotations
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so

class Autorizacao(db.Model):
    __tablename__ = 'autorizacao'

    id: so.Mapped[int] = so.mapped_column(sa.BigInteger, primary_key=True, autoincrement=True)
    id_usuario: so.Mapped[int] = so.mapped_column(sa.ForeignKey('usuarios.id'), nullable=False)
    id_sala: so.Mapped[int] = so.mapped_column(sa.ForeignKey('salas.id'), nullable=False)

    usuario: so.Mapped["Usuario"] = so.relationship("Usuario", back_populates="autorizacoes")
    sala: so.Mapped["Sala"] = so.relationship("Sala", back_populates="autorizacoes")