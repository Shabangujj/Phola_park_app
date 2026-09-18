
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length,TextAreaField, SelectField, FileField
from phola_park_app.forms.report_form import ReportForm
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length
)


class RegisterForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=3, max=150)
        ]
    )

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=120)
        ]
    )

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )

    submit = SubmitField("Register")
from wtforms import BooleanField


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")
class ReportForm(FlaskForm):
    report_type = StringField("Report Type", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[
            ("Water", "Water"),
            ("Electricity", "Electricity"),
            ("Crime", "Crime"),
            ("Health", "Health")
        ],
        validators=[DataRequired()]
    )
    description = TextAreaField("Description", validators=[DataRequired()])
    portfolio = SelectField(
        "Portfolio",
        choices=[
            ("Water", "Water"),
            ("Health", "Health"),
            ("Safety", "Safety"),
            ("Infrastructure", "Infrastructure")
        ],
        validators=[DataRequired()]
    )
    image = FileField("Image")
"""Compatibility wrapper — moved to phola_park_app.forms.base_forms

Deprecated: use phola_park_app.forms.base_forms
"""

import warnings

warnings.warn(
    "phola_park_app.forms is deprecated as a flat module; use phola_park_app.forms.base_forms",
    DeprecationWarning,
)

from phola_park_app.forms.base_forms import *  # noqa: F401,F403

