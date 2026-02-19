from phola_park_app.model import Notification
from phola_park_app.extensions import db

def notify(user_id, title, message, link=None):
    n = Notification(
        user_id=user_id,
        title=title,
        message=message,
        link=link
    )
    db.session.add(n)
    db.session.commit()


def get_unread_notifications(user):
    return Notification.query.filter_by(
        user_id=user.id,
        is_read=False
    ).order_by(Notification.created_at.desc()).all()

def get_notifications_for_user(user):
    if user.role.name == "admin":
        return Notification.query.all()

    return Notification.query.filter(
        (Notification.target_role == user.role.name) |
        (Notification.target_role == "all")
    ).order_by(Notification.created_at.desc()).all()
