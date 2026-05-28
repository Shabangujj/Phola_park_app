"""Health check API endpoints."""
from flask import Blueprint, jsonify

health_api = Blueprint('health_api', __name__, url_prefix='/health')


@health_api.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0'
    }), 200


@health_api.route('/status', methods=['GET'])
def status():
    """Get system status."""
    return jsonify({
        'status': 'online',
        'timestamp': 'now'
    }), 200
