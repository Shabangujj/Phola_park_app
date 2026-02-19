from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta

from phola_park_app.model import User

auth_api = Blueprint("auth_api", __name__, url_prefix="/auth")
reports_api = Blueprint("reports_api", __name__, url_prefix="/reports")

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
    token = create_access_token(
        identity=user.id,
        additional_claims={"role": role_name},
        expires_delta=timedelta(days=1)
    )

    return jsonify({
        "access_token": token,
        "role": role_name
    })
@reports_api.route(
    "",
    methods=["POST"],
    endpoint="create_report_api"
)
@jwt_required()
def create_report():
    claims = get_jwt()
    if claims["role"] != "user":
        return jsonify({"error": "Forbidden"}), 403
    ...

from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

def jwt_role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify({"error": "Forbidden"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@jwt_required()
@jwt_role_required("admin", "supervisor")
def update_report_status(report_id):
    ...

