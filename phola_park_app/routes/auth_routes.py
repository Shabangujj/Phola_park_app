from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from phola_park_app.extensions import db
from phola_park_app.models import User, UserRole
from phola_park_app.utils.audit import log_action

from flask_login import (
    login_required,
    login_user,
    logout_user,
    current_user
)
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
# 🔐 LOGIN USER
# =========================
    login_user(user)

    # =========================
    # 📝 AUDIT LOG
    # =========================
    try:
        log_action(
            user_id=user.id,
            action="LOGIN",
            module="AUTH",
            description=f"User {user.username} logged in successfully",
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
    except Exception as e:
        print("AUDIT LOG ERROR:", e)

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
        return redirect(url_for("user.user_dashboard"))


# =========================
# 📝 REGISTER / CREATE ACCOUNT
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # -------------------------
        # Get form data
        # -------------------------
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # -------------------------
        # Validate required fields
        # -------------------------
        if not full_name or not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("auth.register"))

        # -------------------------
        # Validate password length
        # -------------------------
        if len(password) < 8:
            flash(
                "Password must contain at least 8 characters.",
                "danger"
            )
            return redirect(url_for("auth.register"))

        # -------------------------
        # Confirm password
        # -------------------------
        if password != confirm_password:
            flash(
                "Passwords do not match.",
                "danger"
            )
            return redirect(url_for("auth.register"))

        # -------------------------
        # Check username
        # -------------------------
        existing_username = User.query.filter_by(
            username=username
        ).first()

        if existing_username:
            flash(
                "Username already exists.",
                "warning"
            )
            return redirect(url_for("auth.register"))

        # -------------------------
        # Check email
        # -------------------------
        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email:
            flash(
                "Email already registered.",
                "warning"
            )
            return redirect(url_for("auth.register"))

        # -------------------------
        # Get normal USER role
        # -------------------------
        role = UserRole.query.filter(
            db.func.lower(UserRole.name) == "user"
        ).first()

        if not role:
            flash(
                "Default User role is not configured. "
                "Please contact the administrator.",
                "danger"
            )
            return redirect(url_for("auth.register"))

        # -------------------------
        # Create user
        # -------------------------
        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
            role_id=role.id,
            is_active=True
        )

        # -------------------------
        # Secure password hash
        # -------------------------
        new_user.set_password(password)

        # -------------------------
        # Save user
        # -------------------------
        try:

            db.session.add(new_user)
            db.session.commit()

        except Exception as e:

            db.session.rollback()

            print("REGISTRATION ERROR:", e)

            flash(
                "Unable to create account. Please try again.",
                "danger"
            )

            return redirect(url_for("auth.register"))

        # -------------------------
        # Success
        # -------------------------
        flash(
            "Account created successfully. "
            "You can now log in.",
            "success"
        )

        return redirect(url_for("auth.login"))

    # GET request
    return render_template("register.html")

@auth_bp.route("/logout")
@login_required
def logout():

    user_id = current_user.id
    username = current_user.username

    try:
        log_action(
            user_id=user_id,
            action="LOGOUT",
            module="AUTH",
            description=f"User {username} logged out",
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
    except Exception as e:
        print("AUDIT LOG ERROR:", e)

    logout_user()

    flash("Logged out successfully")

    return redirect(url_for("auth.login"))