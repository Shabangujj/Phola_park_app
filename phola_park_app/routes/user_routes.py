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
from phola_park_app.models import (
    Report, Survey, Announcement,
    SurveyQuestion, SurveyResponse,
    SurveyAnswer,
    Notification, User
)
from phola_park_app.auth_helpers import role_required
from phola_park_app.forms.report_form import ReportForm
import os

from datetime import datetime, timedelta
from datetime import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    jsonify,
    current_app
)

from flask_login import (
    login_required,
    current_user
)
from sqlalchemy import or_, func
user_bp = Blueprint("user", __name__, url_prefix="/user")

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ─────────────────────────────────────────────
# USER ROUTES
# ─────────────────────────────────────────────



@user_bp.route("/dashboard")
@login_required
def user_dashboard():

    # =================================================
    # ROLE CHECK
    # =================================================

    if current_user.role_name != "user":
        abort(403)

    # =================================================
    # USER REPORTS
    # =================================================

    reports_count = (
        Report.query
        .filter_by(
            user_id=current_user.id
        )
        .count()
    )

    recent_reports = (
        Report.query
        .filter_by(
            user_id=current_user.id
        )
        .order_by(
            Report.created_at.desc()
        )
        .limit(5)
        .all()
    )

    # =================================================
    # ANNOUNCEMENTS
    # =================================================
    #
    # Show announcements that:
    #
    # 1. Are active
    # 2. Are not expired
    # 3. Target everyone OR users
    # 4. Match user's portfolio OR are for all portfolios
    #
    # =================================================

    from sqlalchemy import or_, and_

    notices = (
        Announcement.query
        .filter(
            Announcement.is_active.is_(True),

            # Target audience
            or_(
                Announcement.target_role.is_(None),
                Announcement.target_role == "",
                Announcement.target_role == "all",
                Announcement.target_role == "user"
            ),

            # Portfolio
            or_(
                Announcement.portfolio.is_(None),
                Announcement.portfolio == "",
                Announcement.portfolio == current_user.portfolio
            )
        )
        .order_by(
            Announcement.created_at.desc()
        )
        .limit(5)
        .all()
    )

    # =================================================
    # ACTIVE SURVEYS
    # =================================================

    active_surveys = (
    Survey.query
    .filter_by(is_active=True)
    .order_by(Survey.created_at.desc())
    .all()
)

    # =================================================
    # DASHBOARD
    # =================================================

    return render_template(
        "user/user_dashboard.html",

        reports_count=reports_count,

        recent_reports=recent_reports,

        notices=notices,

        active_surveys=active_surveys,
    )
# ─────────────────────────────────────────────
# SUBMIT REPORT
# ─────────────────────────────────────────────

@user_bp.route(
    "/reports/submit",
    methods=["GET", "POST"]
)
@login_required
@role_required("user")
def submit_report():

    form = ReportForm()

    # -----------------------------------------
    # Submit form
    # -----------------------------------------

    if form.validate_on_submit():

        image_file = form.image.data
        filename = None

        # -------------------------------------
        # Save image
        # -------------------------------------

        if image_file:

            filename = secure_filename(
                image_file.filename
            )

            upload_folder = current_app.config[
                "UPLOAD_FOLDER"
            ]

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            image_file.save(
                os.path.join(
                    upload_folder,
                    filename
                )
            )

        # -------------------------------------
        # Create report
        # -------------------------------------

        report = Report(

            title=(
                f"{form.category.data} Report"
            ),

            report_type=form.report_type.data,

            category=form.category.data,

            description=form.description.data,

            portfolio=form.portfolio.data,

            image=filename,

            user_id=current_user.id

        )

        # -------------------------------------
        # Save report
        # -------------------------------------

        try:

            db.session.add(report)

            db.session.commit()

            flash(
                "Report submitted successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "user.user_reports"
                )
            )

        except Exception as e:

            db.session.rollback()

            print(
                "REPORT SUBMISSION ERROR:",
                e
            )

            flash(
                "Unable to submit report. "
                "Please try again.",
                "danger"
            )

    # -----------------------------------------
    # Display form
    # -----------------------------------------

    return render_template(
        "user/submit_report.html",
        form=form
    )


