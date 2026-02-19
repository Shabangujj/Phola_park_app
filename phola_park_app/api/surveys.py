from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from datetime import datetime

from phola_park_app.extensions import db
from phola_park_app.model import Survey, SurveyResponse

surveys_api = Blueprint("surveys_api", __name__, url_prefix="/surveys")
@surveys_api.route("", methods=["GET"])
@jwt_required()
def list_surveys():
    claims = get_jwt()

    if claims.get("role") != "user":
        return jsonify({"error": "Users only"}), 403

    surveys = Survey.query.filter_by(is_active=True).all()

    return jsonify([
        {
            "id": s.id,
            "title": s.title,
            "survey_type": s.survey_type,
            "created_at": s.created_at.isoformat()
        }
        for s in surveys
    ])
@surveys_api.route("/<int:survey_id>/submit", methods=["POST"])
@jwt_required()
def submit_survey(survey_id):
    claims = get_jwt()

    if claims.get("role") != "user":
        return jsonify({"error": "Users only"}), 403

    user_id = get_jwt_identity()
    data = request.get_json()

    # prevent duplicate submission
    existing = SurveyResponse.query.filter_by(
        survey_id=survey_id,
        user_id=user_id
    ).first()

    if existing:
        return jsonify({"error": "You already submitted this survey"}), 400

    response = SurveyResponse(
        survey_id=survey_id,
        user_id=user_id,
        answers=data.get("answers"),
        created_at=datetime.utcnow()
    )

    db.session.add(response)
    db.session.commit()

    return jsonify({"message": "Survey submitted"}), 201
@surveys_api.route("/<int:survey_id>/responses", methods=["GET"])
@jwt_required()
def survey_responses(survey_id):
    claims = get_jwt()

    if claims.get("role") not in ["admin", "supervisor"]:
        return jsonify({"error": "Unauthorized"}), 403

    responses = SurveyResponse.query.filter_by(survey_id=survey_id).all()

    return jsonify({
        "survey_id": survey_id,
        "count": len(responses),
        "responses": [
            {
                "user_id": r.user_id,
                "answers": r.answers,
                "created_at": r.created_at.isoformat()
            }
            for r in responses
        ]
    })
@surveys_api.route("", methods=["POST"])
@jwt_required()
def create_survey():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"error": "Admin only"}), 403

    data = request.get_json()

    survey = Survey(
        title=data["title"],
        survey_type=data["survey_type"],
        is_active=True,
        created_at=datetime.utcnow()
    )

    db.session.add(survey)
    db.session.commit()

    return jsonify({
        "message": "Survey created",
        "id": survey.id
    }), 201
