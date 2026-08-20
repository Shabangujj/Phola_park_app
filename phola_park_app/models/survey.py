"""
JJCORETECH
Survey Models
"""

from datetime import datetime

from phola_park_app.extensions import db


# =====================================================
# SURVEY
# =====================================================

class Survey(db.Model):
    __tablename__ = "surveys"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    survey_type = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    link = db.Column(
        db.String(255)
    )

    portfolio = db.Column(
        db.String(100)
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
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

    questions = db.relationship(
        "SurveyQuestion",
        back_populates="survey",
        cascade="all, delete-orphan",
        lazy=True
    )

    responses = db.relationship(
        "SurveyResponse",
        back_populates="survey",
        cascade="all, delete-orphan",
        lazy=True
    )

    @property
    def total_questions(self):
        return len(self.questions)

    @property
    def total_responses(self):
        return len(self.responses)

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def __repr__(self):
        return f"<Survey {self.title}>"
    # =====================================================
# SURVEY QUESTION
# =====================================================

class SurveyQuestion(db.Model):
    __tablename__ = "survey_questions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    survey_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "surveys.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    question_type = db.Column(
        db.String(30),
        nullable=False
    )

    options = db.Column(
        db.Text
    )

    order = db.Column(
        db.Integer,
        default=1
    )

    survey = db.relationship(
        "Survey",
        back_populates="questions"
    )

    answers = db.relationship(
        "SurveyAnswer",
        back_populates="question",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Question {self.id}>"
# =====================================================
# SURVEY RESPONSE
# =====================================================

class SurveyResponse(db.Model):
    __tablename__ = "survey_responses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    survey_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "surveys.id",
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

    submitted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    survey = db.relationship(
        "Survey",
        back_populates="responses"
    )

    user = db.relationship(
        "User",
        back_populates="survey_responses"
    )

    answers = db.relationship(
        "SurveyAnswer",
        back_populates="response",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<SurveyResponse {self.id}>"
# =====================================================
# SURVEY ANSWER
# =====================================================

class SurveyAnswer(db.Model):
    __tablename__ = "survey_answers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    response_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "survey_responses.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "survey_questions.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    value = db.Column(
        db.Text,
        nullable=False
    )

    response = db.relationship(
        "SurveyResponse",
        back_populates="answers"
    )

    question = db.relationship(
        "SurveyQuestion",
        back_populates="answers"
    )

    def __repr__(self):
        return f"<SurveyAnswer {self.id}>"
    