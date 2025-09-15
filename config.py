import secrets
from datetime import timedelta

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:Pipoca.26@127.0.0.1:3306/aipo"
    JWT_SECRET_KEY = "sua_chave_super_secreta"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
