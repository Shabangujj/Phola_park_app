from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


from phola_park_app.decorators import role_required

reports_bp = Blueprint("reports", __name__, url_prefix="/api/v1/reports")

@reports_bp.route("", methods=["GET"])
@role_required("admin", "supervisor")
@role_required("user")
def get_reports():
    """
    Return reports for logged-in user
    """

    user_id = get_jwt_identity()

    reports = [
        {
            "id": 1,
            "type": "Water Leak",
            "status": "Pending",
            "user_id": user_id
        },
        {
            "id": 2,
            "type": "Street Light Fault",
            "status": "Resolved",
            "user_id": user_id
        }
    ]

    return jsonify({
        "status": "success",
        "count": len(reports),
        "data": reports
    }), 200