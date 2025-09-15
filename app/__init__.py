from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

# Cria app único
app = Flask(__name__)
app.config.from_object(Config)

# Extensões
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Importa rotas e models depois
from app import routes, models
