# phola_park_app/extensions.py
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask import jsonify

db = SQLAlchemy()
migrate = Migrate()  
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Redirect to this route if not logged in
jwt = JWTManager()  

@jwt.unauthorized_loader
def jwt_missing_token(reason):
    return jsonify({
        "error": "Unauthorized",
        "message": "Authorization token is missing"
    }), 401

@jwt.invalid_token_loader
def jwt_invalid_token(reason):
    return jsonify({
        "error": "Unauthorized",
        "message": "Invalid token"
    }), 401

@jwt.expired_token_loader
def jwt_expired_token(jwt_header, jwt_payload):
    return jsonify({
        "error": "Unauthorized",
        "message": "Token has expired"
    }), 401

@jwt.needs_fresh_token_loader
def jwt_fresh_token_required(jwt_header, jwt_payload):
    return jsonify({
        "error": "Unauthorized",
        "message": "Fresh token required"
    }), 401

@jwt.revoked_token_loader
def jwt_revoked_token(jwt_header, jwt_payload):
    return jsonify({
        "error": "Unauthorized",
        "message": "Token has been revoked"
    }), 401
