# phola_park_app/routes.py
import os
from datetime import datetime
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, jsonify, current_app
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from phola_park_app.extensions import db
from phola_park_app.model import Report, Survey, Announcement
from phola_park_app.auth_helpers import role_required
from flask import abort
# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


# ─────────────────────────────
# MAIN / PUBLIC
# ─────────────────────────────
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

# ─────────────────────────────────────────────
# USER ROUTES
# ─────────────────────────────────────────────
user_bp = Blueprint("user", __name__, url_prefix="/user")

@main_bp.route("/dashboard")
@login_required
def user_dashboard():
    if current_user.role != "user":
        abort(403)

    reports_count = Report.query.filter_by(user_id=current_user.id).count()

    recent_reports = (
        Report.query
        .filter_by(user_id=current_user.id)
        .order_by(Report.created_at.desc())
        .limit(5)
        .all()
    )

    notices = (
        Announcement.query
        .filter(
            (Announcement.target == "all") |
            (Announcement.target == current_user.portfolio)
        )
        .order_by(Announcement.created_at.desc())
        .limit(5)
        .all()
    )

    active_surveys = (
        Survey.query
        .filter_by(active=True)
        .order_by(Survey.created_at.desc())
        .all()
    )

    return render_template(
        "user_dashboard.html",
        reports_count=reports_count,
        recent_reports=recent_reports,
        notices=notices,
        active_surveys=active_surveys,
    )


# ─────────────────────────────────────────────
# SUBMIT REPORT
# ─────────────────────────────────────────────
@user_bp.route("/reports/submit", methods=["GET", "POST"])
@login_required
@role_required("user")
def submit_report():
    if request.method == "POST":
        report_type = request.form.get("report_type")
        category = request.form.get("category")
        description = request.form.get("description")
        survey_type = request.form.get("survey_type")

        image_file = request.files.get("image")
        filename = None

        if image_file and image_file.filename:
            if not allowed_file(image_file.filename):
                flash("Invalid image type.", "danger")
                return redirect(url_for("user.submit_report"))

            timestamp = int(datetime.utcnow().timestamp())
            safe_name = secure_filename(image_file.filename)
            filename = f"{timestamp}_{safe_name}"

            upload_dir = os.path.join(current_app.static_folder, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            image_file.save(os.path.join(upload_dir, filename))

        report = Report(
            report_type=report_type,
            category=category,
            description=description,
            survey_type=survey_type,
            portfolio=current_user.portfolio,
            image=filename,
            user_id=current_user.id,
            created_at=datetime.utcnow(),
        )

        db.session.add(report)
        db.session.commit()

        flash("Report submitted successfully.", "success")
        return redirect(url_for("user.reports"))

    categories = ["Water", "Electricity", "Housing", "Crime", "Health", "Waste"]
    survey_types = ["Survey 1", "Survey 2", "Survey 3"]

    return render_template(
        "user/submit_report.html",
        categories=categories,
        survey_types=survey_types,
    )


# ─────────────────────────────────────────────
# USER REPORTS
# ─────────────────────────────────────────────
@user_bp.route("/reports")
@login_required
@role_required("user")
def reports():
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", "")
    category = request.args.get("category")

    query = Report.query.filter_by(user_id=current_user.id)

    if q:
        query = query.filter(Report.description.ilike(f"%{q}%"))
    if category:
        query = query.filter_by(category=category)

    pagination = query.order_by(Report.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template(
        "user/reports.html",
        reports=pagination.items,
        pagination=pagination,
        filters=request.args,
    )


# ─────────────────────────────────────────────
# REPORT DETAIL (AJAX)
# ─────────────────────────────────────────────
@user_bp.route("/reports/<int:report_id>")
@login_required
@role_required("user")
def report_detail(report_id):
    r = Report.query.get_or_404(report_id)

    if r.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    image_url = (
        url_for("static", filename=f"uploads/{r.image}")
        if r.image else None
    )

    return jsonify({
        "id": r.id,
        "report_type": r.report_type,
        "category": r.category,
        "description": r.description,
        "survey_type": r.survey_type,
        "created_at": r.created_at.strftime("%Y-%m-%d %H:%M"),
        "comment": r.comment,
        "image_url": image_url,
    })


# ─────────────────────────────────────────────
# SURVEYS
# ─────────────────────────────────────────────
@user_bp.route("/surveys")
@login_required
@role_required("user")
def surveys():
    surveys = Survey.query.filter_by(active=True).all()
    return render_template("user/surveys.html", surveys=surveys)


# ─────────────────────────────────────────────
# NOTICES
# ─────────────────────────────────────────────
@user_bp.route("/notices")
@login_required
@role_required("user")
def notices():
    notices = Announcement.query.filter(
        (Announcement.target == "all") |
        (Announcement.target == current_user.portfolio)
    ).order_by(Announcement.created_at.desc()).all()

    return render_template("user/notices.html", notices=notices)
# ─────────────────────────────
# ADMIN
# ─────────────────────────────
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    if current_user.role != "admin":
        abort(403)
    return render_template("admin_dashboard.html")
# ─────────────────────────────
# SUPERVISOR
# ─────────────────────────────
supervisor_bp = Blueprint("supervisor", __name__, url_prefix="/supervisor")

@supervisor_bp.route("/dashboard")
@login_required
@role_required("supervisor")
def dashboard():
    if current_user.role != "supervisor":
        abort(403)
    return render_template("supervisor_dashboard.html")

@main_bp.route("/user/reports")
@login_required
def user_reports():
    filters = {
        "q": request.args.get("q", "")
    }

    reports = Report.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "user/user_reports.html",
        reports=reports,
        filters=filters
    )
@main_bp.route("/announcements")
@login_required
def announcements():
    query = Announcement.query

    query = query.filter(
        (Announcement.target_role.name == None) |
        (Announcement.target_role.name == current_user.role.name)
    )

    if current_user.portfolio:
        query = query.filter(
            (Announcement.portfolio == None) |
            (Announcement.portfolio == current_user.portfolio)
        )

    announcements = query.order_by(
        Announcement.created_at.desc()
    ).all()

    return render_template(
        "announcements.html",
        announcements=announcements
    )
