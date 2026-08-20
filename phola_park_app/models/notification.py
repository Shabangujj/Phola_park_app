"""
JJCORETECH
Notification Model
"""

from datetime import datetime

from phola_park_app.extensions import db


# =====================================================
# NOTIFICATION
# =====================================================

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
        db.Text,
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
        default="general",
        nullable=False
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

    # =============================================
    # Helper Methods
    # =============================================

    def mark_as_read(self):
        self.is_read = True

    def mark_as_unread(self):
        self.is_read = False

    @property
    def is_global(self):
        return (
            self.user_id is None and
            self.role_target is None
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
            f"{self.id}: {self.title}>"
        )
