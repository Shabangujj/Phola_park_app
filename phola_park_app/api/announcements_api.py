from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from phola_park_app.model import Announcement, db
from datetime import datetime

announcements_api = Blueprint("announcements_api", __name__)

@announcements_api.route("/announcements", methods=["POST"])
@jwt_required()
def create_announcement():
    claims = get_jwt()
    role = claims.get("role")

    if role not in ["admin", "supervisor"]:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    announcement = Announcement(
        title=data.get("title"),
        message=data.get("message"),
        target=data.get("target", "all"),  # all or portfolio
        portfolio=data.get("portfolio"),
        created_by=get_jwt_identity(),
        created_at=datetime.utcnow()
    )

    db.session.add(announcement)
    db.session.commit()

    return jsonify({"message": "Announcement created"}), 201

@announcements_api.route("/announcements", methods=["GET"])
@jwt_required()
def get_announcements():
    claims = get_jwt()
    portfolio = claims.get("portfolio")

    announcements = Announcement.query.filter(
        (Announcement.target == "all") |
        (Announcement.portfolio == portfolio)
    ).order_by(Announcement.created_at.desc()).all()

    return jsonify([
        {
            "id": a.id,
            "title": a.title,
            "message": a.message,
            "portfolio": a.portfolio,
            "date": a.created_at
        }
        for a in announcements
    ])

@announcements_api.route("/announcements/all", methods=["GET"])
@jwt_required()
def all_announcements():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"error": "Admin only"}), 403

    announcements = Announcement.query.all()

    return jsonify([
        {
            "id": a.id,
            "title": a.title,
            "target": a.target,
            "portfolio": a.portfolio,
            "date": a.created_at
        }
        for a in announcements
    ])

@announcements_api.route("/announcements/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_announcement(id):
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"error": "Admin only"}), 403

    announcement = Announcement.query.get_or_404(id)

    db.session.delete(announcement)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"})
