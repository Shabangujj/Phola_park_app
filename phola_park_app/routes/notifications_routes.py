from flask import Blueprint, jsonify, session, redirect, url_for, request
from datetime import datetime
from phola_park_app.model import Notification, User, Reports, Announcement
from phola_park_app import db
notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")


# 🔔 CREATE NOTIFICATION (Reusable function)
def create_notification(user_id, message):
    notification = Notification(
        user_id=user_id,
        message=message,
        is_read=False,
        created_at=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()


# 📥 GET USER NOTIFICATIONS
@notifications_bp.route("/", methods=["GET"])
def get_notifications():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    user_id = session.get("user_id")

    notifications = Notification.query.filter_by(user_id=user_id)\
        .order_by(Notification.created_at.desc()).all()

    result = []
    for n in notifications:
        result.append({
            "id": n.id,
            "message": n.message,
            "is_read": n.is_read,
            "date": str(n.created_at)
        })

    return jsonify(result)


# ✅ MARK AS READ
@notifications_bp.route("/read/<int:notification_id>", methods=["POST"])
def mark_as_read(notification_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    notification = Notification.query.get_or_404(notification_id)
    notification.is_read = True
    db.session.commit()

    return jsonify({"message": "Marked as read"})


# 🧹 MARK ALL AS READ
@notifications_bp.route("/read_all", methods=["POST"])
def mark_all_read():
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    user_id = session.get("user_id")

    Notification.query.filter_by(user_id=user_id, is_read=False)\
        .update({"is_read": True})

    db.session.commit()

    return jsonify({"message": "All notifications marked as read"})


# ❌ DELETE NOTIFICATION
@notifications_bp.route("/delete/<int:notification_id>", methods=["POST"])
def delete_notification(notification_id):
    if not session.get("user_id"):
        return redirect(url_for("auth.login"))

    notification = Notification.query.get_or_404(notification_id)

    db.session.delete(notification)
    db.session.commit()

    return jsonify({"message": "Notification deleted"})


# 🔔 TRIGGER: REPORT STATUS CHANGE
def notify_report_status(report, new_status):
    user = User.query.get(report.user_id)

    if user:
        create_notification(
            user.id,
            f"Your report #{report.id} status changed to {new_status}"
        )


# 🔔 TRIGGER: NEW ANNOUNCEMENT
def notify_new_announcement(announcement):
    users = User.query.all()

    for user in users:
        create_notification(
            user.id,
            f"New announcement: {announcement.title}"
        )


# 🔔 TRIGGER: NEW REPORT (notify supervisor)
def notify_new_report(report):
    supervisors = User.query.filter_by(role="supervisor", portfolio=report.portfolio).all()

    for sup in supervisors:
        create_notification(
            sup.id,
            f"New report in {report.portfolio} portfolio"
        )