from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from phola_park_app.model import Report, Survey, User
from phola_park_app.extensions import db

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/v1")

from phola_park_app.decorators import role_required

   
@dashboard_bp.route("", methods=["GET"])
@jwt_required()
@role_required("admin", "supervisor")
def dashboard():
    user_id = get_jwt_identity()

    # 🔹 total reports
    total_reports = Report.query.count()

    # 🔹 pending reports
    pending_reports = Report.query.filter_by(status="Pending").count()

    # 🔹 resolved reports
    resolved_reports = Report.query.filter_by(status="Resolved").count()

    # 🔹 available surveys
    total_surveys = Survey.query.count()

    # 🔹 current user info
    user = User.query.get(user_id)

    return jsonify({
        "status": "success",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role.name if user.role else "user"
        },
        "statistics": {
            "total_reports": total_reports,
            "pending_reports": pending_reports,
            "resolved_reports": resolved_reports,
            "total_surveys": total_surveys
        }
    }), 200