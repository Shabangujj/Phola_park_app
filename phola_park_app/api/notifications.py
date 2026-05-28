"""Notifications API endpoints."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

notifications_api = Blueprint('notifications_api', __name__, url_prefix='/notifications')


@notifications_api.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get user notifications."""
    # Implementation here
    return jsonify({'notifications': []}), 200


@notifications_api.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(notification_id):
    """Mark notification as read."""
    # Implementation here
    return jsonify({'message': 'Marked as read'}), 200
