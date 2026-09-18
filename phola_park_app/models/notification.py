"""
JJCORETECH
Phola Park App

Notification Model
"""

from datetime import datetime

from phola_park_app.extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    message = db.Column(
        db.String(1000),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=True
    )

    role_target = db.Column(
        db.String(50),
        nullable=True
    )

    portfolio = db.Column(
        db.String(100),
        nullable=True
    )

    notification_type = db.Column(
        db.String(50),
        nullable=False,
        default="general"
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="notifications"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "user_id": self.user_id,
            "role_target": self.role_target,
            "portfolio": self.portfolio,
            "notification_type": self.notification_type,
            "is_read": self.is_read,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }

    def __repr__(self):
        return (
            f"<Notification "
            f"id={self.id} "
            f"title={self.title!r} "
            f"user_id={self.user_id}>"
        )