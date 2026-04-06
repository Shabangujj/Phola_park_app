from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, render_template, redirect, url_for, flash
from phola_park_app.extensions import db
from phola_park_app.model import User, UserRole
from flask_login import current_user, login_required, login_user, logout_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles:
    ✔ Show login page (GET)
    ✔ Browser form login (POST form)
    ✔ API login (POST JSON)
    """

    # ✅ SHOW LOGIN PAGE
    if request.method == "GET":
        return render_template("login.html")

    # ===============================
    # DETERMINE REQUEST TYPE
    # ===============================
    if request.is_json:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        api_request = True
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        api_request = False

    # ✅ Validate input
    if not email or not password:
        message = "Email and password required"
        if api_request:
            return jsonify({"error": message}), 400
        flash(message)
        return redirect(url_for("auth.login"))

    # ✅ Find user
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        message = "Invalid email or password"
        if api_request:
            return jsonify({"error": message}), 401
        flash(message)
        return redirect(url_for("auth.login"))

    # ✅ Create session login (for dashboard)
    login_user(user)
    if user.role == "admin":
                return redirect(url_for("admin.admin_dashboard"))

    elif user.role == "supervisor":
                return redirect(url_for("supervisor.supervisor_dashboard"))

    else:
                return redirect(url_for("web.dashboard"))

    # ✅ Create JWT token (for API use)
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role.name if user.role else "user"
        }
    )

    # ===============================
    # RETURN RESPONSE
    # ===============================
    if api_request:
        return jsonify({
            "status": "success",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": getattr(user, "username", user.name),
                "email": user.email,
                "role": user.role.name if user.role else "user"
            }
        }), 200

    flash("Login successful")
    return redirect(url_for("web.dashboard"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered")
            return redirect(url_for("auth.register"))

        # hash password
        hashed_pw = generate_password_hash(password)
        # assign default role (assuming role_id=2 is "user")
        default_role_id = UserRole.query.filter_by(name="user").first().id
        # create user
        new_user = User(
            username=name,
            email=email,
            password_hash=hashed_pw,
            role_id=default_role_id  # assign default role 
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")
#--------------------------
#---------logout route
#--------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))