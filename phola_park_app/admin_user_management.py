from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, role_required
from phola_park_app.extensions import db
from phola_park_app.model import User, UserRole, Report, Announcement
from phola_park_app.forms import CreateUserForm

admin_manage_bp = Blueprint("admin_manage", __name__, url_prefix="/admin/manage")

# ---------- Admin-only guard ----------
def admin_only():
    return current_user.is_authenticated and current_user.role == "admin"

# ---------- Admin Home ----------
@admin_manage_bp.route("/")
@login_required
@role_required("admin")
def home():
    if not admin_only():
        return "Unauthorized", 401
    return render_template("admin_dp_home.html")

# ---------- View all users ----------
@admin_manage_bp.route("/users")
@login_required
@role_required("admin")
def users_list():
    if not admin_only():
        return "Unauthorized", 401

    users = User.query.all()
    roles = UserRole.query.all()
    roles_map = {}
    for user in users:
        roles = UserRole.query.filter_by(user_id=user.id).all()
        roles_map[user.id] = roles
    return render_template("admin_manage_users.html", users=users, roles_map=roles_map)

# ---------- Assign role ----------
@admin_manage_bp.route("/assign-role", methods=["POST"])
@login_required
@role_required("admin")
def assign_role():
    if not admin_only():
        return "Unauthorized", 401

    user_id = request.form.get("user_id")
    role = request.form.get("role")
    portfolio = request.form.get("portfolio")

    new_role = UserRole(user_id=user_id, role=role, portfolio=portfolio)
    db.session.add(new_role)
    db.session.commit()

    flash("Role assigned!")
    return redirect(url_for("admin_manage.users_list"))

# ---------- Remove role ----------
@admin_manage_bp.route("/remove-role/<int:role_id>")
@login_required
@role_required("admin")
def remove_role(role_id):
    if not admin_only():
        return "Unauthorized", 401

    role = UserRole.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()

    return redirect(url_for("admin_manage.users_list"))

#--------------notices---------
@admin_manage_bp.route("/notices")
@login_required
@role_required("admin")
def manage_notices():
    return render_template("admin_manage_notices.html")
   
#--------------reports---------
@admin_manage_bp.route("/reports")
@login_required
@role_required("admin")
def reports():
    
    return render_template("admin_manage_reports.html")
#--------------announcement---------
@admin_manage_bp.route("/announcement")
@login_required
@role_required("admin")
def announcement():
    return render_template("admin_announcement.html")

#--------------export all data---------
@admin_manage_bp.route("/export-all-data")
@login_required
@role_required("admin")
def export_all_data():
    return render_template("admin_export_data.html")

@admin_manage_bp.route("/users/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create_user():
    form = CreateUserForm()

    if form.validate_on_submit():
        role = UserRole.query.filter_by(name=form.role.data).first()

        user = User(
            name=form.name.data,
            email=form.email.data,
            role=role,
            is_active=True
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("User created successfully", "success")
        return redirect(url_for("admin.users"))

    return render_template("admin/create_user.html", form=form)