# ─────────────────────────────────────────────
# USER REPORTS
# LIST + FILTER + CSV EXPORT
# ─────────────────────────────────────────────

@user_bp.route("/reports")
@login_required
@role_required("user")
def user_reports():

    # -----------------------------------------
    # Base query
    # -----------------------------------------

    reports = Report.query.filter(
        Report.user_id == current_user.id
    )

    # -----------------------------------------
    # Filters
    # -----------------------------------------

    q = request.args.get(
        "q",
        ""
    ).strip()

    category = request.args.get(
        "category",
        ""
    ).strip()

    date_from = request.args.get(
        "date_from",
        ""
    ).strip()

    date_to = request.args.get(
        "date_to",
        ""
    ).strip()


    # -----------------------------------------
    # Search
    # -----------------------------------------

    if q:

        reports = reports.filter(
            db.or_(
                Report.description.ilike(
                    f"%{q}%"
                ),

                Report.title.ilike(
                    f"%{q}%"
                ),

                Report.category.ilike(
                    f"%{q}%"
                )
            )
        )


    # -----------------------------------------
    # Category
    # -----------------------------------------

    if category:

        reports = reports.filter(
            Report.category == category
        )


    # -----------------------------------------
    # Date From
    # -----------------------------------------

    if date_from:

        try:

            start_date = datetime.strptime(
                date_from,
                "%Y-%m-%d"
            )

            reports = reports.filter(
                Report.created_at >= start_date
            )

        except ValueError:

            flash(
                "Invalid start date.",
                "warning"
            )


    # -----------------------------------------
    # Date To
    # -----------------------------------------

    if date_to:

        try:

            end_date = (
                datetime.strptime(
                    date_to,
                    "%Y-%m-%d"
                )
                + timedelta(days=1)
            )

            reports = reports.filter(
                Report.created_at < end_date
            )

        except ValueError:

            flash(
                "Invalid end date.",
                "warning"
            )


    # -----------------------------------------
    # Order
    # -----------------------------------------

    reports = reports.order_by(
        Report.created_at.desc()
    )


    # =========================================
    # CSV EXPORT
    # =========================================

    if request.args.get("export") == "csv":

        import csv
        import io

        output = io.StringIO()

        writer = csv.writer(
            output
        )

        writer.writerow([
            "ID",
            "Title",
            "Type",
            "Category",
            "Description",
            "Portfolio",
            "Status",
            "Created At"
        ])

        for report in reports.all():

            writer.writerow([

                report.id,

                report.title,

                report.report_type,

                report.category,

                report.description,

                report.portfolio,

                report.status,

                report.created_at

            ])

        return current_app.response_class(

            output.getvalue(),

            mimetype="text/csv",

            headers={
                "Content-Disposition":
                    "attachment; "
                    "filename=user_reports.csv"
            }

        )


    # =========================================
    # PAGINATION
    # =========================================

    pagination = reports.paginate(

        page=request.args.get(
            "page",
            1,
            type=int
        ),

        per_page=10,

        error_out=False

    )


    # =========================================
    # FILTER DATA
    # =========================================

    filters = {

        "q": q,

        "category": category,

        "date_from": date_from,

        "date_to": date_to

    }


    # =========================================
    # RENDER
    # =========================================

    return render_template(

        "user/user_reports.html",

        reports=pagination.items,

        pagination=pagination,

        filters=filters

    )

# =====================================================
# USER SURVEYS
# =====================================================

@user_bp.route("/surveys")
@login_required
@role_required("user")
def surveys():

    surveys = (
        Survey.query
        .filter_by(is_active=True)
        .order_by(
            Survey.created_at.desc()
        )
        .all()
    )

    return render_template(
        "user/surveys.html",
        surveys=surveys
    )

# =====================================================
# TAKE SURVEY
# =====================================================

