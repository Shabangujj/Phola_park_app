"""
JJCORETECH
Phola Park App

Admin Dashboard Routes
"""

from datetime import datetime, timedelta

from flask import (
    render_template,
    jsonify,
)

from flask_login import login_required

from sqlalchemy import func

from . import admin_bp

from phola_park_app.decorators import role_required

from phola_park_app.models import (
    User,
    UserRole,
    Report,
    Survey,
    Announcement,
    AuditLog,
)

from phola_park_app.extensions import db


# =====================================================
# ADMIN DASHBOARD PAGE
# =====================================================

@admin_bp.route("/")
@login_required
@role_required("admin")
def dashboard():

    # -----------------------------------------
    # User statistics
    # -----------------------------------------

    total_users = User.query.count()

    active_users = User.query.filter_by(
        is_active=True
    ).count()

    disabled_users = User.query.filter_by(
        is_active=False
    ).count()

    admin_users = (
        User.query
        .join(UserRole)
        .filter(UserRole.name == "admin")
        .count()
    )

    supervisor_users = (
        User.query
        .join(UserRole)
        .filter(UserRole.name == "supervisor")
        .count()
    )

    normal_users = (
        User.query
        .join(UserRole)
        .filter(UserRole.name == "user")
        .count()
    )

    # -----------------------------------------
    # Recent users
    # -----------------------------------------

    recent_users = (
        User.query
        .order_by(User.created_at.desc())
        .limit(5)
        .all()
    )

    # -----------------------------------------
    # Dashboard totals
    # -----------------------------------------

    total_reports = Report.query.count()

    total_surveys = Survey.query.count()

    total_announcements = Announcement.query.count()

    pending_reports = Report.query.filter_by(
        status="Pending"
    ).count()

    return render_template(
        "admin/dashboard.html",

        total_users=total_users,
        active_users=active_users,
        disabled_users=disabled_users,

        admin_users=admin_users,
        supervisor_users=supervisor_users,
        normal_users=normal_users,

        recent_users=recent_users,

        total_reports=total_reports,
        total_surveys=total_surveys,
        total_announcements=total_announcements,
        pending_reports=pending_reports,
    )


# =====================================================
# DASHBOARD CARDS API
# =====================================================

@admin_bp.route("/dashboard/cards")
@login_required
@role_required("admin")
def dashboard_cards():

    return jsonify({

        "users": User.query.count(),

        "reports": Report.query.count(),

        "surveys": Survey.query.count(),

        "announcements": Announcement.query.count(),

        "pending": Report.query.filter_by(
            status="Pending"
        ).count(),

        "assigned": Report.query.filter_by(
            status="Assigned"
        ).count(),

        "progress": Report.query.filter_by(
            status="In Progress"
        ).count(),

        "resolved": Report.query.filter_by(
            status="Resolved"
        ).count(),

        "closed": Report.query.filter_by(
            status="Closed"
        ).count(),

    })


# =====================================================
# DASHBOARD STATISTICS API
# =====================================================

@admin_bp.route("/dashboard/statistics")
@login_required
@role_required("admin")
def dashboard_statistics():

    categories = (
        db.session.query(
            Report.category,
            func.count(Report.id)
        )
        .group_by(Report.category)
        .all()
    )

    portfolios = (
        db.session.query(
            Report.portfolio,
            func.count(Report.id)
        )
        .group_by(Report.portfolio)
        .all()
    )

    return jsonify({

        "categories": [
            {
                "name": category or "Unassigned",
                "count": count
            }
            for category, count in categories
        ],

        "portfolios": [
            {
                "name": portfolio or "Unassigned",
                "count": count
            }
            for portfolio, count in portfolios
        ]

    })


# =====================================================
# RECENT ACTIVITY API
# =====================================================

@admin_bp.route("/dashboard/activity")
@login_required
@role_required("admin")
def dashboard_activity():

    logs = (
        AuditLog.query
        .order_by(
            AuditLog.timestamp.desc()
        )
        .limit(20)
        .all()
    )

    return jsonify([

        {
            "id": log.id,

            "user": (
                log.user.username
                if log.user
                else "Unknown"
            ),

            "action": log.action,

            "description": log.description,

            "time": (
                log.timestamp.strftime(
                    "%d %b %Y %H:%M"
                )
                if log.timestamp
                else "Unknown"
            ),
        }

        for log in logs

    ])


# =====================================================
# WEEKLY REPORT CHART API
# =====================================================

@admin_bp.route("/dashboard/weekly")
@login_required
@role_required("admin")
def weekly_reports_dashboard():

    start = (
        datetime.utcnow()
        - timedelta(days=7)
    )

    data = (
        db.session.query(
            func.date(Report.created_at),
            func.count(Report.id)
        )
        .filter(
            Report.created_at >= start
        )
        .group_by(
            func.date(Report.created_at)
        )
        .order_by(
            func.date(Report.created_at)
        )
        .all()
    )

    return jsonify({

        "labels": [
            str(row[0])
            for row in data
        ],

        "values": [
            row[1]
            for row in data
        ]

    })