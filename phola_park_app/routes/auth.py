from flask import request, jsonify
from phola_park_app.extensions import db
from phola_park_app.model import User, UserRole
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, jsonify

auth = Blueprint("auth", __name__, url_prefix="/auth")
#-----------------------------
#--login
#-------------------------
from flask_jwt_extended import create_access_token

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role.name,
                "username": user.username
            }
        )

        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.name
            }
        }), 200

    return jsonify({"error": "Invalid email or password"}), 401

#--------------------------------
#---Register
#---------------------------------
@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Validate input
    if not data or not data.get("email") or not data.get("password") or not data.get("username"):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    # Get default role
    default_role = UserRole.query.filter_by(name="user").first()

    if not default_role:
        return jsonify({"error": "Default role not found. Run reset_database."}), 500

    user = User(
        username=data["username"],
        email=data["email"],
        role_id=default_role.id
    )

    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


#------------------
#---------logout
#--------------------
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})
#-----------------
#---Protected Route Test
#--------------------------
@auth.route("/profile")
@login_required
def profile():
    return jsonify({
        "username": current_user.username,
        "role": current_user.role
    })

