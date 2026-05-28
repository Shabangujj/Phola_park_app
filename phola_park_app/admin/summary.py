"""Admin summary and statistics."""
from phola_park_app.extensions import db
from phola_park_app.model import User


def get_user_count():
    """Get total user count."""
    return User.query.count()


def get_admin_statistics():
    """Get admin dashboard statistics."""
    return {
        'total_users': get_user_count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'pending_reports': 0,  # Implement based on your Report model
    }
