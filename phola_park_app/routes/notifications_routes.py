"""
JJCORETECH
Phola Park App

Notification Routes
"""

from datetime import datetime

from flask import (
    Blueprint,
    jsonify,
    redirect,
    url_for,
    render_template,
    session,
)

from flask_login import login_required, current_user

from phola_park_app.extensions import db

from phola_park_app.models import (
    Notification,
    User,
)


notifications_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/notifications"
)


# ============================================================
# NOTIFICATION CENTER PAGE
# ============================================================

@notifications_bp.route("/page")
@login_required
def notification_page():

    notifications = (
        Notification.query
        .filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return render_template(
        "notifications/notifications.html",
        notifications=notifications
    )

# ============================================================
# CREATE NOTIFICATION
# Reusable helper
# ============================================================

def create_notification(
    user_id,
    title,
    message,
    role_target=None,
    portfolio=None,
    notification_type="general",
):

    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        role_target=role_target,
        portfolio=portfolio,
        notification_type=notification_type,
        is_read=False,
        created_at=datetime.utcnow(),
    )

    db.session.add(notification)
    db.session.commit()

    return notification


# ============================================================
# GET USER NOTIFICATIONS
# ============================================================

@notifications_bp.route("/")
@login_required
def get_notifications():

    notifications = (
        Notification.query
        .filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return jsonify([
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "notification_type": n.notification_type,
            "portfolio": n.portfolio,
            "created_at": (
                n.created_at.strftime("%Y-%m-%d %H:%M")
                if n.created_at
                else ""
            ),
        }
        for n in notifications
    ])


# ============================================================
# MARK AS READ
# ============================================================

@notifications_bp.route(
    "/read/<int:notification_id>",
    methods=["POST"]
)
@login_required
def mark_as_read(notification_id):

    notification = Notification.query.get_or_404(
        notification_id
    )

    if notification.user_id != current_user.id:

        return jsonify({
            "error": "Unauthorized"
        }), 403

    notification.is_read = True

    db.session.commit()

    return jsonify({
        "message": "Notification marked as read."
    })


# ============================================================
# MARK ALL AS READ
# ============================================================

@notifications_bp.route(
    "/read_all",
    methods=["POST"]
)
@login_required
def mark_all_read():

    Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).update(
        {
            "is_read": True
        }
    )

    db.session.commit()

    return jsonify({
        "message": "All notifications marked as read."
    })


# ============================================================
# DELETE NOTIFICATION
# ============================================================

@notifications_bp.route(
    "/delete/<int:notification_id>",
    methods=["POST"]
)
@login_required
def delete_notification(notification_id):

    notification = Notification.query.get_or_404(
        notification_id
    )

    if notification.user_id != current_user.id:

        return jsonify({
            "error": "Unauthorized"
        }), 403

    db.session.delete(notification)

    db.session.commit()

    return jsonify({
        "message": "Notification deleted."
    })


# ============================================================
# REPORT STATUS NOTIFICATION
# ============================================================

def notify_report_status(report, new_status):

    create_notification(
        user_id=report.user_id,
        title="Report Status Updated",
        message=(
            f"Your report #{report.id} has been updated to "
            f"'{new_status}'."
        ),
        role_target="user",
        portfolio=report.portfolio,
        notification_type="report",
    )


# ============================================================
# NEW ANNOUNCEMENT NOTIFICATION
# ============================================================

def notify_new_announcement(announcement):

    users = User.query.all()

    for user in users:

        create_notification(
            user_id=user.id,
            title="New Community Announcement",
            message=announcement.title,
            role_target="user",
            portfolio=announcement.portfolio,
            notification_type="announcement",
        )


# ============================================================
# NEW REPORT NOTIFICATION
# Supervisor
# ============================================================

def notify_new_report(report):

    supervisors = (
        User.query
        .join(User.role)
        .filter(
            User.portfolio == report.portfolio,
            User.role.has(name="supervisor")
        )
        .all()
    )

    for supervisor in supervisors:

        create_notification(
            user_id=supervisor.id,
            title="New Community Report",
            message=(
                f"A new report has been submitted in the "
                f"{report.portfolio} portfolio."
            ),
            role_target="supervisor",
            portfolio=report.portfolio,
            notification_type="report",
        )