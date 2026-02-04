# phola_park_app/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from phola_park_app.extensions import db
from phola_park_app.model import User, UserRole
from functools import wraps
from flask import abort


auth_bp = Blueprint("auth", __name__)
#-------------------------
#--login management
#-----------------------------
from flask_login import LoginManager
from phola_park_app.model import User
from phola_park_app.forms import RegisterForm
from .auth_helpers import _redirect_by_role, redirect_by_role
login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)

            # Role-based redirect (CRITICAL)
            if user.role.name == "admin":
                return redirect(url_for("admin.admin_dashboard"))

            elif user.role.name == "supervisor":
                return redirect(url_for("supervisor.dashboard"))

            else:
                return redirect(url_for("user.dashboard"))

        flash("Invalid email or password", "danger")

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("auth.login"))


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def setup_defaults():
	# Create roles if they do not exist
	roles = ["admin", "supervisor", "user"]

	for r in roles:
		role = UserRole.query.filter_by(name=r).first()
		if not role:
			role = UserRole(name=r)
			db.session.add(role)

	db.session.commit()

	# Create default admin
	admin_role = UserRole.query.filter_by(name="admin").first()

	admin = User.query.filter_by(email="admin@test.com").first()
	if not admin:
		admin = User(
			name="System Admin",
			email="admin@test.com",
			role_id=admin_role.id,
			role=admin_role
		)
		admin.set_password("admin123")
		db.session.add(admin)
		db.session.commit()


# ─────────────────────────────────────────────
# ROLE DECORATORS
# ─────────────────────────────────────────────

def admin_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if not current_user.is_authenticated or current_user.role.name != "admin":
			abort(403)
		return f(*args, **kwargs)
	return decorated


def supervisor_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if not current_user.is_authenticated or current_user.role.name != "supervisor":
			abort(403)
		return f(*args, **kwargs)
	return decorated

# ─────────────────────────────────────────────
# ERROR HANDLER
# ─────────────────────────────────────────────

@auth_bp.errorhandler(403)
def forbidden(e):
	return render_template("403.html"), 403

# ─────────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────────
from flask import render_template, redirect, url_for, flash
from .forms import RegisterForm, LoginForm
from phola_park_app.extensions import db
from phola_park_app.model import User, UserRole
from flask_login import login_user


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		user_role = UserRole.query.filter_by(name="user").first()

		if not user_role:
			flash("User role not found. Contact admin.", "danger")
			return redirect(url_for("auth.register"))

		user = User(
			name=form.full_name.data,
			email=form.email.data,
			role=user_role
		)
		user.set_password(form.password.data)

		db.session.add(user)
		db.session.commit()

		flash("Account created successfully. Please login.", "success")
		return redirect(url_for("auth.login"))

	return render_template("register.html", form=form)
# ─────────────────────────────────────────────
# ADMIN CREATE USER (POST)
# ─────────────────────────────────────────────

@auth_bp.route("/create_user", methods=["POST"])
@login_required
@admin_required
def create_user():
	name = request.form.get("name", "").strip()
	email = request.form.get("email", "").lower().strip()
	password = request.form.get("password", "")
	role_name = request.form.get("role", "user")
	portfolio = request.form.get("portfolio")

	if not name or not email or not password:
		flash("All fields are required.", "warning")
		return redirect(url_for("admin.admin_users"))

	if User.query.filter_by(email=email).first():
		flash("Email already exists.", "danger")
		return redirect(url_for("admin.admin_users"))

	role_obj = UserRole.query.filter_by(name=role_name).first()
	if not role_obj:
		flash("Invalid role.", "danger")
		return redirect(url_for("admin.admin_users"))

	user = User(
		name=name,
		email=email,
		role_id=role_obj.id,
		portfolio=portfolio if role_name == "supervisor" else None,
	)
	user.set_password(password)

	db.session.add(user)
	db.session.commit()

	flash("User created successfully.", "success")
	return redirect(url_for("admin.admin_users"))
