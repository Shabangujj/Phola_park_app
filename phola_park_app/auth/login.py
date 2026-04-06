from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from phola_park_app.model import User

auth_api = Blueprint("auth_api", __name__, url_prefix="/auth")


@auth_api.route(
    "/login",
    methods=["POST"],
    endpoint="jwt_login_api"
)
def jwt_login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    role_name = user.role.name if user.role else "user"
    access_token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role_name}
    )

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role_name
        }
    })

