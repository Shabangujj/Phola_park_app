from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from datetime import datetime
from flask import Blueprint


from sqlalchemy import func

from phola_park_app.extensions import db
from phola_park_app.model import Survey, Report, User, Announcement
from phola_park_app.utils.permissions import role_required
from collections import Counter

supervisor_bp = Blueprint('supervisor', __name__, url_prefix='/supervisor')
@supervisor_bp.route("/dashboard")
def supervisor_dashboard():

    # 🔒 Ensure only supervisors access
    if session.get("role") != "supervisor":
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    # ✅ Filter reports by supervisor portfolio
    reports = Report.query.filter_by(portfolio=user.portfolio).all()

    return render_template(
        "supervisor/dashboard.html",
        reports=reports,
        portfolio=user.portfolio
    )
@supervisor_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'supervisor':
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    user = User.query.get(session[user_id]).portfolio

    if not user or not user.portfolio:
        return "No portfolio assigned", 403

    # 🔥 FILTER BY PORTFOLIO
    reports = Report.query.filter_by(portfolio=user.portfolio).all()

    announcements = Announcement.query.filter_by(
        portfolio=user.portfolio
    ).order_by(Announcement.created_at.desc()).all()

    # 📊 STATS
    total_reports = len(reports)

    category_counts = Counter([r.category for r in reports])

    return render_template(
        'supervisor/dashboard.html',
        reports=reports,
        announcements=announcements,
        total_reports=total_reports,
        category_counts=category_counts,
        portfolio=user.portfolio
    )


# ─────────────────────────────────────────────
# VIEW REPORTS
# ─────────────────────────────────────────────
@supervisor_bp.route("/reports")
@login_required
@role_required("supervisor")
def reports():
    portfolio = current_user.portfolio

    status = request.args.get("status", "all")
    keyword = request.args.get("keyword", "")
    start = request.args.get("start_date")
    end = request.args.get("end_date")

    query = Report.query.filter_by(portfolio=portfolio)

    if status != "all":
        query = query.filter_by(status=status)

    if keyword:
        query = query.filter(Report.description.ilike(f"%{keyword}%"))

    if start:
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            query = query.filter(Report.created_at >= start_date)
        except ValueError:
            flash("Invalid start date", "warning")

    if end:
        try:
            end_date = datetime.strptime(end, "%Y-%m-%d")
            query = query.filter(Report.created_at <= end_date)
        except ValueError:
            flash("Invalid end date", "warning")

    reports = query.order_by(Report.created_at.desc()).all()

    return render_template(
        "supervisor.reports.html",
        reports=reports,
        status=status,
        keyword=keyword,
        start=start,
        end=end,
        portfolio=portfolio,
    )


# ─────────────────────────────────────────────
# REPORT DETAIL
# ─────────────────────────────────────────────
@supervisor_bp.route("/reports/<int:report_id>")
@login_required
@role_required("supervisor")
def report_detail(report_id):
    report = Report.query.get_or_404(report_id)

    if report.portfolio != current_user.portfolio:
        flash("Unauthorized access to this report.", "danger")
        return redirect(url_for("supervisor.reports"))

    return render_template(
        "supervisor/report_detail.html",
        report=report
    )


# ─────────────────────────────────────────────
# UPDATE REPORT STATUS
# ─────────────────────────────────────────────
@supervisor_bp.route("/reports/<int:report_id>/status", methods=["POST"])
@login_required
@role_required("supervisor")
def update_status(report_id):
    report = Report.query.get_or_404(report_id)

    if report.portfolio != current_user.portfolio:
        flash("Permission denied.", "danger")
        return redirect(url_for("supervisor.reports"))

    new_status = request.form.get("status")

    if new_status not in {"Pending", "In Progress", "Completed", "Rejected"}:
        flash("Invalid status.", "danger")
        return redirect(url_for("supervisor.report_detail", report_id=report.id))

    report.status = new_status
    db.session.commit()

    flash("Report status updated.", "success")
    return redirect(url_for("supervisor.report_detail", report_id=report.id))


# ─────────────────────────────────────────────
# ADD COMMENT
# ─────────────────────────────────────────────
@supervisor_bp.route("/reports/<int:report_id>/comment", methods=["POST"])
@login_required
@role_required("supervisor")
def add_comment(report_id):
    report = Report.query.get_or_404(report_id)

    if report.portfolio != current_user.portfolio:
        flash("Permission denied.", "danger")
        return redirect(url_for("supervisor.reports"))

    comment = request.form.get("comment", "").strip()
    if comment:
        report.comment = comment
        db.session.commit()
        flash("Comment added.", "success")

    return redirect(url_for("supervisor.report_detail", report_id=report.id))

    
@supervisor_bp.route("/surveys")
@login_required
@role_required("supervisor")
def surveys():
    surveys = Survey.query.order_by(Survey.created_at.desc()).all()
    return render_template("supervisor.surveys.html", surveys=surveys)
@supervisor_bp.route("/surveys/upload", methods=["GET", "POST"])
@login_required
@role_required("supervisor")
def upload_new_survey():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        survey_type = request.form.get("survey_type")
        link = request.form.get("link")

        survey = Survey(
            title=title,
            description=description,
            survey_type=survey_type,
            link=link,
            portfolio=current_user.portfolio
        )
        db.session.add(survey)
        db.session.commit()

        flash("Survey uploaded successfully.", "success")
        return redirect(url_for("supervisor.surveys"))

    return render_template("supervisor.upload_new_survey.html")
    