"""
JJCORETECH
Audit Log Model
"""

from datetime import datetime

from phola_park_app.extensions import db


# =====================================================
# AUDIT LOG
# =====================================================

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    action = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    module = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    description = db.Column(
        db.Text
    )

    ip_address = db.Column(
        db.String(45)
    )

    user_agent = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    # ==========================================
    # Relationships
    # ==========================================

    user = db.relationship(
        "User",
        back_populates="audit_logs"
    )

    # ==========================================
    # Helper Methods
    # ==========================================

    @property
    def username(self):
        if self.user:
            return self.user.username
        return "System"

    @property
    def role(self):
        if self.user:
            return self.user.role_name
        return "System"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role,
            "module": self.module,
            "action": self.action,
            "description": self.description,
            "ip_address": self.ip_address,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }

    def __repr__(self):
        return (
            f"<AuditLog "
            f"{self.module}:{self.action}>"
        )