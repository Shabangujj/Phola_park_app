from flask import Blueprint, jsonify
from phola_park_app.extensions import db

health_bp = Blueprint("health", __name__, url_prefix="/api/v1")


@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    API & database health check
    """

    try:
        db.session.execute("SELECT 1")
        database_status = "ok"
    except Exception:
        database_status = "error"

    return jsonify({
        "status": "ok",
        "service": "Phola Park API",
        "database": database_status
    }), 200