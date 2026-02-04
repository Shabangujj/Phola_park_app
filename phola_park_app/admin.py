# phola_park_app/admin.py
from phola_park_app.admin import get_all_user, create_user
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from phola_park_app.auth_helpers import role_required
from phola_park_app.extensions import db
from phola_park_app.model import User, Report, Notice, Announcement, report_id, portfolio_name
from werkzeug.security import generate_password_hash
from flask import abort

admin_bp = Blueprint("admin", __name__, template_folder="templates")

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.role.name != "admin":
            abort(430)
        return func(*args, **kwargs)
    return wrapper
@admin_bp.route("/admin/dashboard")
@login_required
@admin_required
@role_required("admin")
def admin_dashboard():
    if not current_user.role.name:
        abort(403)
    return render_template("admin_dashboard.html")

@admin_bp.route("/admin/home")
@login_required
@admin_required
@role_required("admin")
def admin_home():
    users = User.query.all()
    return render_template("admin_bp_home.html", users=users)

@admin_bp.route("/assign_role/<int:user_id>", methods=["POST"])
@login_required
@admin_required
@role_required("admin")
def assign_role(user_id):
    role = request.form.get("role")
    portfolio = request.form.get("portfolio")
    user = User.query.get_or_404(user_id)
    user.role = role
    user.portfolio = portfolio if role == "supervisor" else None
    db.session.commit()
    flash("Role updated", "success")
    return redirect(url_for("admin.admin_home"))
#------------------------------
# User Management
#------------------------
def get_all_user():
    """Return list of all registered users."""
    return User.query.all()

def get_user(user_id):
    """Find a sigle user by ID."""
    return User.query.get(int(user_id))
def create_user(name, email, pasword, role="user", portfolio=None):
    """Admin creates a new user manually."""
    if User.query.filter_by(email=email).first():
        return False,"Email already registered."
    
    user = user(
        name=name,
        email=email,
        role=role,
        portfolio=portfolio
    )
    user.set_password(pasword)
    db.session.add(user)
    db.session.commit()
    
    return True, "User created successfully."

def update_user(user_Id,name=None,role=None, portfolio=None):
    """Admin updates user info."""
    user = User.query.get(int(user_Id))
    if not user:
        return False, "User not found"
    
    if name:
        user.name = name
    if role:
        user.role = role
    if portfolio:
        user.portfolio = portfolio
        
    db.session.commit()
    return True, "User updated"
def delete_user(user_id):
    """Admin deletes a user."""
    user = User.query.get(int(user_id))
    if not user:
        return False, "User Not Found"
    db.session.delete(user)
    db.session.commit()
    return True, "User removed"

#----------------
#Reports Mangemant
#-----------------------

def  get_all_reports():
    """Returns every report submitted in the system."""
    return
Report.query.order_by(Report.timestamp.desc()).all()

def  get_reports_by_portfolio(portfolio_name):
    """Supervisor-specific filtering."""
    return
Report.query.filter_by(portfolio=portfolio_name).all()

def  get_reports():
    """view single report page."""
    return
Report.query.get(int(report_id))

def delete_report(report_id):
    """deletes a report."""
    report = Report.query.get(int(report_id))
    if not report:
        return False, "Report Not Found"
    db.session.delete(report)
    db.session.commit()
    return True, "Report removed"

#------------------------------
#---Annoncement and Notice
#-------------------------------

def create_announcement(message):
    """Adnim creates an announcement for all user."""
    ann = Announcement(message=message)
    db.session.add(ann)
    db.session.commit()
    return True, "Announcement posted."

def get_announcement():
    """Retrieve all announcement."""
    return
Announcement.query.order_by(Announcement.created_at.desc()).all()

def delete_announcement(ann_id):
    """Remove announcement."""
    ann = Announcement.query.get(int(ann_id))
    if not ann:
        return False, "Announcement not Found"
    
    db.session.delete(ann)
    db.session.commit()
    return False, "Notice post"
def get_notices():
    return
Notice.query.order_by(Notice.created_at.desc()).all()

def create_notice(message):
    """Admin post a notice."""
    nt = Notice(message=message)
    db.session.add(nt)
    db.session.commit()
    return True, "Notice posted."
def delete_notice(notice_id):
    nt = Notice.query.get(int(notice_id))
    if not nt:
        return False, "Notice not Found"
    
    db.session.delete(nt)
    db.session.commit()
    return True, "Notice Deleted"
#------------------
#----ADMIN DASHBOARD SUMMARY
#----------------------------------

def dashboard_summary():
    """Return counts for admin dashboard."""
    total_users = User.query.count()
    total_reports = Report.query.count()
    total_announcements = Announcement.query.count()
    total_notices = Notice.query.correlate()
    return {
        "total_users": total_users,
        "total_reports": total_reports,
        "total_announcements": total_announcements,
        "total_notice": total_notices
    }

