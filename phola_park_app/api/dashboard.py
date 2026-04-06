from flask import Blueprint, jsonify
from datetime import datetime, timedelta

from flask_jwt_extended import get_jwt, get_jwt_identity
from phola_park_app.auth.jwt_guard import jwt_role_required

from phola_park_app.extensions import db
from phola_park_app.model import Report, User

dashboard_api = Blueprint("dashboard_api", __name__, url_prefix="/dashboard")


# ===============================
# USER DASHBOARD
# ===============================
@dashboard_api.route("", methods=["GET"])
@jwt_role_required("user")
def user_dashboard():
    user_id = get_jwt_identity()

    reports_count = Report.query.filter_by(user_id=user_id).count()

    recent_reports = (
        Report.query
        .filter_by(user_id=user_id)
        .order_by(Report.created_at.desc())
        .limit(5)
        .all()
    )

    return jsonify({
        "role": "user",
        "reports_count": reports_count,
        "recent_reports": [
            {
                "id": r.id,
                "category": r.category,
                "status": r.status,
                "created_at": r.created_at.isoformat()
            } for r in recent_reports
        ]
    })


# ===============================
# SUPERVISOR DASHBOARD
# ===============================
@dashboard_api.route("/supervisor", methods=["GET"])
@jwt_role_required("supervisor")
def supervisor_dashboard():
    claims = get_jwt()
    portfolio = claims.get("portfolio")

    total_reports = Report.query.filter_by(portfolio=portfolio).count()

    pending_reports = Report.query.filter_by(
        portfolio=portfolio,
        status="pending"
    ).count()

    return jsonify({
        "role": "supervisor",
        "portfolio": portfolio,
        "total_reports": total_reports,
        "pending_reports": pending_reports
    })


# ===============================
# ADMIN DASHBOARD
# ===============================
@dashboard_api.route("/admin", methods=["GET"])
@jwt_role_required("admin")
def admin_dashboard():
    total_users = User.query.count()
    total_reports = Report.query.count()

    last_7_days = datetime.utcnow() - timedelta(days=7)
    recent_reports = Report.query.filter(
        Report.created_at >= last_7_days
    ).count()

    return jsonify({
        "role": "admin",
        "total_users": total_users,
        "total_reports": total_reports,
        "reports_last_7_days": recent_reports
    })