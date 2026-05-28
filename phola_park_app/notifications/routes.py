"""Notification routes."""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')


@notifications_bp.route('/')
@login_required
def list_notifications():
    """List all notifications for user."""
    return render_template('notifications/list.html')


@notifications_bp.route('/<int:notification_id>')
@login_required
def view_notification(notification_id):
    """View specific notification."""
    return render_template('notifications/view.html')


@notifications_bp.route('/send', methods=['POST'])
@login_required
def send_notification():
    """Send a notification."""
    # Logic here
    return jsonify({'status': 'sent'})
