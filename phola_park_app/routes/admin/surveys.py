"""
====================================================
JJCORETECH
Phola Park App
Admin Survey Management
====================================================
"""

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required

from sqlalchemy import func

from . import admin_bp

from phola_park_app.decorators import role_required

from phola_park_app.models import (
    Survey,
    SurveyQuestion,
    SurveyResponse,
    SurveyAnswer
)

from phola_park_app.extensions import db


# ====================================================
# SURVEY LIST
# ====================================================

@admin_bp.route("/surveys")
@login_required
@role_required("admin")
def surveys():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    query = Survey.query

    if search:
        query = query.filter(
            Survey.title.ilike(
                f"%{search}%"
            )
        )

    surveys = query.order_by(
        Survey.created_at.desc()
    ).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    return render_template(
        "admin/surveys.html",
        surveys=surveys,
        search=search
    )


# ====================================================
# VIEW SURVEY
# ====================================================

@admin_bp.route(
    "/surveys/<int:survey_id>"
)
@login_required
@role_required("admin")
def view_survey(survey_id):

    survey = Survey.query.get_or_404(
        survey_id
    )

    return render_template(
        "admin/view_survey.html",
        survey=survey
    )


# ====================================================
# CREATE SURVEY
# ====================================================

@admin_bp.route(
    "/surveys/create",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def create_survey():

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        survey_type = request.form.get(
            "survey_type",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        portfolio = request.form.get(
            "portfolio",
            ""
        ).strip()

        link = request.form.get(
            "link",
            ""
        ).strip()

        # -------------------------------
        # Validation
        # -------------------------------

        if not title:
            flash(
                "Survey title is required.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.create_survey"
                )
            )

        if not survey_type:
            flash(
                "Survey type is required.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.create_survey"
                )
            )

        # -------------------------------
        # Create Survey
        # -------------------------------

        survey = Survey(
            title=title,
            survey_type=survey_type,
            description=description,
            portfolio=portfolio or None,
            link=link or None,
            is_active=True
        )

        try:

            db.session.add(survey)

            db.session.commit()

            flash(
                "Survey created successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "admin.view_survey",
                    survey_id=survey.id
                )
            )

        except Exception as e:

            db.session.rollback()

            print(
                "CREATE SURVEY ERROR:",
                e
            )

            flash(
                "Unable to create survey.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.create_survey"
                )
            )

    return render_template(
        "admin/create_survey.html"
    )


# ====================================================
# EDIT SURVEY
# ====================================================

@admin_bp.route(
    "/surveys/<int:survey_id>/edit",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def edit_survey(survey_id):

    survey = Survey.query.get_or_404(
        survey_id
    )

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        survey_type = request.form.get(
            "survey_type",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        portfolio = request.form.get(
            "portfolio",
            ""
        ).strip()

        link = request.form.get(
            "link",
            ""
        ).strip()

        if not title:

            flash(
                "Survey title is required.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.edit_survey",
                    survey_id=survey.id
                )
            )

        if not survey_type:

            flash(
                "Survey type is required.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.edit_survey",
                    survey_id=survey.id
                )
            )

        survey.title = title
        survey.survey_type = survey_type
        survey.description = description
        survey.portfolio = portfolio or None
        survey.link = link or None

        try:

            db.session.commit()

            flash(
                "Survey updated successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "admin.view_survey",
                    survey_id=survey.id
                )
            )

        except Exception as e:

            db.session.rollback()

            print(
                "EDIT SURVEY ERROR:",
                e
            )

            flash(
                "Unable to update survey.",
                "danger"
            )

    return render_template(
        "admin/edit_survey.html",
        survey=survey
    )


# ====================================================
# DELETE SURVEY
# ====================================================

@admin_bp.route(
    "/surveys/<int:survey_id>/delete",
    methods=["POST"]
)
@login_required
@role_required("admin")
def delete_survey(survey_id):

    survey = Survey.query.get_or_404(
        survey_id
    )

    try:

        db.session.delete(survey)

        db.session.commit()

        flash(
            "Survey deleted successfully.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        print(
            "DELETE SURVEY ERROR:",
            e
        )

        flash(
            "Unable to delete survey.",
            "danger"
        )

    return redirect(
        url_for(
            "admin.surveys"
        )
    )


# ====================================================
# CLOSE SURVEY
# ====================================================

