from functools import wraps
from flask import redirect, url_for
from flask_login import current_user
from flask_jwt_extended import verify_jwt_in_request, get_jwt


# 🔐 JWT ROLE PROTECTION (API)
def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if claims.get("role") != role:
                return {"error": "Access denied"}, 403

            return fn(*args, **kwargs)
        return decorated_function
    return wrapper


# 🔐 SESSION ROLE REDIRECT (WEB PAGES)
def redirect_if_wrong_role(role):
    def decorator(fn):
        @wraps(fn)
        def wrapped_function(*args, **kwargs):

            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))

            if current_user.role.name != role:
                if current_user.role.name == "admin":
                    return redirect(url_for("admin.admin_dashboard"))
                elif current_user.role.name == "supervisor":
                    return redirect(url_for("supervisor.dashboard"))
                else:
                    return redirect(url_for("main.user_dashboard"))

            return fn(*args, **kwargs)
        return wrapped_function
    return decorator
