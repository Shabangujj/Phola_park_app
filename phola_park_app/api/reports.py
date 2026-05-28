"""Reports API endpoints."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

reports_api = Blueprint('reports_api', __name__, url_prefix='/reports')


@reports_api.route('/', methods=['GET'])
@jwt_required()
def get_reports():
    """Get all reports."""
    # Implementation here
    return jsonify({'reports': []}), 200


@reports_api.route('/', methods=['POST'])
@jwt_required()
def create_report():
    """Create a new report."""
    data = request.get_json()
    # Implementation here
    return jsonify({'message': 'Report created'}), 201


@reports_api.route('/<int:report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    """Get specific report."""
    # Implementation here
    return jsonify({'report': {}}), 200
