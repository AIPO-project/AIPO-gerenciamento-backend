from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate
from .routes.users import bp_users
from .routes.salas import bp_salas
from .routes.acessos import bp_acessos
from .routes.autorizacoes import bp_autorizacoes

def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # registra blueprints
    app.register_blueprint(bp_users, url_prefix="/api/v1")
    app.register_blueprint(bp_salas, url_prefix="/api/v1")
    app.register_blueprint(bp_acessos, url_prefix="/api/v1")
    app.register_blueprint(bp_autorizacoes, url_prefix="/api/v1")

    return app