@admin_bp.route(
    "/surveys/<int:survey_id>/close",
    methods=["POST"]
)
@login_required
@role_required("admin")
def close_survey(survey_id):

    survey = Survey.query.get_or_404(
        survey_id
    )

    survey.deactivate()

    db.session.commit()

    flash(
        "Survey closed successfully.",
        "success"
    )

    return redirect(
        url_for(
            "admin.view_survey",
            survey_id=survey.id
        )
    )


# ====================================================
# REOPEN SURVEY
# ====================================================

@admin_bp.route(
    "/surveys/<int:survey_id>/reopen",
    methods=["POST"]
)
@login_required
@role_required("admin")
def reopen_survey(survey_id):

    survey = Survey.query.get_or_404(
        survey_id
    )

    survey.activate()

    db.session.commit()

    flash(
        "Survey reopened successfully.",
        "success"
    )

    return redirect(
        url_for(
            "admin.view_survey",
            survey_id=survey.id
        )
    )


# ====================================================
# SURVEY RESPONSES
# ====================================================

@admin_bp.route(
    "/surveys/<int:survey_id>/responses"
)
@login_required
@role_required("admin")
def survey_responses(survey_id):

    survey = Survey.query.get_or_404(
        survey_id
    )

    responses = (
        SurveyResponse.query
        .filter_by(
            survey_id=survey.id
        )
        .order_by(
            SurveyResponse.submitted_at.desc()
        )
        .all()
    )

    return render_template(
        "admin/survey_responses.html",
        survey=survey,
        responses=responses
    )
# =====================================================
# SURVEY ANALYTICS
# =====================================================

@admin_bp.route(
    "/surveys/<int:survey_id>/analytics"
)
@login_required
@role_required("admin")
def survey_analytics(survey_id):

    # -----------------------------------------
    # Get survey
    # -----------------------------------------

    survey = Survey.query.get_or_404(
        survey_id
    )

    # -----------------------------------------
    # Basic statistics
    # -----------------------------------------

    total_responses = (
        SurveyResponse.query
        .filter_by(
            survey_id=survey.id
        )
        .count()
    )

    total_questions = len(
        survey.questions
    )

    # -----------------------------------------
    # Question-by-question analytics
    # -----------------------------------------

    question_analytics = []

    for question in sorted(
        survey.questions,
        key=lambda q: q.order or 0
    ):

        answer_counts = {}

        # Find responses for this question
        for response in survey.responses:

            for answer in response.answers:

                if answer.question_id != question.id:
                    continue

                value = (
                    answer.value.strip()
                    if answer.value
                    else ""
                )

                if not value:
                    continue

                answer_counts[value] = (
                    answer_counts.get(
                        value,
                        0
                    ) + 1
                )

        # -------------------------------------
        # Prepare chart data
        # -------------------------------------

        question_labels = list(
            answer_counts.keys()
        )

        question_values = list(
            answer_counts.values()
        )

        question_analytics.append({

            "id": question.id,

            "text": question.text,

            "question_type":
                question.question_type,

            "labels":
                question_labels,

            "values":
                question_values,

            "total_answers":
                sum(question_values)

        })

    # -----------------------------------------
    # Overall answer summary
    # -----------------------------------------

    overall_counts = {}

    for question_data in question_analytics:

        for index, label in enumerate(
            question_data["labels"]
        ):

            value = question_data["values"][index]

            overall_counts[label] = (
                overall_counts.get(
                    label,
                    0
                ) + value
            )

    labels = list(
        overall_counts.keys()
    )

    values = list(
        overall_counts.values()
    )

    # -----------------------------------------
    # Render
    # -----------------------------------------

    return render_template(

        "admin/survey_analytics.html",

        survey=survey,

        total_responses=total_responses,

        total_questions=total_questions,

        question_analytics=question_analytics,

        labels=labels,

        values=values

    )
# ====================================================
# ADD SURVEY QUESTION
# ====================================================

