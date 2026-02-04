# phola_park_app/auth_helpers.py

from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user

from phola_park_app.extensions import db
from phola_park_app.model import UserRole


# ─────────────────────────────────────────────
# ROLE UTILITIES
# ─────────────────────────────────────────────

from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user


def role_required(*roles):
    """
    Restrict route access by role(s).

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

            if current_user.role.name not in roles:
                abort(403)

            return fn(*args, **kwargs)
        return wrapper
    return decorator

# ─────────────────────────────────────────────
# ROLE CHECK HELPERS
# ─────────────────────────────────────────────
def is_admin() -> bool:
    return current_user.is_authenticated and current_user.role.name == "admin"


def is_supervisor() -> bool:
    return current_user.is_authenticated and current_user.role.name == "supervisor"


def is_admin_or_supervisor() -> bool:
    return (
        current_user.is_authenticated and
        current_user.role.name in {"admin", "supervisor"}
    )



# ─────────────────────────────────────────────
# ROLE-BASED REDIRECT
# ─────────────────────────────────────────────
from flask_login import current_user
from flask import redirect, url_for

def _redirect_by_role():
    role = current_user.role.name

    if role == "admin":
        return redirect(url_for("admin.admin_dashboard"))
    elif role == "supervisor":
        return redirect(url_for("supervisor.dashboard"))
    else:
        return redirect(url_for("main.user_dashboard"))

from flask_login import current_user
from flask import redirect, url_for

def redirect_by_role():
    if current_user.role == "admin":
        return redirect(url_for("admin.admin_dashboard"))

    if current_user.role == "supervisor":
        return redirect(url_for("supervisor.supervisor_dashboard"))

    return redirect(url_for("user.dashboard"))

@role_required("admin", "supervisor", "user")
def notifications():
    ...
    # Example function to demonstrate role-based access
    pass
