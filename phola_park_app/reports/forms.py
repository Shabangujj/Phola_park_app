from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    FileField,
    SubmitField
)
from wtforms.validators import DataRequired

class ReportForm(FlaskForm):

    title = StringField(
        "Issue Title",
        validators=[DataRequired()]
    )

    category = SelectField(
        "Category",
        choices=[
            ("Water", "Water"),
            ("Electricity", "Electricity"),
            ("Road Damage", "Road Damage"),
            ("Crime", "Crime"),
            ("Housing", "Housing"),
            ("Illegal Dumping", "Illegal Dumping"),
            ("Other", "Other")
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[DataRequired()]
    )

    image = FileField("Photo")

    submit = SubmitField(
        "Submit Report"
    )