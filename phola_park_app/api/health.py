from flask import jsonify
from . import api_bp
from flask import Blueprint, jsonify
from phola_park_app.extensions import db
from sqlalchemy import text

health_api = Blueprint("health_api", __name__, url_prefix="/health")

@health_api.route(
    "",
    methods=["GET"],
    endpoint="health_check_api"
)
def health_check():
    try:
        # simple DB ping
        db.session.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    return jsonify({
        "status": "ok",
        "service": "Phola Park API",
        "database": db_status
    }), 200
