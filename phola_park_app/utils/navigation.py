# 🔗 Navigation Helper Functions

from flask import url_for, redirect, session


# 🏠 HOME REDIRECT BASED ON ROLE
def home_url(role):
    """
    Returns dashboard URL based on user role
    """
    if role == "admin":
        return url_for("admin.admin_dashboard")
    elif role == "supervisor":
        return url_for("supervisor.dashboard")
    elif role == "user":
        return url_for("user.dashboard")
    else:
        return url_for("auth.login")


# 📊 DASHBOARD NAME (OPTIONAL - for UI titles)
def get_dashboard_name(role):
    if role == "admin":
        return "Admin Dashboard"
    elif role == "supervisor":
        return "Supervisor Dashboard"
    elif role == "user":
        return "User Dashboard"
    return "Dashboard"


# 🔐 ROLE CHECK HELPERS
def is_admin(role):
    return role == "admin"


def is_supervisor(role):
    return role == "supervisor"


def is_user(role):
    return role == "user"


# 📂 NAVIGATION LINKS (OPTIONAL ADVANCED)
def get_nav_links(role):
    """
    Returns navigation links based on role
    """
    if role == "admin":
        return [
            {"name": "Dashboard", "url": url_for("admin.admin_dashboard")},
            {"name": "Users", "url": url_for("admin.admin_users")},
            {"name": "Reports", "url": url_for("admin.view_reports")},
            {"name": "Announcements", "url": url_for("admin.announcements")},
            {"name": "Audit Logs", "url": url_for("admin.audit_logs")},
        ]

    elif role == "supervisor":
        return [
            {"name": "Dashboard", "url": url_for("supervisor.dashboard")},
            {"name": "Reports", "url": url_for("supervisor.reports")},
        ]

    elif role == "user":
        return [
            {"name": "Dashboard", "url": url_for("user.dashboard")},
            {"name": "Surveys", "url": url_for("user.surveys")},
            {"name": "Reports", "url": url_for("user.reports")},
        ]

    return redirect(home_url(session.get("role")))