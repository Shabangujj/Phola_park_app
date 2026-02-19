from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from phola_park_app.model import User

auth_bp = Blueprint("api_auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)

    if not data:
        return jsonify({
            "error": "Bad Request",
            "message": "JSON body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Bad Request",
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "error": "Unauthorized",
            "message": "User not found"
        }), 401

    if not user.check_password(password):
        return jsonify({
            "error": "Unauthorized",
            "message": "Invalid password"
        }), 401
    access_token = create_access_token(
    identity=user.id,
    additional_claims={
        "role": user.role,
        "permissions": user.extra_permissions  # optional per-user overrides
    }
)
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }), 200
from flask_jwt_extended import jwt_required, get_jwt, jwt_role_required

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    claims = get_jwt()
    return {
        "message": "Protected route accessed",
        "role": claims.get("role")
    }, 200

@auth_bp.route("/profile", methods=["GET"])
@jwt_role_required("admin", "supervisor", "user")
def profile():
    return {"message": "Base access granted"}

@auth_bp.route("/admin/dashboard", methods=["GET"])
@jwt_role_required("admin")
def admin_dashboard():
    return {"message": "Admin access"}

@auth_bp.route("/supervisor/dashboard", methods=["GET"])
@jwt_role_required("supervisor")
def supervisor_dashboard():
    return {"message": "Supervisor access"}

@auth_bp.route("/user/dashboard", methods=["GET"])
@jwt_role_required("user")
def user_dashboard():
    return {"message": "User access"}