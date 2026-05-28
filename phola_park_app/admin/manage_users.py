"""User management functionality for admin."""
from phola_park_app.extensions import db
from phola_park_app.model import User


def get_all_users():
    """Fetch all users."""
    return User.query.all()


def get_user_by_id(user_id):
    """Fetch user by ID."""
    return User.query.get(user_id)


def update_user_role(user_id, new_role):
    """Update user role."""
    user = User.query.get(user_id)
    if user:
        user.role = new_role
        db.session.commit()
        return True
    return False


def delete_user(user_id):
    """Delete a user."""
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
