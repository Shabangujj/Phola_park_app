"""Base form classes using WTForms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length


class BaseForm(FlaskForm):
    """Base form class with common settings."""
    class Meta:
        csrf = True


class LoginForm(BaseForm):
    """User login form."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(BaseForm):
    """User registration form."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class ReportForm(BaseForm):
    """Report submission form."""
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20)])
    report_type = SelectField('Report Type', choices=[('incident', 'Incident'), ('service', 'Service Request')])
    submit = SubmitField('Submit Report')
