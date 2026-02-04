from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired

class ReportForm(FlaskForm):
    submit = SubmitField('Submit Report')
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
