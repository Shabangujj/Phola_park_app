# phola_park_app/model.py
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db

# ───────────────────────────────────────────
# USER ROLE MODEL
# ───────────────────────────────────────────
class UserRole(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship("User", back_populates="role", lazy="dynamic")

    def __repr__(self):
        return f"<UserRole {self.name}>"


# ───────────────────────────────────────────
# USER MODEL
# ───────────────────────────────────────────
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    # 🔑 ROLE FK
    role_id = db.Column(
        db.Integer,
        db.ForeignKey("user_roles.id", ondelete="RESTRICT"),
        nullable=False
    )
    is_active = db.Column(db.Boolean, default=True)

    # ✅ SINGLE, CORRECT RELATIONSHIP
    role = db.relationship("UserRole", back_populates="users")

    # supervisor-only
    portfolio = db.Column(db.String(50), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    reports = db.relationship("Report", backref="user", lazy=True)
    notices = db.relationship("Notice", backref="creator", lazy=True)

    # ───────────────
    # AUTH HELPERS
    # ───────────────
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # ───────────────
    # ROLE HELPERS (SAFE)
    # ───────────────
    @property
    def role_name(self) -> str:
        return self.role.name if self.role else "user"

    @property
    def is_admin(self) -> bool:
        return self.role_name == "admin"

    @property
    def is_supervisor(self) -> bool:
        return self.role_name == "supervisor"

    @property
    def is_user(self) -> bool:
        return self.role_name == "user"

    def __repr__(self):
        return f"<User {self.email} ({self.role_name})>"

# ───────────────────────────────────────────
# REPORT MODEL
# ───────────────────────────────────────────
class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)

    report_type = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120))
    description = db.Column(db.Text)

    image = db.Column(db.String(255))

    survey_type = db.Column(db.String(120))
    portfolio = db.Column(db.String(50))

    comment = db.Column(db.Text)
    status = db.Column(db.String(20), default="Pending", nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    def __repr__(self):
        return f"<Report {self.id}>"


# ───────────────────────────────────────────
# SURVEY MODEL
# ───────────────────────────────────────────
class Survey(db.Model):
    __tablename__ = "surveys"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    topic = db.Column(db.String(50), nullable=False)  # Water, Health, Crime, etc.
    created_at = db.Column(db.DateTime, default=db.func.now())

    questions = db.relationship(
        "SurveyQuestion",
        backref="survey",
        cascade="all, delete-orphan"
    )
class SurveyQuestion(db.Model):
    __tablename__ = "survey_questions"

    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey("surveys.id"), nullable=False)

    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(30), nullable=False)  
    # rating, multiple_choice, text, yes_no

    options = db.Column(db.Text, nullable=True)  
    # JSON string for MC options

    order = db.Column(db.Integer, default=0)
class SurveyResponse(db.Model):
    __tablename__ = "survey_responses"

    id = db.Column(db.Integer, primary_key=True)

    survey_id = db.Column(db.Integer, db.ForeignKey("surveys.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    submitted_at = db.Column(db.DateTime, default=db.func.now())

    survey = db.relationship("Survey", backref="responses")
    user = db.relationship("User", backref="survey_responses")
class SurveyAnswer(db.Model):
    __tablename__ = "survey_answers"

    id = db.Column(db.Integer, primary_key=True)

    response_id = db.Column(
        db.Integer,
        db.ForeignKey("survey_responses.id"),
        nullable=False
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey("survey_questions.id"),
        nullable=False
    )

    value = db.Column(db.Text, nullable=False)

    response = db.relationship("SurveyResponse", backref="answers")
    question = db.relationship("SurveyQuestion")


# ───────────────────────────────────────────
# ANNOUNCEMENTS
# ───────────────────────────────────────────
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="notifications")

    created_at = db.Column(db.DateTime, default=db.func.now())
    is_read = db.Column(db.Boolean, default=False)
    target_role = db.Column(db.String(50), default="all")
    link = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f"<Notification {self.title}>"
    
class Announcement(db.Model):
    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

    target_role = db.Column(db.String(20), nullable=True)  
    # admin / supervisor / user / None (all)

    portfolio = db.Column(db.String(50), nullable=True)  
    # Optional: Water, Electricity, etc.

    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<Announcement {self.id}>"

# ───────────────────────────────────────────
# NOTICES
# ───────────────────────────────────────────
class Notice(db.Model):
    __tablename__ = "notices"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

    target_group = db.Column(db.String(100), default="all")
    portfolio = db.Column(db.String(120))
    notice_type = db.Column(db.String(20), default="notice")

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notice {self.title}>"
