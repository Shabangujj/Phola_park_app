# Cleaned up auth_helpers to remove duplicate imports and fix role checks

from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user


def role_required(*roles):
    """Decorator to restrict route access by role(s).

    Usage:
        @role_required("admin")
        @role_required("admin", "supervisor")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in first.", "warning")
                return redirect(url_for("auth.login"))

            user_role = None
            try:
                # support both string roles and Role objects with .name
                user_role = getattr(current_user, "role")
                if hasattr(user_role, "name"):
                    user_role = user_role.name
            except Exception:
                user_role = None

            if user_role not in roles:
                abort(403)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def is_admin() -> bool:
    try:
        r = getattr(current_user, "role")
        return current_user.is_authenticated and (r == "admin" or getattr(r, "name", None) == "admin")
    except Exception:
        return False


def is_supervisor() -> bool:
    try:
        r = getattr(current_user, "role")
        return current_user.is_authenticated and (r == "supervisor" or getattr(r, "name", None) == "supervisor")
    except Exception:
        return False


def is_admin_or_supervisor() -> bool:
    return is_admin() or is_supervisor()


def redirect_by_role():
    """Redirect user to a view depending on their role."""
    try:
        r = getattr(current_user, "role")
        role_name = r if isinstance(r, str) else getattr(r, "name", None)
    except Exception:
        role_name = None

    if role_name == "admin":
        return redirect(url_for("admin.admin_dashboard"))
    if role_name == "supervisor":
        return redirect(url_for("supervisor.supervisor_dashboard"))
    return redirect(url_for("user.dashboard"))
