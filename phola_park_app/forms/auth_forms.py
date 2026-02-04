from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from wtforms import StringField, TextAreaField, SelectField, FileField, PasswordField
from phola_park_app.forms.report_form import ReportForm
class RegisterForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")]
    )
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
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
