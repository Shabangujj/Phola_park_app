"""
JJCORETECH
Project Model
"""

from datetime import datetime

from phola_park_app.extensions import db


# =====================================================
# PROJECT
# =====================================================

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    status = db.Column(
        db.String(50),
        default="Planning",
        nullable=False
    )

    priority = db.Column(
        db.String(20),
        default="Medium",
        nullable=False
    )

    progress = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    budget = db.Column(
        db.Float,
        default=0.0
    )

    location = db.Column(
        db.String(200)
    )

    start_date = db.Column(
        db.Date
    )

    end_date = db.Column(
        db.Date
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
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    creator = db.relationship(
        "User",
        backref=db.backref(
            "projects_created",
            lazy=True
        )
    )

    # ==========================================
    # Helper Methods
    # ==========================================

    def start(self):
        self.status = "In Progress"

    def complete(self):
        self.status = "Completed"
        self.progress = 100

    def cancel(self):
        self.status = "Cancelled"

    def archive(self):
        self.status = "Archived"

    def update_progress(self, value):
        value = max(0, min(100, int(value)))
        self.progress = value

        if value == 100:
            self.status = "Completed"
        elif value > 0 and self.status == "Planning":
            self.status = "In Progress"

    @property
    def is_completed(self):
        return self.progress == 100

    @property
    def is_overdue(self):
        if self.end_date is None:
            return False

        return (
            self.progress < 100 and
            datetime.utcnow().date() > self.end_date
        )

    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            return (
                self.end_date -
                self.start_date
            ).days

        return None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "status": self.status,
            "priority": self.priority,
            "progress": self.progress,
            "budget": self.budget,
            "location": self.location,
            "created_by": self.created_by
        }

    def __repr__(self):
        return (
            f"<Project "
            f"{self.name}>"
        )