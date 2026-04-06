# phola_park_app/user_routes.py
import os
from datetime import datetime, timedelta
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash,
    jsonify, current_app, abort
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from phola_park_app.extensions import db
from phola_park_app.model import (
    Report, Survey, Announcement,
    Notification, User
)
from phola_park_app.auth_helpers import role_required
from phola_park_app.forms.report_form import ReportForm

user_bp = Blueprint("user", __name__, url_prefix="/user")

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ─────────────────────────────────────────────
# USER DASHBOARD
# ─────────────────────────────────────────────
@user_bp.route("/dashboard")
@login_required
@role_required("user")
def dashboard():
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
        .filter_by(is_active=True)
        .order_by(Survey.created_at.desc())
        .all()
    )

    return render_template(
        "user/dashboard.html",
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
def submit_report():
    form = ReportForm()
    print("CSRF:", form.csrf_token.data)
    if form.validate_on_submit():
        flash("Submitting report...", "info")
        image_file = form.image.data
        filename = None

        if image_file:
            filename = secure_filename(image_file.filename)
            image_file.save(
                os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            )

        report = Report(
            report_type=form.report_type.data,
            category=form.category.data,
            description=form.description.data,
            portfolio=form.portfolio.data,
            image=filename,
            user_id=current_user.id
        )

        db.session.add(report)
        db.session.commit()

        flash("Report submitted successfully", "success")
        return redirect(url_for("user.user_reports"))

    return render_template("user_submit_report.html", form=form)


# ─────────────────────────────────────────────
# USER REPORTS (LIST + FILTER + EXPORT)
# ─────────────────────────────────────────────
@user_bp.route("/reports")
@login_required
@role_required("user")
def user_reports():
    reports = Report.query.filter(Report.user_id == current_user.id)

    q = request.args.get("q", "").strip()
    category = request.args.get("category")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    if q:
        reports = reports.filter(Report.description.ilike(f"%{q}%"))
        reports = reports.order_by(Report.created_at.desc()).all()
        filters = {"q": q, "category": category, "date_from": date_from, "date_to": date_to}
    if category:
        reports = reports.filter_by(category=category)

    if date_from:
        reports = reports.filter(Report.created_at >= datetime.strptime(date_from, "%Y-%m-%d"))

    if date_to:
        reports = reports.filter(
            Report.created_at < datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)
        )

    if request.args.get("export") == "csv":
        import csv, io
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerow(["ID", "Type", "Category", "Description", "Created At"])

        for r in reports:
            cw.writerow([r.id, r.report_type, r.category, r.description, r.created_at])

        return current_app.response_class(
            si.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=reports.csv"},
        )

    pagination = reports.order_by(Report.created_at.desc()).paginate(
        page=request.args.get("page", 1, type=int),
        per_page=10,
        error_out=False
    )

    return render_template(
        "user.user_reports.html",
        reports=pagination.items,
        pagination=pagination,
        filters=filters if q else {}
    )


# ─────────────────────────────────────────────
# SURVEYS
# ─────────────────────────────────────────────
@user_bp.route("/surveys")
@login_required
@role_required("user")
def surveys():
    surveys = Survey.query.order_by(Survey.created_at.desc()).all()

    return render_template("user/surveys.html", surveys=surveys)


@user_bp.route("/surveys/<int:survey_id>/submit", methods=["POST"])
@login_required
@role_required("user")
def submit_survey(survey_id):
    from phola_park_app.model import SurveyResponse, SurveyAnswer
    from phola_park_app.notifications import notify_survey_submission

    survey = Survey.query.get_or_404(survey_id)

    response = SurveyResponse(
        survey_id=survey.id,
        user_id=current_user.id
    )
    db.session.add(response)
    db.session.commit()

    for key, value in request.form.items():
        if key.startswith("q_"):
            db.session.add(
                SurveyAnswer(
                    response_id=response.id,
                    question_id=int(key[2:]),
                    value=value
                )
            )

    db.session.commit()
    notify_survey_submission(survey, current_user)

    flash("Survey submitted successfully.", "success")
    return redirect(url_for("user.dashboard"))


# ─────────────────────────────────────────────
# NOTICES
# ─────────────────────────────────────────────
@user_bp.route("/notices")
@login_required
@role_required("user")
def user_notices():
    notices = Announcement.query.order_by(
        Announcement.created_at.desc()
    ).all()

    return render_template("user/notices.html", notices=notices)


# ─────────────────────────────────────────────
# REPORT DETAIL (AJAX)
# ─────────────────────────────────────────────
@user_bp.route("/reports/<int:report_id>")
@login_required
def report_detail(report_id):
    report = Report.query.get_or_404(report_id)
    if report.user_id != current_user.id:
        abort(403)

    return jsonify(report.to_dict())


# ─────────────────────────────────────────────
# NOTIFICATIONS
# ─────────────────────────────────────────────
def notify_report_created(report):
    recipients = (
        User.query.filter_by(role="admin").all() +
        User.query.filter_by(role="supervisor", portfolio=report.portfolio).all()
    )

    for u in recipients:
        db.session.add(
            Notification(
                user_id=u.id,
                title="New Community Report",
                message=f"New {report.category} report submitted.",
                link=url_for("admin.report_detail", report_id=report.id)
            )
        )

    db.session.commit()
