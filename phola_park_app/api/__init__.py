from flask import Blueprint, Flask

api_bp = Blueprint("api", __name__, url_prefix="/api")

from .health import *
from .reports import *