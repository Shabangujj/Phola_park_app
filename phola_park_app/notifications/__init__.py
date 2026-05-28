"""Notifications module initialization."""
from flask import Blueprint

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

from . import routes

__all__ = ['notifications_bp']
