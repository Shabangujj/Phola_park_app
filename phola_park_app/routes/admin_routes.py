from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from phola_park_app.decorators import role_required
from phola_park_app.models import AuditLog, User, Survey, Report, Announcement, UserRole, Project
from datetime import datetime, date, timedelta
from functools import wraps
from flask_login import current_user

from phola_park_app.routes.web_routes import login_required
from phola_park_app.extensions import db
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# =========================
# 🔐 ADMIN ACCESS ONLY
# =========================
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first", "warning")
            return redirect(url_for('auth.login'))

        if session.get('role') != 'admin':
            flash("Admin access only", "danger")
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)
    return wrapper

from flask import jsonify
from flask_login import login_required
from sqlalchemy import func

from phola_park_app.models import (
    User,
    Report,
    Survey,
    Announcement
)
from phola_park_app.decorators import role_required


@admin_bp.route("/admin/dashboard/cards")
@login_required
@role_required("Admin")
def dashboard_cards():
    total_users = User.query.count()
    total_reports = Report.query.count()
    total_surveys = Survey.query.count()
    total_announcements = Announcement.query.count()

    pending_reports = Report.query.filter_by(status="Pending").count()
    in_progress_reports = Report.query.filter_by(status="In Progress").count()
    resolved_reports = Report.query.filter_by(status="Resolved").count()

    rejected_reports = Report.query.filter_by(status="Rejected").count()
    completed_reports = Report.query.filter_by(status="Completed").count()

    return jsonify({
        "total_users": total_users,
        "total_reports": total_reports,
        "total_surveys": total_surveys,
        "total_announcements": total_announcements,
        "pending_reports": pending_reports,
        "in_progress_reports": in_progress_reports,
        "resolved_reports": resolved_reports,
        "rejected_reports": rejected_reports,
        "completed_reports": completed_reports
    })
# =========================
# 👑 ADMIN DASHBOARD
# =========================
@admin_bp.route('/')
@admin_required
@login_required
def dashboard():
    page = request.args.get("page", 1, type=int)
    users = User.query.paginate(page=page, per_page=10, error_out=False)
    reports = Report.query.order_by(Report.created_at.desc()).all()
    surveys = Survey.query.all()
    stats = {  # Placeholder stats
        "total_users": User.query.count(),
        "total_reports": Report.query.count(),
        "surveys": Survey.query.count(),
        "announcements": Announcement.query.count()
    }

    return render_template(
        'admin/admin_dashboard.html',
        stats=stats,
        users=users,
        reports=reports,
        surveys=surveys,
        announcements=Announcement.query.order_by(Announcement.created_at.desc()).all()
       
    )

from flask import render_template
from flask_login import login_required
from sqlalchemy import func

from phola_park_app.models import (
    User,
    Report,
    Survey,
    Announcement
)
from phola_park_app.decorators import role_required


@admin_bp.route("/admin/analytics-dashboard")
@login_required
@role_required("Admin")
def analytics_dashboard():
    # Dashboard Statistics
    total_users = User.query.count()
    total_reports = Report.query.count()
    total_surveys = Survey.query.count()
    total_announcements = Announcement.query.count()

    pending_reports = Report.query.filter_by(status="Pending").count()
    in_progress_reports = Report.query.filter_by(status="In Progress").count()
    resolved_reports = Report.query.filter_by(status="Resolved").count()

    # Reports by Category
    category_stats = (
        db.session.query(
            Report.category,
            func.count(Report.id)
        )
        .group_by(Report.category)
        .all()
    )

    categories = [c[0] for c in category_stats]
    category_counts = [c[1] for c in category_stats]

    # Reports by Portfolio
    portfolio_stats = (
        db.session.query(
            Report.portfolio,
            func.count(Report.id)
        )
        .group_by(Report.portfolio)
        .all()
    )

    portfolios = [p[0] for p in portfolio_stats]
    portfolio_counts = [p[1] for p in portfolio_stats]

    return render_template(
        "admin/analytics_dashboard.html",
        total_users=total_users,
        total_reports=total_reports,
        total_surveys=total_surveys,
        total_announcements=total_announcements,
        pending_reports=pending_reports,
        in_progress_reports=in_progress_reports,
        resolved_reports=resolved_reports,
        categories=categories,
        category_counts=category_counts,
        portfolios=portfolios,
        portfolio_counts=portfolio_counts,
    )
# =========================
# 👥 VIEW USERS
# =========================
@admin_bp.route('/admin/users')
@login_required
@role_required("admin")
def view_users():
    page = request.args.get("page", 1, type=int)
    users = User.query.order_by(User.id).paginate(
        page=page,
        per_page=10,
        error_out=False
    )
    return render_template('admin/users.html', users=users)
