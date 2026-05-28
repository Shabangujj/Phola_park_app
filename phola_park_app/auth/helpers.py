"""Authentication helper functions."""
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    """Hash a password for storage."""
    return generate_password_hash(password)


def verify_password(hashed_password, password):
    """Verify a password against its hash."""
    return check_password_hash(hashed_password, password)


def is_valid_email(email):
    """Check if email format is valid."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
