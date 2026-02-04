from flask import url_for
from flask_login import current_user

def home_url():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return url_for("admin.admin_dashboard")
        elif current_user.role == "supervisor":
            return url_for("supervisor.supervisor_dashboard")
        return url_for("user.dashboard")

    return url_for("auth.login")
