from __future__ import annotations
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional

from app.models.autorizacoes import Autorizacao

class Usuario(db.Model):
    __tablename__ = 'usuarios' 
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(45), nullable=False)
    matricula: so.Mapped[str] = so.mapped_column(sa.String(45), nullable=False, unique=True)
    tipoUsuario: so.Mapped[Optional[str]] = so.mapped_column(sa.String(45))
    nivelGerencia: so.Mapped[Optional[str]] = so.mapped_column(sa.String(45))
    chave: so.Mapped[Optional[str]] = so.mapped_column(sa.String(45), unique=True)
    ativo: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, server_default=sa.text("1"))
    
    autorizacoes: so.Mapped[list["Autorizacao"]] = so.relationship(back_populates="usuario")