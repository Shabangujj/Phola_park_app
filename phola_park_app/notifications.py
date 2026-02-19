from phola_park_app.extensions import db
from flask_login import current_user
from phola_park_app.model import User, Notification


def notify_survey_submission(survey, user):
    

    supervisors = User.query.filter_by(
        role="supervisor",
        portfolio=survey.topic
    ).all()

    admins = User.query.filter_by(role="admin").all()

    for u in supervisors + admins:
        db.session.add(
            Notification(
                user_id=u.id,
                title="New Survey Submission",
                message=f"{survey.name} submitted by a user.",
                link="/supervisor/surveys"
            )
        )

    db.session.commit()

def unread_notification_count():
    if not current_user.is_authenticated:
        return 0

    return Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).count()
