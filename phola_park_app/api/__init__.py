"""
====================================================
JJCORETECH
Phola Park App
REST API
====================================================
"""

from flask import Blueprint

api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)

