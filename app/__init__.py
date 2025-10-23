from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate, jwt
from .routes.users import bp_users
from .routes.salas import bp_salas
from .routes.acessos import bp_acessos
from .routes.autorizacoes import bp_autorizacoes
from app.routes.authentication import authentication_bp

def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    app.config["JWT_SECRET_KEY"] = "sua_chave_super_secreta"
    app.config["JSON_SORT_KEYS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    # registra blueprints
    app.register_blueprint(bp_users, url_prefix="/api/v1")
    app.register_blueprint(bp_salas, url_prefix="/api/v1")
    app.register_blueprint(bp_acessos, url_prefix="/api/v1")
    app.register_blueprint(bp_autorizacoes, url_prefix="/api/v1")
    app.register_blueprint(authentication_bp, url_prefix="/api/v1")
    return app
