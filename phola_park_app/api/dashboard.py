"""Dashboard API endpoints."""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

dashboard_api = Blueprint('dashboard_api', __name__, url_prefix='/dashboard')


@dashboard_api.route('/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics."""
    user_id = get_jwt_identity()
    # Implementation here
    return jsonify({
        'total_reports': 0,
        'pending_reports': 0,
        'active_surveys': 0
    }), 200


@dashboard_api.route('/recent-activity', methods=['GET'])
@jwt_required()
def get_recent_activity():
    """Get recent user activity."""
    user_id = get_jwt_identity()
    # Implementation here
    return jsonify({'activities': []}), 200
