from functools import wraps
from flask import abort
from flask_login import current_user
from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)

            if not current_user.role or current_user.role.name != role_name:
                abort(403)

            return f(*args, **kwargs)
        return wrapped
    return decorator

def supervisor_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.role not in ("supervisor", "admin"):
            abort(403)
        return func(*args, **kwargs)
    return wrapper
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.role != "admin":
            abort(403)
        return func(*args, **kwargs)
    return wrapper

def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.role != "user":
            abort(403)
        return func(*args, **kwargs)
    return wrapper

def admin_or_supervisor_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.role not in ("admin", "supervisor"):
            abort(403)
        return func(*args, **kwargs)
    return wrapper

def any_role_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        return func(*args, **kwargs)
    return wrapper

            
        