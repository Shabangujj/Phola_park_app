"""
JJCORETECH
Notice, Announcement & Committee Models
"""

from datetime import datetime

from phola_park_app.extensions import db


# =====================================================
# ANNOUNCEMENT
# =====================================================

class Announcement(db.Model):
    __tablename__ = "announcements"

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

    target_role = db.Column(
        db.String(50),
        nullable=True
    )

    portfolio = db.Column(
        db.String(100),
        nullable=True
    )

    priority = db.Column(
        db.String(20),
        default="Normal",
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    publish_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    expiry_date = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ----------------------------
    # Helper Methods
    # ----------------------------

    def publish(self):
        self.is_active = True

    def unpublish(self):
        self.is_active = False

    @property
    def is_expired(self):

        if self.expiry_date is None:
            return False

        return datetime.utcnow() > self.expiry_date

    def __repr__(self):
        return f"<Announcement {self.title}>"




# =====================================================
# NOTICE
# =====================================================

class Notice(db.Model):
    __tablename__ = "notices"

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

    target_group = db.Column(
        db.String(100),
        default="all"
    )

    portfolio = db.Column(
        db.String(100)
    )

    notice_type = db.Column(
        db.String(50),
        default="Notice"
    )

    priority = db.Column(
        db.String(20),
        default="Normal"
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    creator = db.relationship(
        "User",
        back_populates="notices"
    )

    # ----------------------------

    def publish(self):
        self.is_active = True

    def archive(self):
        self.is_active = False

    @property
    def is_notice(self):
        return self.notice_type.lower() == "notice"

    @property
    def is_alert(self):
        return self.notice_type.lower() == "alert"

    def __repr__(self):
        return f"<Notice {self.title}>"




# =====================================================
# COMMITTEE
# =====================================================

class Committee(db.Model):
    __tablename__ = "committees"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    portfolio = db.Column(
        db.String(100),
        nullable=False
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    creator = db.relationship(
        "User",
        back_populates="committees_created"
    )

    def __repr__(self):
        return f"<Committee {self.name}>"