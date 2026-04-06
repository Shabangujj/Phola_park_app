from functools import wraps
from flask import redirect, url_for, jsonify
from flask_login import current_user
from flask_jwt_extended import verify_jwt_in_request, get_jwt

# ======================================================
# 🔐 JWT ROLE PROTECTION (FOR APIs)
# ======================================================

def api_role_required(*roles):
    """
    Protect API routes using JWT roles
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()

            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in roles:
                return jsonify({
                    "error": "Forbidden",
                    "message": "You do not have permission"
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper


# ======================================================
# 🔐 SESSION ROLE PROTECTION (WEB PAGES)
# ======================================================

def role_required(*roles):
    """
    Protect web routes based on logged-in user role
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):

            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))

            user_role = getattr(current_user.role, "name", current_user.role)

            if user_role not in roles:
                return redirect_user_dashboard(user_role)

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


# ======================================================
# 🔄 SMART REDIRECT BASED ON ROLE
# ======================================================

def redirect_user_dashboard(role):
    if role == "admin":
        return redirect(url_for("admin.admin_dashboard"))
    elif role == "supervisor":
        return redirect(url_for("supervisor.dashboard"))
    else:
        return redirect(url_for("user.user_dashboard"))