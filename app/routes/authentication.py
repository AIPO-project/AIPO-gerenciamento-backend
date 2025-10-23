from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.authenticationController import AuthenticationController

authentication_bp = Blueprint("authentication_bp", __name__)

authentication_bp.route("/login", methods=["POST"])(AuthenticationController.login)
authentication_bp.route("/protected", methods=["GET"])(AuthenticationController.protected)
