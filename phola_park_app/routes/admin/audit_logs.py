"""
====================================================
JJCORETECH
Phola Park App
Admin Audit Logs
====================================================
"""
from phola_park_app.extensions import db
from datetime import date, datetime
from itertools import count

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Response
)

from flask_login import (
    login_required,
    current_user
)

from sqlalchemy import or_

from . import admin_bp

from phola_park_app.decorators import role_required

from phola_park_app.models import (
    AuditLog,
    User
)

from datetime import date
from sqlalchemy import func
from flask import render_template, request
from flask_login import login_required

@admin_bp.route("/audit-logs")
@login_required
@role_required("admin")
def audit_logs():

    page = request.args.get("page", 1, type=int)
    action = request.args.get("action", "").strip()

    query = AuditLog.query

    # Filter by action
    if action:
        query = query.filter(
            AuditLog.action.ilike(f"%{action}%")
        )

    # Order by newest first
    query = query.order_by(AuditLog.created_at.desc())

    logs = query.paginate(
        page=page,
        per_page=20,
        error_out=False
    )

    # Dashboard statistics
    total_logs = AuditLog.query.count()

    active_users = db.session.query(
        AuditLog.user_id
    ).distinct().count()

    today_logs = AuditLog.query.filter(
        func.date(AuditLog.created_at) == date.today()
    ).count()

    most_common = (
        db.session.query(
            AuditLog.action,
            func.count(AuditLog.id)
        )
        .group_by(AuditLog.action)
        .order_by(func.count(AuditLog.id).desc())
        .first()
    )

    most_common_action = (
        most_common[0] if most_common else "None"
    )

    # Logs per day
    logs_per_day = (
        db.session.query(
            func.date(AuditLog.created_at),
            func.count(AuditLog.id)
        )
        .group_by(func.date(AuditLog.created_at))
        .all()
    )

    dates = [str(row[0]) for row in logs_per_day]
    counts = [row[1] for row in logs_per_day]

    # Actions chart
    actions = (
        db.session.query(
            AuditLog.action,
            func.count(AuditLog.id)
        )
        .group_by(AuditLog.action)
        .all()
    )

    action_labels = [row[0] for row in actions]
    action_counts = [row[1] for row in actions]

    return render_template(
        "admin/audit_logs.html",
        logs=logs.items,
        pagination=logs,
        action=action,
        total_logs=total_logs,
        active_users=active_users,
        today_logs=today_logs,
        most_common_action=most_common_action,
        dates=dates,
        counts=counts,
        action_labels=action_labels,
        action_counts=action_counts
    )
@admin_bp.route(
    "/audit-logs/<int:log_id>"
)
@login_required
@role_required("admin")
def audit_log(log_id):

    log = AuditLog.query.get_or_404(
        log_id
    )

    return render_template(

        "admin/audit_log.html",

        log=log

    )
@admin_bp.route(
    "/audit-logs/<int:log_id>/delete",
    methods=["POST"]
)
@login_required
@role_required("admin")
def delete_log(log_id):

    log = AuditLog.query.get_or_404(
        log_id
    )

    db.session.delete(log)

    db.session.commit()

    flash(

        "Audit log deleted.",

        "success"

    )

    return redirect(
        url_for(
            "admin.audit_logs"
        )
    )
@admin_bp.route(
    "/audit-logs/clear",
    methods=["POST"]
)
@login_required
@role_required("admin")
def clear_logs():

    AuditLog.query.delete()

    db.session.commit()

    flash(

        "All audit logs cleared.",

        "warning"

    )

    return redirect(
        url_for(
            "admin.audit_logs"
        )
    )
@admin_bp.route(
    "/audit-logs/export"
)
@login_required
@role_required("admin")
def export_audit_logs():

    logs = AuditLog.query.order_by(
        AuditLog.created_at.desc()
    ).all()

    def generate():

        yield (
            "ID,"
            "Username,"
            "Action,"
            "Module,"
            "IP Address,"
            "Created\n"
        )

        for log in logs:

            yield (

                f"{log.id},"

                f"{log.username},"

                f"{log.action},"

                f"{log.module},"

                f"{log.ip_address},"

                f"{log.created_at}\n"

            )

    return Response(

        generate(),

        mimetype="text/csv",

        headers={

            "Content-Disposition":

            "attachment; filename=audit_logs.csv"

        }

    )
@admin_bp.route("/audit-logs/dashboard")
@login_required
@role_required("admin")
def audit_dashboard():

    total_logs = AuditLog.query.count()

    today = date.today()

    today_logs = AuditLog.query.filter(

        db.func.date(
            AuditLog.created_at
        ) == today

    ).count()

    return render_template(

        "admin/audit_dashboard.html",

        total_logs=total_logs,

        today_logs=today_logs

    )
@admin_bp.route("/audit-logs/activity")
@login_required
@role_required("admin")
def activity_feed():

    logs = AuditLog.query.order_by(

        AuditLog.created_at.desc()

    ).limit(50).all()

    return render_template(

        "admin/activity_feed.html",

        logs=logs

    )