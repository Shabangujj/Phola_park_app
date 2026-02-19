from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from datetime import datetime

from phola_park_app.extensions import db
from phola_park_app.model import Notification
from phola_park_app.decorators import role_required

notifications_api = Blueprint("notifications_api", __name__, url_prefix="/notifications")
notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/notifications", methods=["GET"])
@jwt_required()
def get_notifications():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role")

    if role == "admin":
        notifications = Notification.query.order_by(Notification.created_at.desc()).all()

    elif role == "supervisor":
        portfolio = claims.get("portfolio")
        notifications = Notification.query.filter_by(
            role_target="supervisor",
            portfolio=portfolio
        ).order_by(Notification.created_at.desc()).all()

    else:
        notifications = Notification.query.filter_by(
            user_id=current_user_id
        ).order_by(Notification.created_at.desc()).all()

    return jsonify([
        {
            "id": n.id,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at
        } for n in notifications
    ])

@notifications_bp.route("/notifications/<int:id>/read", methods=["PUT"])
@jwt_required()
def mark_as_read(id):
    notification = Notification.query.get_or_404(id)

    notification.is_read = True
    db.session.commit()

    return {"message": "Notification marked as read"}
@notifications_bp.route("/notifications/unread-count", methods=["GET"])
@jwt_required()
def unread_count():
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role")

    if role == "admin":
        count = Notification.query.filter_by(is_read=False).count()

    elif role == "supervisor":
        portfolio = claims.get("portfolio")
        count = Notification.query.filter_by(
            role_target="supervisor",
            portfolio=portfolio,
            is_read=False
        ).count()
    else:
        count = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()

    return {"unread": count}
@notifications_bp.route("/notifications/read-all", methods=["PUT"])
@jwt_required()
def mark_all_read():
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role")

    if role == "admin":
        Notification.query.filter_by(is_read=False).update({"is_read": True})

    elif role == "supervisor":
        portfolio = claims.get("portfolio")
        Notification.query.filter_by(
            role_target="supervisor",
            portfolio=portfolio,
            is_read=False
        ).update({"is_read": True})
    else:
        Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).update({"is_read": True})

    db.session.commit()

    return {"message": "All notifications marked as read"}
@notifications_bp.route("/notifications/broadcast", methods=["POST"])
@jwt_required()
def broadcast_notification():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return {"error": "Admin only"}, 403

    data = request.get_json()

    message = data.get("message")
    role_target = data.get("role_target")
    portfolio = data.get("portfolio")

    notification = Notification(
        message=message,
        role_target=role_target,
        portfolio=portfolio
    )

    db.session.add(notification)
    db.session.commit()

    return {"message": "Broadcast sent"}
