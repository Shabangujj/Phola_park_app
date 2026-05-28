"""Admin module initialization."""
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from . import routes

__all__ = ['admin_bp']
