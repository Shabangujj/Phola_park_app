"""Admin helper functions."""


def check_admin_permission(user):
    """Check if user is admin."""
    return user and user.role == 'admin'


def check_supervisor_permission(user):
    """Check if user is supervisor."""
    return user and user.role in ['admin', 'supervisor']


def validate_role(role):
    """Validate user role."""
    valid_roles = ['admin', 'supervisor', 'resident']
    return role in valid_roles