# =========================
# paginate users
# =========================
@admin_bp.route("/admin/users")
@login_required
@role_required("admin")
def users():

    page = request.args.get("page", 1, type=int)

    users = User.query.order_by(User.id).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    return render_template(
        "admin/users.html",
        users=users
    )

# =========================
# ➕ ADD USER
# =========================
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from phola_park_app.model import db, User, UserRole


# =========================
# ➕ ADD USER
# =========================
# =========================
# ✏ EDIT USER
# =========================
@admin_bp.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form.get('username')
        user.role = request.form.get('role')
        user.portfolio = request.form.get('portfolio')

        db.session.commit()

        flash("User updated", "success")
        return redirect(url_for('admin.view_users'))

    return render_template('admin/edit_user.html', user=user)
# =========================
# 📋 ADMIN REPORTS
# =========================
@admin_bp.route("/admin_reports")
@login_required
@admin_required
def admin_reports():

    search = request.args.get("search", "")
    category = request.args.get("category", "")
    status = request.args.get("status", "")
    portfolio = request.args.get("portfolio", "")
    days = request.args.get("days", "")

    query = Report.query

    # Search
    if search:
        query = query.filter(
            Report.description.contains(search)
        )

    # Category
    if category:
        query = query.filter_by(category=category)

    # Status
    if status:
        query = query.filter_by(status=status)

    # Portfolio
    if portfolio:
        query = query.filter_by(portfolio=portfolio)

    # Date Filter
    if days:
        try:
            date_limit = datetime.utcnow() - timedelta(days=int(days))
            query = query.filter(Report.created_at >= date_limit)
        except ValueError:
            pass

    reports = query.order_by(
        Report.created_at.desc()
    ).all()

    # Dashboard Statistics
    total_reports = Report.query.count()

    pending_reports = Report.query.filter_by(
        status="Pending"
    ).count()

    assigned_reports = Report.query.filter_by(
        status="Assigned"
    ).count()

    in_progress_reports = Report.query.filter_by(
        status="In Progress"
    ).count()

    resolved_reports = Report.query.filter_by(
        status="Resolved"
    ).count()

    closed_reports = Report.query.filter_by(
        status="Closed"
    ).count()

    # Portfolio Chart Data
    portfolio_counts = {}

    for report in reports:
        key = report.portfolio or "Unknown"
        portfolio_counts[key] = portfolio_counts.get(key, 0) + 1

    return render_template(
        "admin_reports.html",
        reports=reports,
        portfolio_counts=portfolio_counts,
        total_reports=total_reports,
        pending_reports=pending_reports,
        assigned_reports=assigned_reports,
        in_progress_reports=in_progress_reports,
        resolved_reports=resolved_reports,
        closed_reports=closed_reports
    )
# =========================
# 📊 VIEW REPORTS
# =========================
@admin_bp.route("/admin/view_reports")
@login_required
@admin_required
def view_reports():

    search = request.args.get("search")
    category = request.args.get("category")
    status = request.args.get("status")
    portfolio = request.args.get("portfolio")
    days = request.args.get("days")

    query = Report.query

    if days:
        date_limit = datetime.utcnow() - timedelta(days=int(days))
        query = query.filter(Report.created_at >= date_limit)

    if search:
        query = query.filter(
            Report.description.contains(search)
        )

    if category:
        query = query.filter_by(category=category)

    if status:
        query = query.filter_by(status=status)

    if portfolio:
        query = query.filter_by(portfolio=portfolio)

    reports = query.order_by(
        Report.created_at.desc()
    ).all()

    portfolio_counts = {}

    for report in reports:
        key = report.portfolio or "Unknown"
        portfolio_counts[key] = portfolio_counts.get(key, 0) + 1

    return render_template(
        "admin/view_reports.html",
        reports=reports,
        portfolio_counts=portfolio_counts
    )
@admin_bp.route("/admin/report/<int:report_id>")
@login_required
@admin_required
def view_report(report_id):

    report = Report.query.get_or_404(report_id)

    return render_template(
        "admin/view_report.html",
        report=report
    ) 
# =========================
# ✏ EDIT REPORT
# =========================
 
@admin_bp.route(
    "/admin/report/<int:report_id>/edit",
    methods=["GET","POST"]
)
@login_required
@admin_required
def edit_report(report_id):

    report = Report.query.get_or_404(report_id)

    if request.method == "POST":

        report.title = request.form["title"]

        report.category = request.form["category"]

        report.description = request.form["description"]

        report.portfolio = request.form["portfolio"]

        report.location = request.form["location"]

        report.comment = request.form["comment"]

        db.session.commit()

        flash(
            "Report updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "admin.view_report",
                report_id=report.id
            )
        )

    return render_template(
        "admin/edit_report.html",
        report=report
    )
   
