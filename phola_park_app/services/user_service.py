"""User business logic service."""
from phola_park_app.extensions import db
from phola_park_app.model import User
from .base_service import BaseService


class UserService(BaseService):
    """Service for user-related operations."""
    
    def __init__(self):
        super().__init__(User, db)
    
    def get_by_email(self, email):
        """Get user by email."""
        return User.query.filter_by(email=email).first()
    
    def get_by_role(self, role):
        """Get all users with specific role."""
        return User.query.filter_by(role=role).all()
    
    def get_active_users(self):
        """Get all active users."""
        return User.query.filter_by(is_active=True).all()
