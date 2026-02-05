from flask import jsonify
from . import api_bp

@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "Phola Park API",
        "version": "1.0"
    }), 200
