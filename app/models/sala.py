from __future__ import annotations
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional

from app.models.autorizacoes import Autorizacao

class Sala(db.Model):
    __tablename__ = 'salas'

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    nome: so.Mapped[Optional[str]] = so.mapped_column(sa.String(45))
    codigo: so.Mapped[Optional[str]] = so.mapped_column(sa.String(45))
    fechadura: so.Mapped[str] = so.mapped_column(sa.String(45), nullable=False, unique=True)
    local: so.Mapped[Optional[str]] = so.mapped_column(sa.String(45))
    ativo: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, server_default=sa.text("1"))
    
    autorizacoes: so.Mapped[list["Autorizacao"]] = so.relationship(back_populates="sala")
