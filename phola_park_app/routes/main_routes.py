import os
from datetime import datetime

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash,
    current_app, abort
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from phola_park_app.extensions import db
from phola_park_app.model import (
    Report, Notification, Announcement, User, UserRole, Project
)
from phola_park_app.utils.navigation import home_url
from phola_park_app.decorators import role_required

# ─────────────────────────────────────
# BLUEPRINT (DECLARE ONCE)
# ─────────────────────────────────────
main_bp = Blueprint("main", __name__,url_prefix="/api/v1")
from flask import Blueprint, jsonify
@main_bp.route("/")
def home():
    return jsonify({
        "status": "running",
        "message": "Phola Park API is working",
        "version": "v1"
    })
@main_bp.route("/dashboard")
@login_required
def dashboard():
    role = current_user.role.name

    if role == "admin":
        return render_template("admin_dashboard.html")

    elif role == "supervisor":
        return render_template("supervisor_dashboard.html")

    return render_template("user_dashboard.html")
# ─────────────────────────────────────
# test user
# _____________________________________
@main_bp.route("/test-auth")
@login_required
def test_auth():
    return f"""
    Logged in: {current_user.is_authenticated}<br>
    User: {current_user.username}<br>
    Role: {current_user.role.name}
    """

# ─────────────────────────────────────
# FILE UPLOAD SETTINGS
# ─────────────────────────────────────
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ─────────────────────────────────────
# LANDING PAGE
# ─────────────────────────────────────
@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    return render_template("index.html")

# ─────────────────────────────────────
# ROLE-AWARE HOME REDIRECT
# ─────────────────────────────────────
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # type: ignore[import]

@main_bp.route("/protected")
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    claims = get_jwt()

    return jsonify({
        "message": "Access granted",
        "user_id": user_id,
        "role": claims["role"],
        "username": claims["username"]
    })

# ─────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────
@main_bp.route("/admin/dashboard")
@login_required
@role_required("admin")
def admin_dashboard():
    stats = {
        "reports": Report.query.count(),
        "announcements": Announcement.query.count(),
        "notifications": Notification.query.count()
    }

    return render_template(
        "admin_dashboard.html",
        stats=stats
    )

# ─────────────────────────────────────
# SUPERVISOR DASHBOARD
# ─────────────────────────────────────
@main_bp.route("/supervisor/dashboard")
@login_required
@role_required("supervisor")
def supervisor_dashboard():
    stats = {
        "reports": Report.query.count(),
        "notifications": Notification.query.count()
    }

    reports = Report.query.order_by(Report.created_at.desc()).all()

    notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).all()

    return render_template(
        "supervisor_dashboard.html",
        stats=stats,
        reports=reports,
        notifications=notifications
    )

# ─────────────────────────────────────
# USER DASHBOARD
# ─────────────────────────────────────
@main_bp.route("/user/dashboard")
@login_required
@role_required
def user_dashboard():
    return render_template(
        "user_dashboard.html",
        user=current_user
    )

# ─────────────────────────────────────
# USER NOTICES / ANNOUNCEMENTS
# ─────────────────────────────────────
@main_bp.route("/notices")
@login_required
@role_required("user")
def user_notices():
    notices = (
        Announcement.query
        .filter_by(is_active=True)
        .order_by(Announcement.created_at.desc())
        .all()
    )
    return render_template("user_notices.html", notices=notices)

# ─────────────────────────────────────
# SUBMIT REPORT (USER)
# ─────────────────────────────────────
@main_bp.route("/submit-report", methods=["POST"])
@login_required
@role_required("user")
def submit_report():
    category = request.form.get("category")
    description = request.form.get("description")
    image_file = request.files.get("image")

    if not category or not description:
        flash("Category and description are required.", "danger")
        return redirect(url_for("main.user_dashboard"))

    image_filename = None

    if image_file and image_file.filename:
        if not allowed_file(image_file.filename):
            flash("Invalid image type.", "danger")
            return redirect(url_for("main.user_dashboard"))

        filename = secure_filename(image_file.filename)

        upload_path = os.path.join(
            current_app.static_folder,
            "uploads/reports"
        )
        os.makedirs(upload_path, exist_ok=True)

        image_file.save(os.path.join(upload_path, filename))
        image_filename = f"uploads/reports/{filename}"

    report = Report(
        report_type="User Report",
        description=description,
        category=category,
        image=image_filename,
        user_id=current_user.id,
        created_at=datetime.utcnow()
    )

    db.session.add(report)
    db.session.commit()

    flash("Report submitted successfully ✔", "success")
    return redirect(url_for("main.user_dashboard"))

# ─────────────────────────────────────
# USER NOTIFICATIONS PAGE
# ─────────────────────────────────────
@main_bp.route("/notifications")
@login_required
def notifications_page():
    notifications = (
        Notification.query
        .filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    return render_template(
        "notifications.html",
        notifications=notifications
    )
@main_bp.route("/")
def portfolio():
    projects = Project.query.all()
    return render_template("portfolio.html", projects=projects)