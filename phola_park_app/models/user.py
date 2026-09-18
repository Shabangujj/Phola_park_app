"""
JJCORETECH
Phola Park App

User and User Role Models
"""

from datetime import datetime

from flask_login import UserMixin

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from phola_park_app.extensions import db


# ============================================================
# USER ROLE
# ============================================================

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

    # --------------------------------------------------------
    # RELATIONSHIPS
    # --------------------------------------------------------

    users = db.relationship(
        "User",
        back_populates="role",
        lazy="dynamic"
    )

    def __repr__(self):

        return f"<UserRole {self.name}>"


# ============================================================
# USER
# ============================================================

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ========================================================
    # BASIC INFORMATION
    # ========================================================

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

    # ========================================================
    # AUTHENTICATION
    # ========================================================

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

    # ========================================================
    # ROLE
    # ========================================================

    role_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user_roles.id",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    role = db.relationship(
        "UserRole",
        back_populates="users"
    )

    # ========================================================
    # PORTFOLIO
    #
    # Admin:
    #     Can be None / Administration
    #
    # Supervisor:
    #     Must have a portfolio
    #
    # Community User:
    #     Can be None / Not Assigned
    # ========================================================

    portfolio = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    # ========================================================
    # TIMESTAMPS
    # ========================================================

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

    # ========================================================
    # REPORT RELATIONSHIPS
    # ========================================================

    # Reports created by this user
    reports = db.relationship(
        "Report",
        foreign_keys="Report.user_id",
        back_populates="reporter",
        cascade="all, delete-orphan",
        lazy=True
    )

    # Reports assigned to this user
    assigned_reports = db.relationship(
        "Report",
        foreign_keys="Report.assigned_to",
        back_populates="assignee",
        lazy=True
    )

    # ========================================================
    # NOTICE RELATIONSHIP
    # ========================================================

    notices = db.relationship(
        "Notice",
        back_populates="creator",
        cascade="all, delete-orphan",
        lazy=True
    )

    # ========================================================
    # COMMITTEE RELATIONSHIP
    # ========================================================

    committees_created = db.relationship(
        "Committee",
        back_populates="creator",
        lazy=True
    )

    # ========================================================
    # AUDIT LOG RELATIONSHIP
    # ========================================================

    audit_logs = db.relationship(
        "AuditLog",
        back_populates="user",
        lazy=True
    )

    # ========================================================
    # NOTIFICATION RELATIONSHIP
    # ========================================================

    notifications = db.relationship(
        "Notification",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # ========================================================
    # SURVEY RESPONSE RELATIONSHIP
    # ========================================================

    survey_responses = db.relationship(
        "SurveyResponse",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # ========================================================
    # PASSWORD METHODS
    # ========================================================

    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )

    # ========================================================
    # FLASK-LOGIN
    # ========================================================

    def get_id(self):

        return str(self.id)

    # ========================================================
    # ROLE HELPERS
    # ========================================================

    @property
    def role_name(self):

        if not self.role:
            return "user"

        return self.role.name.lower()

    def set_role(self, role_name):

        if not role_name:
            return False

        role = UserRole.query.filter(
            db.func.lower(UserRole.name)
            == role_name.lower()
        ).first()

        if not role:
            return False

        self.role = role

        return True

    # ========================================================
    # ROLE CHECKS
    # ========================================================

    @property
    def is_admin(self):

        return self.role_name == "admin"

    @property
    def is_supervisor(self):

        return self.role_name == "supervisor"

    @property
    def is_user(self):

        return self.role_name == "user"

    # ========================================================
    # PERMISSION HELPERS
    # ========================================================

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

    # ========================================================
    # PORTFOLIO HELPERS
    # ========================================================

    @property
    def has_portfolio(self):

        return bool(
            self.portfolio and
            self.portfolio.strip()
        )

    def assign_portfolio(self, portfolio):

        if portfolio is None:

            self.portfolio = None

            return

        portfolio = portfolio.strip()

        self.portfolio = (
            portfolio
            if portfolio
            else None
        )

    def clear_portfolio(self):

        self.portfolio = None

    # ========================================================
    # DISPLAY HELPERS
    # ========================================================

    @property
    def full_display_name(self):

        if self.full_name:
            return self.full_name

        return self.username

    # ========================================================
    # SERIALIZATION
    # ========================================================

    def to_dict(self, include_email=True):

        data = {
            "id": self.id,

            "full_name": self.full_name,

            "username": self.username,

            "phone": self.phone,

            "avatar": self.avatar,

            "email_verified": self.email_verified,

            "is_active": self.is_active,

            "role": self.role_name,

            "portfolio": self.portfolio,

            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),

            "updated_at": (
                self.updated_at.isoformat()
                if self.updated_at
                else None
            ),

            "last_login": (
                self.last_login.isoformat()
                if self.last_login
                else None
            )
        }

        if include_email:

            data["email"] = self.email

        return data

    # ========================================================
    # REPRESENTATION
    # ========================================================

    def __repr__(self):

        return (
            f"<User "
            f"id={self.id} "
            f"username={self.username} "
            f"role={self.role_name} "
            f"portfolio={self.portfolio}>"
        )