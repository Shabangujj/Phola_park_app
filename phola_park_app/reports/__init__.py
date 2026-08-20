from flask import Blueprint

reports_bp = Blueprint(
    "reports",
    __name__,
    template_folder="../templates/reports"
)

from phola_park_app.reports import routes