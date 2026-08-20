"""
JJCORETECH
User & UserRole Models
"""

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from phola_park_app.extensions import db


# =====================================================
# USER ROLE
# =====================================================

class UserRole(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    users = db.relationship(
        "User",
        back_populates="role",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<UserRole {self.name}>"


# =====================================================
# USER
# =====================================================

class User(UserMixin, db.Model):
    __tablename__ = "users"

    # -------------------------------------
    # Primary Key
    # -------------------------------------

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # -------------------------------------
    # Personal Information
    # -------------------------------------

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    username = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    phone = db.Column(
        db.String(20),
        nullable=True
    )

    avatar = db.Column(
        db.String(255),
        nullable=True
    )

    # -------------------------------------
    # Authentication
    # -------------------------------------

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    email_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # -------------------------------------
    # Authorization
    # -------------------------------------

    role_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user_roles.id",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    portfolio = db.Column(
        db.String(100),
        nullable=True
    )

    # -------------------------------------
    # Audit
    # -------------------------------------

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

    last_login = db.Column(
        db.DateTime,
        nullable=True
    )

    # -------------------------------------
    # Relationships
    # -------------------------------------

    role = db.relationship(
        "UserRole",
        back_populates="users"
    )

    reports = db.relationship(
        "Report",
        foreign_keys="Report.user_id",
        back_populates="reporter",
        cascade="all, delete-orphan",
        lazy=True
    )

    assigned_reports = db.relationship(
        "Report",
        foreign_keys="Report.assigned_to",
        back_populates="assignee",
        lazy=True
    )

    notices = db.relationship(
        "Notice",
        back_populates="creator",
        cascade="all, delete-orphan",
        lazy=True
    )

    committees_created = db.relationship(
        "Committee",
        back_populates="creator",
        lazy=True
    )

    audit_logs = db.relationship(
        "AuditLog",
        back_populates="user",
        lazy=True
    )

    notifications = db.relationship(
        "Notification",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    survey_responses = db.relationship(
        "SurveyResponse",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # -------------------------------------
    # Authentication Helpers
    # -------------------------------------

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    def get_id(self):
        return str(self.id)

    # -------------------------------------
    # Role Helpers
    # -------------------------------------

    @property
    def role_name(self):
        return (
            self.role.name.lower()
            if self.role
            else "user"
        )

    def set_role(self, role_name):

        role = UserRole.query.filter_by(
            name=role_name.lower()
        ).first()

        if role is None:
            raise ValueError(
                f"Role '{role_name}' does not exist."
            )

        self.role = role

    @property
    def is_admin(self):
        return self.role_name == "admin"

    @property
    def is_supervisor(self):
        return self.role_name == "supervisor"

    @property
    def is_user(self):
        return self.role_name == "user"

    # -------------------------------------
    # Permission Helpers
    # -------------------------------------

    def can_manage_users(self):
        return self.is_admin

    def can_manage_reports(self):
        return self.is_admin or self.is_supervisor

    def can_manage_surveys(self):
        return self.is_admin

    def can_manage_settings(self):
        return self.is_admin

    def can_manage_projects(self):
        return self.is_admin

    # -------------------------------------
    # Display Helpers
    # -------------------------------------

    def full_display_name(self):
        return f"{self.full_name} (@{self.username})"

    # -------------------------------------
    # API Helper
    # -------------------------------------

    def to_dict(self):

        return {

            "id": self.id,

            "full_name": self.full_name,

            "username": self.username,

            "email": self.email,

            "phone": self.phone,

            "avatar": self.avatar,

            "role": self.role_name,

            "portfolio": self.portfolio,

            "email_verified": self.email_verified,

            "is_active": self.is_active,

            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),

            "last_login": (
                self.last_login.isoformat()
                if self.last_login
                else None
            )

        }

    # -------------------------------------
    # Representation
    # -------------------------------------

    def __repr__(self):

        return (
            f"<User "
            f"id={self.id}, "
            f"username='{self.username}', "
            f"role='{self.role_name}'>"
        )
        