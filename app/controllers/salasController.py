from app import db
import sqlalchemy as sa
from app.models import Sala, Usuario, Autorizacao

class SalasController:

    @staticmethod
    def listar_salas():
        query = sa.select(Sala)
        salas = db.session.scalars(query).all()
        return salas

    @staticmethod
    def buscar_por_codigo(codigo):
        query = sa.select(Sala).where(Sala.codigo == codigo)
        sala = db.session.scalars(query).first()
        return sala

    @staticmethod
    def atualizar_sala(codigo, sala_atualizada):
        sala = SalasController.buscar_por_codigo(codigo)
        if not sala:
            raise Exception("Sala não encontrada")

        sala.nome = sala_atualizada.nome
        sala.local = sala_atualizada.local

        db.session.commit()

    @staticmethod 
    def salas_do_usuario(matricula): 
        try: 
            query = ( sa.select(Sala) 
                    .join(Autorizacao, Sala.id == Autorizacao.id_sala) 
                    .join(Usuario, Usuario.id == Autorizacao.id_usuario) 
                    .where(Usuario.matricula == matricula) ) 
            return db.session.scalars(query).all() 
        except Exception as e: 
            return {"error": str(e)}, 500