@user_bp.route(
    "/surveys/<int:survey_id>",
    methods=["GET"]
)
@login_required
@role_required("user")
def take_survey(survey_id):

    survey = Survey.query.get_or_404(
        survey_id
    )

    # ---------------------------------------------
    # Only active surveys can be completed
    # ---------------------------------------------

    if not survey.is_active:

        flash(
            "This survey is no longer available.",
            "warning"
        )

        return redirect(
            url_for("user.surveys")
        )

    # ---------------------------------------------
    # Load questions
    # ---------------------------------------------

    questions = (
        SurveyQuestion.query
        .filter_by(
            survey_id=survey.id
        )
        .order_by(
            SurveyQuestion.order.asc(),
            SurveyQuestion.id.asc()
        )
        .all()
    )

    return render_template(
        "user/take_survey.html",
        survey=survey,
        questions=questions
    )


# =====================================================
# SUBMIT SURVEY
# =====================================================

@user_bp.route(
    "/surveys/<int:survey_id>/submit",
    methods=["POST"]
)
@login_required
@role_required("user")
def submit_survey(survey_id):

    survey = Survey.query.get_or_404(
        survey_id
    )

    # ---------------------------------------------
    # Check survey status
    # ---------------------------------------------

    if not survey.is_active:

        flash(
            "This survey is no longer available.",
            "warning"
        )

        return redirect(
            url_for("user.surveys")
        )

    # ---------------------------------------------
    # Load questions
    # ---------------------------------------------

    questions = (
        SurveyQuestion.query
        .filter_by(
            survey_id=survey.id
        )
        .order_by(
            SurveyQuestion.order.asc(),
            SurveyQuestion.id.asc()
        )
        .all()
    )

    # ---------------------------------------------
    # Make sure survey has questions
    # ---------------------------------------------

    if not questions:

        flash(
            "This survey has no questions yet.",
            "warning"
        )

        return redirect(
            url_for(
                "user.take_survey",
                survey_id=survey.id
            )
        )

    # ---------------------------------------------
    # Prevent duplicate submission
    # ---------------------------------------------

    existing_response = (
        SurveyResponse.query
        .filter_by(
            survey_id=survey.id,
            user_id=current_user.id
        )
        .first()
    )

    if existing_response:

        flash(
            "You have already submitted this survey.",
            "info"
        )

        return redirect(
            url_for("user.surveys")
        )

    # ---------------------------------------------
    # Validate answers
    # ---------------------------------------------

    answers = {}

    for question in questions:

        field_name = f"question_{question.id}"

        value = request.form.get(
            field_name,
            ""
        ).strip()

        if not value:

            flash(
                f"Please answer Question {question.order}.",
                "danger"
            )

            return redirect(
                url_for(
                    "user.take_survey",
                    survey_id=survey.id
                )
            )

        answers[question.id] = value

    # ---------------------------------------------
    # Create Survey Response
    # ---------------------------------------------

    response = SurveyResponse(
        survey_id=survey.id,
        user_id=current_user.id
    )

    try:

        db.session.add(response)

        db.session.flush()

        # -----------------------------------------
        # Create Survey Answers
        # -----------------------------------------

        for question in questions:

            answer = SurveyAnswer(
                response_id=response.id,
                question_id=question.id,
                value=answers[question.id]
            )

            db.session.add(answer)

        db.session.commit()

        flash(
            "Survey submitted successfully.",
            "success"
        )

        return redirect(
            url_for("user.surveys")
        )

    except Exception as e:

        db.session.rollback()

        print(
            "SURVEY SUBMISSION ERROR:",
            e
        )

        flash(
            "Unable to submit survey. Please try again.",
            "danger"
        )

        return redirect(
            url_for(
                "user.take_survey",
                survey_id=survey.id
            )
        )

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
# ─────────────────────────────────────────────
# USER NOTICES
# ─────────────────────────────────────────────

@user_bp.route("/notices")
@login_required
@role_required("user")
def user_notices():

    notices = (
        Announcement.query
        .filter(
            Announcement.is_active.is_(True),

            # Target audience
            or_(
                Announcement.target_role.is_(None),
                Announcement.target_role == "",
                Announcement.target_role == "all",
                Announcement.target_role == "user"
            ),

            # Portfolio
            or_(
                Announcement.portfolio.is_(None),
                Announcement.portfolio == "",
                Announcement.portfolio == current_user.portfolio
            )
        )
        .order_by(
            Announcement.created_at.desc()
        )
        .all()
    )

    return render_template(
        "user/notices.html",
        notices=notices
    )