@admin_bp.route(
    "/surveys/<int:survey_id>/questions/add",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def add_question(survey_id):

    survey = Survey.query.get_or_404(
        survey_id
    )

    if request.method == "POST":

        text = request.form.get(
            "text",
            ""
        ).strip()

        question_type = request.form.get(
            "question_type",
            ""
        ).strip()

        options = request.form.get(
            "options",
            ""
        ).strip()

        order_value = request.form.get(
            "order",
            "1"
        ).strip()

        # --------------------------------------------
        # Validation
        # --------------------------------------------

        if not text:

            flash(
                "Question text is required.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.add_question",
                    survey_id=survey.id
                )
            )

        if not question_type:

            flash(
                "Question type is required.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.add_question",
                    survey_id=survey.id
                )
            )

        try:

            question_order = int(
                order_value
            )

        except (TypeError, ValueError):

            question_order = (
                survey.total_questions + 1
            )

        # --------------------------------------------
        # Validate question types
        # --------------------------------------------

        allowed_types = {
            "text",
            "textarea",
            "number",
            "yes_no",
            "multiple_choice",
            "rating"
        }

        if question_type not in allowed_types:

            flash(
                "Invalid question type.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.add_question",
                    survey_id=survey.id
                )
            )

        # --------------------------------------------
        # Multiple choice requires options
        # --------------------------------------------

        if question_type == "multiple_choice" and not options:

            flash(
                "Please provide options for a multiple-choice question.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.add_question",
                    survey_id=survey.id
                )
            )

        # --------------------------------------------
        # Create question
        # --------------------------------------------

        question = SurveyQuestion(
            survey_id=survey.id,
            text=text,
            question_type=question_type,
            options=options or None,
            order=question_order
        )

        try:

            db.session.add(question)

            db.session.commit()

            flash(
                "Question added successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "admin.view_survey",
                    survey_id=survey.id
                )
            )

        except Exception as e:

            db.session.rollback()

            print(
                "ADD QUESTION ERROR:",
                e
            )

            flash(
                "Unable to add question.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.add_question",
                    survey_id=survey.id
                )
            )

    return render_template(
        "admin/add_question.html",
        survey=survey
    )


# ====================================================
# EDIT SURVEY QUESTION
# ====================================================

@admin_bp.route(
    "/questions/<int:question_id>/edit",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def edit_question(question_id):

    question = SurveyQuestion.query.get_or_404(
        question_id
    )

    survey = question.survey

    if request.method == "POST":

        text = request.form.get(
            "text",
            ""
        ).strip()

        question_type = request.form.get(
            "question_type",
            ""
        ).strip()

        options = request.form.get(
            "options",
            ""
        ).strip()

        order_value = request.form.get(
            "order",
            "1"
        ).strip()

        # --------------------------------------------
        # Validation
        # --------------------------------------------

        if not text:

            flash(
                "Question text is required.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.edit_question",
                    question_id=question.id
                )
            )

        if not question_type:

            flash(
                "Question type is required.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.edit_question",
                    question_id=question.id
                )
            )

        allowed_types = {
            "text",
            "textarea",
            "number",
            "yes_no",
            "multiple_choice",
            "rating"
        }

        if question_type not in allowed_types:

            flash(
                "Invalid question type.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.edit_question",
                    question_id=question.id
                )
            )

        if question_type == "multiple_choice" and not options:

            flash(
                "Please provide options for a multiple-choice question.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.edit_question",
                    question_id=question.id
                )
            )

        try:

            question_order = int(
                order_value
            )

        except (TypeError, ValueError):

            question_order = question.order or 1

        # --------------------------------------------
        # Update question
        # --------------------------------------------

        question.text = text

        question.question_type = (
            question_type
        )

        question.options = (
            options or None
        )

        question.order = (
            question_order
        )

        try:

            db.session.commit()

            flash(
                "Question updated successfully.",
                "success"
            )

            return redirect(
                url_for(
                    "admin.view_survey",
                    survey_id=survey.id
                )
            )

        except Exception as e:

            db.session.rollback()

            print(
                "EDIT QUESTION ERROR:",
                e
            )

            flash(
                "Unable to update question.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.edit_question",
                    question_id=question.id
                )
            )

    return render_template(
        "admin/edit_question.html",
        question=question,
        survey=survey
    )


# ====================================================
# DELETE SURVEY QUESTION
# ====================================================

@admin_bp.route(
    "/questions/<int:question_id>/delete",
    methods=["POST"]
)
@login_required
@role_required("admin")
def delete_question(question_id):

    question = SurveyQuestion.query.get_or_404(
        question_id
    )

    survey_id = question.survey_id

    try:

        db.session.delete(question)

        db.session.commit()

        flash(
            "Question deleted successfully.",
            "success"
        )

    except Exception as e:

        db.session.rollback()

        print(
            "DELETE QUESTION ERROR:",
            e
        )

        flash(
            "Unable to delete question.",
            "danger"
        )

    return redirect(
        url_for(
            "admin.view_survey",
            survey_id=survey_id
        )
    )