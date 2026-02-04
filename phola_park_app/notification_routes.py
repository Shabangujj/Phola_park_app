from flask import Blueprint, render_template, abort, redirect, url_for
from flask_login import login_required, current_user
from phola_park_app.model import Notification
from phola_park_app.extensions import db
notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route("/notifications")
@login_required
def notifications():
    notifications = (
        Notification.query
        .filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return render_template(
        "notifications.html",
        notifications=notifications
    )
@notifications_bp.route("/notifications/<int:id>")
@login_required
def open_notification(id):
    n = Notification.query.get_or_404(id)

    if n.user_id != current_user.id:
        abort(403)

    n.is_read = True
    db.session.commit()

    return redirect(n.link or url_for("main.index"))
