"""
JJCORETECH
Phola Park App
Admin Blueprint
"""

from flask import Blueprint

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

# Import route modules
from .dashboard import *
from .users import *
from .reports import *
from .surveys import *
from .announcements import *
from .analytics import *
from .audit_logs import *
from .projects import *
from .settings import *