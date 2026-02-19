from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import func
from datetime import datetime, timedelta

from phola_park_app.model import Report

analytics_api = Blueprint("analytics_api", __name__, url_prefix="/analytics")

def apply_date_filters(query, date_field):
    days = request.args.get("days", type=int)
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        return query.filter(date_field >= start, date_field < end)

    if days:
        since = datetime.utcnow() - timedelta(days=days)
        return query.filter(date_field >= since)

    since = datetime.utcnow() - timedelta(days=7)
    return query.filter(date_field >= since)
@analytics_api.route("/reports-by-category", methods=["GET"])
@jwt_required()
def reports_by_category():
    claims = get_jwt()

    if claims.get("role") not in ["admin", "supervisor"]:
        return jsonify({"error": "Unauthorized"}), 403

    query = Report.query

    if claims.get("role") == "supervisor":
        query = query.filter_by(portfolio=claims.get("portfolio"))

    query = apply_date_filters(query, Report.created_at)

    results = (
        query.with_entities(Report.category, func.count(Report.id))
        .group_by(Report.category)
        .all()
    )

    return jsonify({
        "labels": [r[0] for r in results],
        "values": [r[1] for r in results]
    })
@analytics_api.route("/reports-by-status", methods=["GET"])
@jwt_required()
def reports_by_status():
    claims = get_jwt()

    if claims.get("role") not in ["admin", "supervisor"]:
        return jsonify({"error": "Unauthorized"}), 403

    query = Report.query

    if claims.get("role") == "supervisor":
        query = query.filter_by(portfolio=claims.get("portfolio"))

    query = apply_date_filters(query, Report.created_at)

    results = (
        query.with_entities(Report.status, func.count(Report.id))
        .group_by(Report.status)
        .all()
    )

    return jsonify({
        "labels": [r[0] for r in results],
        "values": [r[1] for r in results]
    })
@analytics_api.route("/reports-over-time", methods=["GET"])
@jwt_required()
def reports_over_time():
    claims = get_jwt()

    if claims.get("role") not in ["admin", "supervisor"]:
        return jsonify({"error": "Unauthorized"}), 403

    query = Report.query

    if claims.get("role") == "supervisor":
        query = query.filter_by(portfolio=claims.get("portfolio"))

    query = apply_date_filters(query, Report.created_at)

    results = (
        query.with_entities(
            func.date(Report.created_at),
            func.count(Report.id)
        )
        .group_by(func.date(Report.created_at))
        .order_by(func.date(Report.created_at))
        .all()
    )

    return jsonify({
        "labels": [str(r[0]) for r in results],
        "values": [r[1] for r in results]
    })
@analytics_api.route("/reports-by-portfolio", methods=["GET"])
@jwt_required()
def reports_by_portfolio():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"error": "Admin only"}), 403

    query = apply_date_filters(Report.query, Report.created_at)

    results = (
        query.with_entities(Report.portfolio, func.count(Report.id))
        .group_by(Report.portfolio)
        .all()
    )

    return jsonify({
        "labels": [r[0] for r in results],
        "values": [r[1] for r in results]
    })
