from functools import wraps
from flask import abort
from flask_login import current_user, login_required


def role_required(*roles):
    """
    Restrict access to users with specific roles.
    Example:
        @role_required("admin")
        @role_required("admin", "supervisor")
    """

    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)  # Unauthorized

            if not hasattr(current_user, "role") or current_user.role is None:
                abort(403)  # Forbidden

            user_role = current_user.role.name

            if user_role not in roles:
                abort(403)  # Forbidden

            return f(*args, **kwargs)

        return decorated_function

    return decorator
from flask import redirect, url_for

def redirect_if_wrong_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if current_user.role.name != role:
                if current_user.role.name == "admin":
                    return redirect(url_for("admin.admin_dashboard"))
                elif current_user.role.name == "supervisor":
                    return redirect(url_for("supervisor.dashboard"))
                else:
                    return redirect(url_for("main.user_dashboard"))
            return f(*args, **kwargs)
        return wrapper
    return decorator
