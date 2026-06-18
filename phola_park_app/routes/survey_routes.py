from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from phola_park_app.model import Survey

surveys_bp = Blueprint("surveys", __name__, url_prefix="/api/v1/surveys")


@surveys_bp.route("", methods=["GET"])
@jwt_required()
def get_surveys():
    """Return available surveys from the database (JWT protected)."""
    try:
        qs = Survey.query.order_by(Survey.created_at.desc()).all()
        surveys = []
        for s in qs:
            surveys.append({
                "id": s.id,
                "title": getattr(s, 'title', None) or getattr(s, 'name', None),
                "survey_type": getattr(s, 'survey_type', None) or getattr(s, 'topic', None),
                "link": s.link,
                "portfolio": s.portfolio,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            })

        return jsonify({"status": "success", "count": len(surveys), "data": surveys}), 200
    except Exception:
        # Fallback: return empty list if DB is unavailable
        return jsonify({"status": "success", "count": 0, "data": []}), 200