# =========================
# 🗑 DELETE REPORT
# =========================

@admin_bp.route("/admin/report/<int:report_id>/delete")
@login_required
@admin_required
def delete_report(report_id):

    report = Report.query.get_or_404(report_id)

    db.session.delete(report)

    db.session.commit()

    flash(
        "Report deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.view_reports")
    )
# =========================
# Export reports CSV
# =========================
@admin_bp.route("/export_reports")
def export_reports():
    from flask import Response, session, redirect, url_for

    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    reports = Report.query.all()

    def generate():
        yield "ID,Type,Description,Portfolio,User,Date\n"
        for r in reports:
            yield f"{r.id},{r.report_type},{r.description},{r.portfolio},{r.user_id},{r.created_at}\n"

    return Response(generate(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=reports.csv"})

# =========================
# 📝 VIEW SURVEYS
# =========================
from flask import render_template, request
from flask_login import login_required

# Import your models
from phola_park_app.model import Survey

@admin_bp.route("/admin/surveys")
@login_required
@admin_required
def admin_surveys():
    """Admin - View all surveys"""

    surveys = Survey.query.order_by(
        Survey.created_at.desc()
    ).all()

    return render_template(
        "admin/admin_surveys.html",
        surveys=surveys
    )
# =========================
# ➕ ADD SURVEY
# =========================
@admin_bp.route("/add_survey", methods=["GET", "POST"])
def add_survey():
    from flask import render_template, request, redirect, url_for, flash, session

    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        survey_type = request.form.get("survey_type")

        new_survey = Survey(
            title=title,
            description=description,
            survey_type=survey_type
        )

        db.session.add(new_survey)
        db.session.commit()

        flash("Survey created successfully", "success")
        return redirect(url_for("main.admin_dashboard"))

    return render_template("admin/add_survey.html")
# =========================
# ➕ CREATE SURVEY
# =========================
@admin_bp.route("/admin/surveys/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_survey():

    if request.method == "POST":

        survey = Survey(
            title=request.form.get("title"),
            survey_type=request.form.get("survey_type"),
            description=request.form.get("description"),
            portfolio=request.form.get("portfolio"),
            link=request.form.get("link")
        )

        db.session.add(survey)
        db.session.commit()

        flash("Survey created successfully.", "success")

        return redirect(url_for("admin.admin_surveys"))

    return render_template("admin/create_survey.html")

# =========================
# 🗑 DELETE SURVEY
# =========================
@admin_bp.route('/delete_survey/<int:id>')
@admin_required
def delete_survey(id):
    survey = Survey.query.get_or_404(id)

    db.session.delete(survey)
    db.session.commit()

    flash("Survey deleted", "success")
    return redirect(url_for('admin.view_surveys'))
# =========================
# ✏️ EDIT SURVEY
# =========================
@admin_bp.route("/admin/surveys/<int:id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_survey(id):

    survey = Survey.query.get_or_404(id)

    if request.method == "POST":

        survey.title = request.form.get("title")
        survey.description = request.form.get("description")
        survey.survey_type = request.form.get("survey_type")
        survey.portfolio = request.form.get("portfolio")
        survey.link = request.form.get("link")

        db.session.commit()

        flash("Survey updated successfully.", "success")

        return redirect(url_for("admin.admin_surveys"))

    return render_template(
        "admin/edit_survey.html",
        survey=survey
    )
# =========================
# 🚨EXPORT REPORTS CSV
# =========================
import csv
from flask import Response
from io import StringIO
from datetime import datetime

@admin_bp.route('/export_reports_csv')
def export_reports_csv():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))

    reports = Report.query.all()

    si = StringIO()
    writer = csv.writer(si)

    # Header
    writer.writerow([
        "ID", "Type", "Description", "Category",
        "Portfolio", "User ID", "Date"
    ])

    # Data
    for r in reports:
        writer.writerow([
            r.id,
            r.report_type,
            r.description,
            r.category,
            r.portfolio,
            r.user_id,
            r.created_at.strftime("%Y-%m-%d")
        ])

    output = si.getvalue()

    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=reports.csv"
        }
    )
    # =========================
    # ANNOUNCEMENTS MANAGEMENT
    # =========================
