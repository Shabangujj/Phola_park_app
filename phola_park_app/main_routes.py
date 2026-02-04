import os
from datetime import datetime
from functools import wraps

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash,
    current_app, abort
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from phola_park_app.extensions import db
from phola_park_app.model import (
    Report, Notification, Announcement,
    User, UserRole
)
from phola_park_app.utils.navigation import home_url

# ─────────────────────────────────────
# BLUEPRINT (DECLARE ONCE)
# ─────────────────────────────────────
main_bp = Blueprint("main", __name__)

# ─────────────────────────────────────
# FILE UPLOAD HELPERS
# ─────────────────────────────────────
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ─────────────────────────────────────
# ROLE DECORATOR
# ─────────────────────────────────────
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if not current_user.role or current_user.role.name not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator

# ─────────────────────────────────────
# LANDING PAGE
# ─────────────────────────────────────
@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    return render_template("landing.html")

# ─────────────────────────────────────
# ROLE-AWARE HOME
# ─────────────────────────────────────
@main_bp.route("/home")
@login_required
def home():
    return redirect(home_url())

# ─────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────
@main_bp.route("/admin/dashboard")
@login_required
@role_required("admin")
def admin_dashboard():
    stats = {
        "users": User.query.count(),
        "supervisors": User.query.join(UserRole)
            .filter(UserRole.name == "supervisor")
            .count(),
        "reports": Report.query.count()
    }
    return render_template("admin_dashboard.html", stats=stats)

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
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
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
@role_required("user")
def user_dashboard():
    return render_template("user_dashboard.html", user=current_user)

# ─────────────────────────────────────
# USER NOTICES
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
# SUBMIT REPORT
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
            current_app.static_folder, "uploads/reports"
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
# NOTIFICATIONS
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
    return render_template("notifications.html", notifications=notifications)
