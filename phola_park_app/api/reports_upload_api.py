from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from phola_park_app.model import Report
from phola_park_app.extensions import db
from phola_park_app.utils.upload_utils import save_file
from flask import current_app

reports_upload_api = Blueprint(
    "reports_upload_api",
    __name__,
    url_prefix="/reports"
)

@reports_upload_api.route("/<int:report_id>/upload", methods=["POST"])
@jwt_required()
def upload_report_image(report_id):
    user_id = get_jwt_identity()
    claims = get_jwt()

    report = Report.query.get_or_404(report_id)

    # user can upload only to own report
    if claims.get("role") == "user" and report.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    if "image" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["image"]
    filename = save_file(file)

    if not filename:
        return jsonify({"error": "Invalid file type"}), 400

    report.image = filename
    db.session.commit()

    return jsonify({
        "message": "Image uploaded",
        "filename": filename
    })
@reports_upload_api.route("/image/<filename>", methods=["GET"])
def view_image(filename):
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )
