from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime, timedelta

from phola_park_app.extensions import db
from phola_park_app.model import Report, SurveyResponse, User
from phola_park_app.decorators import role_required
from flask_jwt_extended import get_jwt_identity
from phola_park_app.auth.jwt_guard import jwt_role_required

dashboard_api = Blueprint("dashboard_api", __name__, url_prefix="/dashboard")

@dashboard_api.route(
    "",
    methods=["GET"],
    endpoint="user_dashboard_summary_api"
)

@jwt_role_required("user")
def user_dashboard_summary():
    reports_count = Report.query.filter_by(user_id=current_user.id).count()

    recent_reports = (
        Report.query
        .filter_by(user_id=current_user.id)
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

@dashboard_api.route(
    "/supervisor",
    methods=["GET"],
    endpoint="supervisor_dashboard_summary_api"
)
@jwt_role_required("supervisor")
def supervisor_dashboard_summary():
    portfolio = current_user.portfolio

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

@dashboard_api.route(
    "/admin",
    methods=["GET"],
    endpoint="admin_dashboard_summary_api"
)
@jwt_role_required("admin")
def admin_dashboard_summary():
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

from flask_jwt_extended import jwt_required, get_jwt
from phola_park_app.auth.jwt_guard import jwt_role_required

@dashboard_api.route(
    "",
    methods=["GET"],
    endpoint="user_dashboard_jwt_api"
)
@jwt_role_required("user")
def user_dashboard_jwt():
    claims = get_jwt()
    role = claims["role"]

    return jsonify({
        "message": "User dashboard",
        "role": role
    })

@dashboard_api.route(
    "/supervisor",
    methods=["GET"],
    endpoint="supervisor_dashboard_jwt_api"
)

@jwt_role_required("supervisor")
def supervisor_dashboard_jwt():
    claim = get_jwt()
    role = claim["role"]
    return jsonify({
        "message": "Supervisor dashboard",
        "role": role
    })

@dashboard_api.route(
    "/admin", 
    methods=["GET"],
    endpoint="admin_dashboard_jwt_api"
)

@jwt_role_required("admin")
def admin_dashboard_jwt():
    claim = get_jwt()
    role = claim["role"]
    return jsonify({
        "message": "Admin dashboard",
        "role": role
    })
