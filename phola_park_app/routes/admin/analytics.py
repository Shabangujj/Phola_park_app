"""
====================================================
JJCORETECH
Phola Park App
Admin Analytics
====================================================
"""

from datetime import datetime, timedelta

from flask import (
    render_template,
    request,
    jsonify
)

from flask_login import login_required

from sqlalchemy import func

from . import admin_bp

from phola_park_app.decorators import role_required

from phola_park_app.models import (
    User,
    Report,
    Survey,
    SurveyResponse,
    Announcement
)
from phola_park_app.extensions import db
@admin_bp.route("/analytics")
@login_required
@role_required("admin")
def analytics_dashboard():

    statistics = {

        "users": User.query.count(),

        "reports": Report.query.count(),

        "surveys": Survey.query.count(),

        "announcements": Announcement.query.count(),

        "responses": SurveyResponse.query.count()

    }

    return render_template(

        "admin/analytics_dashboard.html",

        statistics=statistics

    )
@admin_bp.route("/analytics/reports")
@login_required
@role_required("admin")
def report_status_analytics():

    data = (

        db.session.query(

            Report.status,

            func.count(Report.id)

        )

        .group_by(
            Report.status
        )

        .all()

    )

    labels = [row[0] for row in data]

    values = [row[1] for row in data]

    return jsonify({

        "labels": labels,

        "values": values

    })
@admin_bp.route("/analytics/categories")
@login_required
@role_required("admin")
def report_category_analytics():

    data = (

        db.session.query(

            Report.category,

            func.count(Report.id)

        )

        .group_by(
            Report.category
        )

        .all()

    )

    return jsonify({

        "labels":[row[0] for row in data],

        "values":[row[1] for row in data]

    })
@admin_bp.route("/analytics/portfolios")
@login_required
@role_required("admin")
def portfolio_analytics():

    data = (

        db.session.query(

            Report.portfolio,

            func.count(Report.id)

        )

        .group_by(
            Report.portfolio
        )

        .all()

    )

    return jsonify({

        "labels":[row[0] for row in data],

        "values":[row[1] for row in data]

    })
@admin_bp.route("/analytics/users")
@login_required
@role_required("admin")
def user_role_analytics():

    data = (

        db.session.query(

            User.role_id,

            func.count(User.id)

        )

        .group_by(
            User.role_id
        )

        .all()

    )

    return jsonify({

        "labels":[str(row[0]) for row in data],

        "values":[row[1] for row in data]

    })
@admin_bp.route("/analytics/weekly")
@login_required
@role_required("admin")
def weekly_reports():

    start = datetime.utcnow() - timedelta(days=7)

    data = (

        db.session.query(

            func.date(
                Report.created_at
            ),

            func.count(
                Report.id
            )

        )

        .filter(
            Report.created_at >= start
        )

        .group_by(
            func.date(
                Report.created_at
            )
        )

        .all()

    )

    return jsonify({

        "labels":[str(row[0]) for row in data],

        "values":[row[1] for row in data]

    })
@admin_bp.route("/analytics/surveys")
@login_required
@role_required("admin")
def surveys_analytics():

    data = (

        db.session.query(

            Survey.title,

            func.count(
                SurveyResponse.id
            )

        )

        .join(

            SurveyResponse,

            Survey.id == SurveyResponse.survey_id

        )

        .group_by(
            Survey.title
        )

        .all()

    )

    return jsonify({

        "labels":[row[0] for row in data],

        "values":[row[1] for row in data]

    })
@admin_bp.route("/analytics/recent")
@login_required
@role_required("admin")
def recent_activity():

    reports = Report.query.order_by(

        Report.created_at.desc()

    ).limit(10).all()

    return render_template(

        "admin/recent_activity.html",

        reports=reports

    )
@admin_bp.route("/analytics/kpi")
@login_required
@role_required("admin")
def kpi_dashboard():

    pending = Report.query.filter_by(
        status="Pending"
    ).count()

    progress = Report.query.filter_by(
        status="In Progress"
    ).count()

    resolved = Report.query.filter_by(
        status="Resolved"
    ).count()

    closed = Report.query.filter_by(
        status="Closed"
    ).count()

    return jsonify({

        "pending": pending,

        "progress": progress,

        "resolved": resolved,

        "closed": closed

    })