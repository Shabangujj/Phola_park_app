from flask import Blueprint, jsonify, session, redirect, url_for, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required  # type: ignore[reportMissingImports]
from phola_park_app.model import User, Report
reports_bp = Blueprint("reports", __name__, url_prefix="/reports")
@reports_bp.route("", methods=["GET"])
@jwt_required()
def get_reports():
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # 🔐 ADMIN → see everything
    if user.role == "admin":
        reports = Report.query.all()

    # 🔐 SUPERVISOR → see only their portfolio
    elif user.role == "supervisor":
        if not user.portfolio:
            return jsonify({"error": "No portfolio assigned"}), 403

        reports = Report.query.filter_by(portfolio=user.portfolio).all()

    # 🔐 USER → see only their own reports
    else:
        reports = Report.query.filter_by(user_id=user.id).all()

    # ✅ Convert to JSON
    result = []
    for r in reports:
        result.append({
            "id": r.id,
            "type": r.report_type,
            "description": r.description,
            "portfolio": r.portfolio,
            "user_id": r.user_id,
            "date": str(r.created_at),
            "status": r.status
        })

    return jsonify(result), 200