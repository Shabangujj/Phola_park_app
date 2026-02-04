from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, Response
from flask_login import login_required, current_user
from phola_park_app.extensions import db
from phola_park_app.model import (
    User, Report, Notice, Announcement,
    UserRole, Survey, Notification
)
from phola_park_app.utils.permissions import role_required
import csv

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def create_announcement_notifications(announcement):
    """Create notifications for users based on role and/or portfolio."""
    users = User.query.all()

    for user in users:
        if announcement.target_role and user.role.name != announcement.target_role:
            continue

        if announcement.portfolio and user.portfolio != announcement.portfolio:
            continue

        notification = Notification(
            user_id=user.id,
            title=announcement.title,
            message=announcement.message
        )
        db.session.add(notification)

    db.session.commit()


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
@admin_bp.route("/")
@login_required
@role_required("admin")
def admin_home():
    return redirect(url_for("main.home"))


@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
def admin_dashboard():
    stats = {
        "users": User.query.count(),
        "supervisors": User.query.join(UserRole).filter(UserRole.name == "supervisor").count(),
        "reports": Report.query.count(),
        "surveys": Survey.query.count(),
    }

    recent_reports = (
        Report.query
        .order_by(Report.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin_dashboard.html",
        stats=stats,
        recent_reports=recent_reports
    )


# ─────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────
@admin_bp.route("/users")
@login_required
@role_required("admin")
def admin_users():
    users = User.query.join(UserRole).order_by(User.id.asc()).all()
    roles = UserRole.query.all()
    return render_template("admin_users.html", users=users, roles=roles)


@admin_bp.route("/users/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create_user():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").lower().strip()
        password = request.form.get("password", "")
        role_name = request.form.get("role", "user")
        portfolio = request.form.get("portfolio")

        if not name or not email or not password:
            flash("All fields are required.", "warning")
            return redirect(url_for("admin.create_user"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "danger")
            return redirect(url_for("admin.create_user"))

        role = UserRole.query.filter_by(name=role_name).first()
        if not role:
            abort(400)

        user = User(
            name=name,
            email=email,
            role_id=role.id,
            portfolio=portfolio if role_name == "supervisor" else None,
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("User created successfully.", "success")
        return redirect(url_for("admin.admin_users"))

    roles = UserRole.query.all()
    return render_template("admin_create_user.html", roles=roles)


@admin_bp.route("/users/<int:user_id>/role", methods=["POST"])
@login_required
@role_required("admin")
def change_user_role(user_id):
    user = User.query.get_or_404(user_id)
    role_id = request.form.get("role_id")

    role = UserRole.query.get(role_id)
    if not role:
        abort(400)

    user.role_id = role.id
    db.session.commit()

    flash("User role updated.", "success")
    return redirect(url_for("admin.admin_users"))


@admin_bp.route("/users/<int:user_id>/toggle")
@login_required
@role_required("admin")
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()

    flash("User status updated.", "info")
    return redirect(url_for("admin.admin_users"))


@admin_bp.route("/assign-portfolio/<int:user_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def assign_portfolio(user_id):
    user = User.query.get_or_404(user_id)

    if user.role.name != "supervisor":
        flash("Only supervisors can be assigned portfolios.", "warning")
        return redirect(url_for("admin.admin_users"))

    portfolios = ["Water", "Electricity", "Housing", "Roads", "Sanitation", "Health", "Safety"]

    if request.method == "POST":
        user.portfolio = request.form.get("portfolio")
        db.session.commit()
        flash("Portfolio assigned successfully.", "success")
        return redirect(url_for("admin.admin_users"))

    return render_template("admin_assign_portfolio.html", user=user, portfolios=portfolios)


# ─────────────────────────────────────────────
# REPORTS
# ─────────────────────────────────────────────
@admin_bp.route("/reports")
@login_required
@role_required("admin")
def admin_reports():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return render_template("admin_reports.html", reports=reports)


@admin_bp.route("/reports/export/csv")
@login_required
@role_required("admin")
def export_reports_csv():
    reports = Report.query.all()

    def generate():
        yield "ID,Category,Status,Created At\n"
        for r in reports:
            yield f"{r.id},{r.category},{r.status},{r.created_at}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=reports.csv"}
    )


# ─────────────────────────────────────────────
# NOTICES
# ─────────────────────────────────────────────
@admin_bp.route("/notices")
@login_required
@role_required("admin")
def notices():
    notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return render_template("admin_notices.html", notices=notices)


@admin_bp.route("/notices/delete/<int:notice_id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    db.session.delete(notice)
    db.session.commit()
    flash("Notice deleted.", "info")
    return redirect(url_for("admin.notices"))


# ─────────────────────────────────────────────
# ANNOUNCEMENTS
# ─────────────────────────────────────────────
@admin_bp.route("/announcements", methods=["GET", "POST"])
@login_required
@role_required("admin")
def admin_announcements():
    if request.method == "POST":
        ann = Announcement(
            title=request.form["title"],
            message=request.form["message"],
            target_role=request.form.get("target_role") or None,
            portfolio=request.form.get("portfolio") or None
        )
        db.session.add(ann)
        db.session.commit()

        create_announcement_notifications(ann)

        flash("Announcement published.", "success")
        return redirect(url_for("admin.admin_announcements"))

    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template("admin_announcements.html", announcements=announcements)


@admin_bp.route("/announcements/<int:id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_announcement(id):
    announcement = Announcement.query.get_or_404(id)

    if request.method == "POST":
        announcement.title = request.form["title"]
        announcement.message = request.form["message"]
        announcement.target_role = request.form.get("target_role") or None
        announcement.portfolio = request.form.get("portfolio") or None
        db.session.commit()

        flash("Announcement updated.", "success")
        return redirect(url_for("admin.admin_announcements"))

    return render_template("admin/edit_announcement.html", announcement=announcement)


@admin_bp.route("/announcements/<int:id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete_announcement(id):
    announcement = Announcement.query.get_or_404(id)
    db.session.delete(announcement)
    db.session.commit()
    flash("Announcement deleted.", "success")
    return redirect(url_for("admin.admin_announcements"))


# ─────────────────────────────────────────────
# DB TOOLS
# ─────────────────────────────────────────────
@admin_bp.route("/db-tools")
@login_required
@role_required("admin")
def db_tools():
    return render_template("admin_db_tools.html")
#-----------------------------------------
#-----admin surveys route added------
#-----------------------
@admin_bp.route("/surveys")
@login_required
@role_required("admin")
def admin_surveys():
    surveys = Survey.query.order_by(Survey.created_at.desc()).all()
    return render_template("admin_surveys.html", surveys=surveys)