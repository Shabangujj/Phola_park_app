from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

surveys_bp = Blueprint("surveys", __name__, url_prefix="/api/v1/surveys")


@surveys_bp.route("", methods=["GET"])
@jwt_required()
def get_surveys():
    """
    Return available surveys
    """

    surveys = [
        {"id": 1, "title": "Community Safety Survey"},
        {"id": 2, "title": "Water & Sanitation Survey"},
        {"id": 3, "title": "Health Services Survey"},
    ]

    return jsonify({
        "status": "success",
        "count": len(surveys),
        "data": surveys
    }), 200