@admin_bp.route('/announcements', methods=['GET', 'POST'])
def announcements():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        portfolio = request.form.get('portfolio')

        new_announcement = Announcement(
            title=title,
            message=message,
            portfolio=portfolio
        )

        db.session.add(new_announcement)
        db.session.commit()

        flash("Announcement created successfully!", "success")
        return redirect(url_for('admin.announcements'))

    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()

    return render_template(
        'admin/announcements.html',
        announcements=announcements
    )
    # =========================
# 📢 ADMIN ANNOUNCEMENTS
# =========================
@admin_bp.route("/admin/announcements")
@login_required
@admin_required
def admin_announcements():

    announcements = Announcement.query.order_by(
        Announcement.created_at.desc()
    ).all()

    return render_template(
        "admin/admin_announcements.html",
        announcements=announcements
    )
    # =========================
    # DELETE ANNOUNCEMENT
    # =========================
@admin_bp.route("/delete_announcement/<int:announcement_id>", methods=["POST"])
def delete_announcement(announcement_id):

    # 🔒 Only admin allowed
    if session.get("role") != "admin":
        flash("Unauthorized access", "danger")
        return redirect(url_for("auth.login"))

    announcement = Announcement.query.get_or_404(announcement_id)

    try:
        db.session.delete(announcement)
        db.session.commit()
        flash("Announcement deleted successfully", "success")
    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)
        flash("Error deleting announcement", "danger")

    return redirect(url_for("admin.announcements"))
# =========================
# EDIT ANNOUNCEMENT
# =========================
@admin_bp.route("/edit_announcement/<int:announcement_id>", methods=["GET", "POST"])
def edit_announcement(announcement_id):

    # 🔒 Only admin allowed
    if session.get("role") != "admin":
        flash("Unauthorized access", "danger")
        return redirect(url_for("auth.login"))

    announcement = Announcement.query.get_or_404(announcement_id)

    if request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("message")

        # ✅ Update fields
        announcement.title = title
        announcement.message = message

        try:
            db.session.commit()
            flash("Announcement updated successfully", "success")
        except Exception as e:
            db.session.rollback()
            print("ERROR:", e)
            flash("Error updating announcement", "danger")

        return redirect(url_for("admin.announcements"))

    return render_template("admin/edit_announcement.html", announcement=announcement)
# =========================
# ADMIN USER
# =========================
@admin_bp.route('/users')
def admin_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))

    users = User.query.all()

    return render_template(
        'admin/users.html',
        users=users
    )
# =========================
# DELETE USER
# =========================
@admin_bp.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully", "success")
    return redirect(url_for('admin.admin_users'))
# =========================
# ASSIGN PORTFOLIO
# =========================
@admin_bp.route("/assign_portfolio/<int:user_id>", methods=["POST"])
def assign_portfolio(user_id):

    portfolio = request.form.get("portfolio")

    user = User.query.get(user_id)

    if not user:
        flash("User not found", "danger")
        return redirect(url_for("admin.users"))

    # ✅ Update correct field
    user.portfolio = portfolio

    try:
        db.session.commit()
        print(f"UPDATED USER: {user.id} -> {user.portfolio}")
        flash("Portfolio assigned successfully", "success")
    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)
        flash("Failed to assign portfolio", "danger")
    print("FORM DATA:", request.form)
    return redirect(url_for("admin.admin_users"))
# =========================
# assign role
# =========================
@admin_bp.route("/assign_role/<int:user_id>", methods=["POST"])
def assign_role(user_id):
    from flask import request, redirect, url_for, flash
    from phola_park_app.model import User, UserRole
    from phola_park_app.extensions import db

    user = User.query.get_or_404(user_id)

    # Get role from form OR API
    new_role_name = request.form.get("role") or request.json.get("role")

    if not new_role_name:
        flash("No role provided", "danger")
        return redirect(url_for("admin.admin_users"))

    # 🔍 Find role object
    role = UserRole.query.filter_by(name=new_role_name).first()

    if not role:
        flash("Invalid role selected", "danger")
        return redirect(url_for("admin.admin_users"))

    # ✅ Assign role object (FIX)
    user.role = role

    db.session.commit()

    flash(f"{user.email} is now {new_role_name}", "success")

    return redirect(url_for("admin.admin_users"))
# =========================
# update routes
# =========================
@admin_bp.route("/update_report_status/<int:report_id>", methods=["POST"])
def update_report_status(report_id):
    from flask import request, redirect, url_for, session, flash

    if session.get("role") not in ["admin", "supervisor"]:
        return redirect(url_for("auth.login"))

    report = Report.query.get_or_404(report_id)
    new_status = request.form.get("status")

    report.status = new_status
    db.session.commit()

    flash("Status updated", "success")
    return redirect(url_for("admin.view_reports"))
