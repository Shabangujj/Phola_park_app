"""
JJCORETECH
Report Models
"""

from datetime import datetime

from phola_park_app.extensions import db


# =====================================================
# REPORT
# =====================================================

class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    report_type = db.Column(
        db.String(120),
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    category = db.Column(
        db.String(120)
    )

    comment = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(255)
    )

    survey_type = db.Column(
        db.String(120)
    )

    portfolio = db.Column(
        db.String(100)
    )

    status = db.Column(
        db.String(30),
        default="Pending",
        nullable=False
    )

    location = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # ===============================
    # Foreign Keys
    # ===============================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    assigned_to = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id"
        ),
        nullable=True
    )

    # ===============================
    # Relationships
    # ===============================

    reporter = db.relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="reports"
    )

    assignee = db.relationship(
        "User",
        foreign_keys=[assigned_to],
        back_populates="assigned_reports"
    )

    notes = db.relationship(
        "ReportNote",
        back_populates="report",
        cascade="all, delete-orphan",
        lazy=True
    )

    # ===============================
    # Helper Methods
    # ===============================

    def assign(self, supervisor):
        self.assignee = supervisor
        self.status = "Assigned"

    def close(self):
        self.status = "Closed"

    def reopen(self):
        self.status = "Pending"

    @property
    def is_closed(self):
        return self.status == "Closed"

    @property
    def is_pending(self):
        return self.status == "Pending"

    @property
    def is_assigned(self):
        return self.assigned_to is not None

    def to_dict(self):

        return {

            "id": self.id,

            "title": self.title,

            "report_type": self.report_type,

            "category": self.category,

            "description": self.description,

            "portfolio": self.portfolio,

            "status": self.status,

            "location": self.location,

            "user_id": self.user_id,

            "assigned_to": self.assigned_to,

            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )

        }

    def __repr__(self):

        return f"<Report #{self.id} - {self.title}>"
    # =============================
    # REPORT NOTE MODEL
    #=============================

class ReportNote(db.Model):
    __tablename__ = "report_notes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    note = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    report_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "reports.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    report = db.relationship(
        "Report",
        back_populates="notes"
    )

    user = db.relationship(
        "User"
    )

    def __repr__(self):

        return f"<ReportNote {self.id}>"