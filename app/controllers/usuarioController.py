from app import db
import sqlalchemy as sa
from app.models import Usuario

class UsuarioController:

    @staticmethod
    def listar_usuarios():
        query = sa.select(Usuario)
        usuarios = db.session.scalars(query).all() 
        return usuarios

    @staticmethod
    def buscar_por_matricula(matricula):
        query = sa.select(Usuario).where(Usuario.matricula == matricula)
        usuario = db.session.scalars(query).first()
        return usuario

    @staticmethod
    def atualizar_usuario(matricula, usuario_atualizado):
        usuario = UsuarioController.buscar_por_matricula(matricula)
        if not usuario:
            raise Exception("Usuário não encontrado")

        usuario.nome = usuario_atualizado.nome
        usuario.chave = usuario_atualizado.chave

        db.session.commit()