# ===============
# AUDIT LOGS
# =================
from sqlalchemy import func
from collections import defaultdict
from flask import request, Response
from datetime import datetime
import csv

@admin_bp.route("/audit-logs")
@login_required
@admin_required
def audit_logs():
    from phola_park_app.model import AuditLog
    
    query = AuditLog.query
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()

    # 📊 Logs per day
    logs_per_day = db.session.query(
        func.date(AuditLog.timestamp),
        func.count(AuditLog.id)
    ).group_by(func.date(AuditLog.timestamp)).all()

    dates = [str(row[0]) for row in logs_per_day]
    counts = [row[1] for row in logs_per_day]

    # 📊 Actions breakdown
    actions_data = db.session.query(
        AuditLog.action,
        func.count(AuditLog.id)
    ).group_by(AuditLog.action).all()

    action_labels = [row[0] for row in actions_data]
    action_counts = [row[1] for row in actions_data]

    # 🔢 Total logs
    total_logs = AuditLog.query.count()

    # 👤 Unique users (active users)
    active_users = db.session.query(
        func.count(func.distinct(AuditLog.user_id))
    ).scalar()

    # 🔁 Most common action
    most_common = db.session.query(
        AuditLog.action,
        func.count(AuditLog.id).label("count")
    ).group_by(AuditLog.action).order_by(func.count(AuditLog.id).desc()).first()

    most_common_action = most_common[0] if most_common else "N/A"

    # 📅 Today's logs
    today = date.today()
    today_logs = db.session.query(func.count(AuditLog.id)).filter(
        func.date(AuditLog.timestamp) == today
    ).scalar()

    # 🔍 FILTERS
    action = request.args.get("action")
    user_id = request.args.get("user_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    query = db.session.query(AuditLog)

    if action:
        query = query.filter(AuditLog.action == action)

    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    if start_date:
        query = query.filter(AuditLog.timestamp >= datetime.strptime(start_date, "%Y-%m-%d"))

    if end_date:
        query = query.filter(AuditLog.timestamp <= datetime.strptime(end_date, "%Y-%m-%d"))

    logs = query.order_by(AuditLog.timestamp.desc()).all()
    return render_template(
        "admin/audit_logs.html",
        logs=logs,
        dates=dates,
        counts=counts,
        action_labels=action_labels,
        action_counts=action_counts,
        total_logs=total_logs,
        active_users=active_users,
        most_common_action=most_common_action,
        today_logs=today_logs
    )
# ==================
# LOGS DELETES
# =====================
@admin_bp.route("/delete_audit_log/<int:log_id>", methods=["POST"])
@login_required
@admin_required
def delete_audit_log(log_id):
    from phola_park_app.model import AuditLog
    from phola_park_app.extensions import db
    from flask import redirect, url_for, flash

    log = AuditLog.query.get_or_404(log_id)

    db.session.delete(log)
    db.session.commit()

    flash("Audit log deleted", "success")
    return redirect(url_for("admin.audit_logs"))
# ==================
# audit log export
# ==================
@admin_bp.route("/audit-logs/export")
@login_required
@admin_required
def export_audit_logs():

    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()

    def generate():
        yield "User,Action,Description,Date\n"

        for log in logs:
            user = log.user.username if log.user else "N/A"
            yield f"{user},{log.action},{log.description},{log.timestamp}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=audit_logs.csv"}
    )
    ## =========================
    ## Project management (placeholder)
    ## =========================
@admin_bp.route("/projects")
@login_required
def admin_projects():
    projects = Project.query.all()
    return render_template("admin_projects.html", projects=projects)


@admin_bp.route("/add_project", methods=["GET", "POST"])
@login_required
def add_project():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        image = request.form.get("image")
        link = request.form.get("link")

        new_project = Project(
            title=title,
            description=description,
            image=image,
            link=link
        )

        db.session.add(new_project)
        db.session.commit()

        flash("Project added successfully", "success")
        return redirect(url_for("admin.admin_projects"))

    return render_template("add_project.html")
@admin_bp.route("/edit_project/<int:id>", methods=["GET", "POST"])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)

    if request.method == "POST":
        project.title = request.form.get("title")
        project.description = request.form.get("description")
        project.image = request.form.get("image")
        project.link = request.form.get("link")

        db.session.commit()

        flash("Project updated successfully", "success")
        return redirect(url_for("admin.admin_projects"))

    return render_template("edit_project.html", project=project)
@admin_bp.route("/delete_project/<int:id>")
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)

    db.session.delete(project)
    db.session.commit()

    flash("Project deleted successfully", "danger")
    return redirect(url_for("admin.admin_projects"))