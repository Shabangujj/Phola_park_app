from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity
from flask_login import current_user
from ..auth.jwt_guard import jwt_access_required, jwt_role_required
from phola_park_app.model import Report, User, Notification
from phola_park_app.extensions import db
from datetime import datetime, timedelta
from phola_park_app.model import Notification


reports_api = Blueprint("reports_api", __name__, url_prefix="/reports")
reports_bp = Blueprint("reports", __name__)

@reports_api.route("", methods=["POST"], endpoint="create_report_api")
@jwt_role_required("user")
@jwt_access_required("user")
def create_report():
    data = request.get_json()

    required_fields = ["report_type", "category", "description", "survey_type", "portfolio"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    report = Report(
        report_type=data["report_type"],
        category=data["category"],
        description=data["description"],
        survey_type=data["survey_type"],
        portfolio=data["portfolio"],
        user_id=current_user.id,
        created_at=datetime.utcnow()
    )

    db.session.add(report)
    db.session.commit()
    # create supervisor notification
    notification = Notification(
    message=f"New report submitted: {report.report_type}",
    role_target="supervisor",
    portfolio=report.portfolio
)

    db.session.add(notification)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Report submitted",
        "report_id": report.id
    }), 201

@reports_api.route("/my", methods=["GET"], endpoint="my_reports_api")
@jwt_role_required("user")
@jwt_access_required("user")
def my_reports():
    reports = (
        Report.query
        .filter_by(user_id=current_user.id)
        .order_by(Report.created_at.desc())
        .all()
    )

    return jsonify({
        "count": len(reports),
        "reports": [
            {
                "id": r.id,
                "category": r.category,
                "description": r.description,
                "status": r.status,
                "created_at": r.created_at.isoformat()
            }
            for r in reports
        ]
    })

@reports_api.route("/portfolio/<string:portfolio>", methods=["GET"], endpoint="reports_by_portfolio_api")
@jwt_role_required("admin", "supervisor")
@jwt_access_required(min_role="supervisor", permission="view_reports")
def reports_by_portfolio(portfolio):
    reports = (
        Report.query
        .filter_by(portfolio=portfolio)
        .order_by(Report.created_at.desc())
        .all()
    )

    return jsonify({
        "portfolio": portfolio,
        "count": len(reports),
        "reports": [
            {
                "id": r.id,
                "category": r.category,
                "description": r.description,
                "status": r.status,
                "created_at": r.created_at.isoformat(),
                "user_id": r.user_id
            }
            for r in reports
        ]
    })

@reports_api.route("", methods=["GET"], endpoint="all_reports_api")
@jwt_role_required("admin")
@jwt_access_required("admin")
def all_reports():
    query = Report.query

    category = request.args.get("category")
    days = request.args.get("days", type=int)

    if category:
        query = query.filter_by(category=category)

    if days:
        since = datetime.utcnow() - timedelta(days=days)
        query = query.filter(Report.created_at >= since)

    reports = query.order_by(Report.created_at.desc()).all()

    return jsonify({
        "count": len(reports),
        "reports": [
            {
                "id": r.id,
                "category": r.category,
                "description": r.description,
                "status": r.status,
                "portfolio": r.portfolio,
                "created_at": r.created_at.isoformat()
            }
            for r in reports
        ]
    })
@reports_api.route("/<int:report_id>/status", methods=["PATCH"], endpoint="update_report_status_api")
@jwt_role_required("admin", "supervisor")
@jwt_access_required(min_role="supervisor", permission="edit_reports")
def update_report_status(report_id):
    data = request.get_json()
    status = data.get("status")

    if not status:
        return jsonify({"error": "status is required"}), 400
    supervisor_user = User.query.filter_by(id=current_user.id).first()
    report = Report.query.get_or_404(report_id)
    report.status = status
    notification = Notification(
    user_id=supervisor_user.id,  # REQUIRED
    title="New Report Submitted",
    message=f"New {report.category} report submitted in {report.portfolio}",
    created_at=datetime.utcnow()
)

    db.session.add(notification)
    db.session.commit()

    

    return jsonify({
        "status": "success",
        "message": "Report status updated"
    })    
@reports_bp.route("/", methods=["GET"])
@jwt_access_required()
def get_reports():
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role")

    # Query parameters
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    category = request.args.get("category")
    status = request.args.get("status")

    query = Report.query

    # Users see only their reports
    if role == "user":
        query = query.filter_by(user_id=user_id)

    # optional filters
    if category:
        query = query.filter_by(category=category)

    if status:
        query = query.filter_by(status=status)

    reports = query.order_by(Report.created_at.desc()) \
                   .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "total": reports.total,
        "pages": reports.pages,
        "current_page": page,
        "data": [r.to_dict() for r in reports.items]
    })
@reports_bp.route("/", methods=["POST"])
@jwt_access_required()
def create_report():
    data = request.get_json()
    user_id = get_jwt_identity()

    new_report = Report(
        report_type=data.get("report_type"),
        description=data.get("description"),
        category=data.get("category"),
        portfolio=data.get("portfolio"),
        user_id=user_id
    )

    db.session.add(new_report)
    db.session.commit()

    return jsonify({
        "message": "Report submitted successfully",
        "report": new_report.to_dict()
    }), 201
@reports_bp.route("/<int:report_id>", methods=["PUT"])
@jwt_access_required()
def update_report(report_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    role = get_jwt().get("role")

    report = Report.query.get_or_404(report_id)

    # users can only edit their own
    if role == "user" and report.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    report.description = data.get("description", report.description)
    report.category = data.get("category", report.category)
    report.portfolio = data.get("portfolio", report.portfolio)

    db.session.commit()

    return jsonify({
        "message": "Report updated",
        "report": report.to_dict()
    })
@reports_bp.route("/<int:report_id>", methods=["DELETE"])
@jwt_role_required("admin")
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)

    db.session.delete(report)
    db.session.commit()

    return jsonify({"message": "Report deleted"})
