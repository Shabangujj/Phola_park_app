from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from phola_park_app.extensions import db
from phola_park_app.model import User, UserRole
from flask_login import login_required, login_user, logout_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # =========================
    # 📄 LOAD LOGIN PAGE
    # =========================
    if request.method == "GET":
        return render_template("login.html")

    # =========================
    # 📥 DETECT REQUEST TYPE
    # =========================
    if request.is_json:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        api_request = True
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        api_request = False

    # =========================
    # ⚠️ VALIDATE INPUT
    # =========================
    if not email or not password:
        message = "Email and password required"
        if api_request:
            return jsonify({"error": message}), 400
        flash(message, "danger")
        return redirect(url_for("auth.login"))

    # =========================
    # 🔍 FIND USER
    # =========================
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        message = "Invalid email or password"
        if api_request:
            return jsonify({"error": message}), 401
        flash(message, "danger")
        return redirect(url_for("auth.login"))

    # =========================
    # ✅ SAFE ROLE HANDLING
    # =========================
    role = user.role.name.lower() if user.role else "user"

    # =========================
    # 🔐 SAVE SESSION (CRITICAL)
    # =========================
    session["user_id"] = user.id
    session["role"] = user.role.name.lower() if user.role else "user"
    session["portfolio"] = getattr(user, "portfolio", None)

    print("SESSION SAVED:", session)

    # =========================
    # � LOGIN USER
    # =========================
    login_user(user)

    # =========================
    # 🔁 API RESPONSE
    # =========================
    if api_request:
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "role": role
            }
        }), 200

    # =========================
    # 🚀 ROLE-BASED REDIRECT
    # =========================
    if role == "admin":
        return redirect(url_for("admin.dashboard"))

    elif role == "supervisor":
        return redirect(url_for("supervisor.dashboard"))

    else:
        return redirect(url_for("web.user_dashboard"))


# =========================
# 📝 REGISTER
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All fields are required")
            return redirect(url_for("auth.register"))

        # Check if exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered")
            return redirect(url_for("auth.register"))

        # Hash password
        hashed_pw = generate_password_hash(password)

        # Get default role
        role = UserRole.query.filter_by(name="user").first()

        if not role:
            flash("Default role not configured")
            return redirect(url_for("auth.register"))

        # Create user
        new_user = User(
            username=name,
            email=email,
            password_hash=hashed_pw,
            role_id=role.id
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# =========================
# 🚪 LOGOUT
# =========================
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for("auth.login"))