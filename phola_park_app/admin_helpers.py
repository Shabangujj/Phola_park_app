from flask_login import current_user
from phola_park_app.model import User, Notification
from phola_park_app.database import db
from phola_park_app.admin_helpers import is_admin, is_supervisor, is_admin_or_supervisor, redirect_if_wrong_role

def create_announcement_notifications(announcement):
    query = User.query

    if hasattr(announcement, 'target_role') and announcement.target_role:
        query = query.filter_by(role=announcement.target_role)

    if hasattr(announcement, 'portfolio') and announcement.portfolio:
        query = query.filter_by(portfolio=announcement.portfolio)

    users = query.all()

    for u in users:
        n = Notification(
            user_id=current_user.id,
            title=f"📢 {announcement.title}",
            message=announcement.message,
            link="/announcements"
        )
        db.session.add(n)

    db.session.commit()
