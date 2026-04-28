from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from phola_park_app.decorators import role_required
from phola_park_app.model import db, User, Survey, Report, Announcement, UserRole
from datetime import datetime
from functools import wraps

from phola_park_app.routes.web_routes import login_required

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


# =========================
# 👑 ADMIN DASHBOARD
# =========================
@admin_bp.route('/')
@admin_required
def dashboard():
    users = User.query.all()
    reports = Report.query.order_by(Report.created_at.desc()).all()
    surveys = Survey.query.all()
    stats = {  # Placeholder stats
        "users": len(users),
        "reports": len(reports),
        "surveys": len(surveys),
        "announcements": Announcement.query.count()
    }

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        users=users,
        reports=reports,
        surveys=surveys,
        announcements=Announcement.query.order_by(Announcement.created_at.desc()).all()
       
    )


# =========================
# 👥 VIEW USERS
# =========================
@admin_bp.route('/users')
@admin_required
def view_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)


# =========================
# ➕ ADD USER
# =========================
@admin_bp.route('/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        portfolio = request.form.get('portfolio')

        new_user = User(
            username=username,
            password=password,  # ⚠️ replace with hashing later
            role=role,
            portfolio=portfolio
        )

        db.session.add(new_user)
        db.session.commit()

        flash("User added successfully", "success")
        return redirect(url_for('admin.view_users'))

    return render_template('admin/admin_user.html')


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
# 📊 VIEW REPORTS
# =========================
@admin_bp.route("/view_reports")
def view_reports():
    from flask import render_template, request, session, redirect, url_for
    from datetime import datetime, timedelta

    if session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    portfolio = request.args.get("portfolio")
    days = request.args.get("days")

    query = Report.query

    # 📅 Date filter
    if days:
        days = int(days)
        date_limit = datetime.utcnow() - timedelta(days=days)
        query = query.filter(Report.created_at >= date_limit)

    # 📂 Portfolio filter
    if portfolio:
        query = query.filter_by(portfolio=portfolio)

    reports = query.all()

    # 📊 Count per portfolio (for charts)
    portfolio_counts = {}
    for r in reports:
        key = r.portfolio or "Unknown"
        portfolio_counts[key] = portfolio_counts.get(key, 0) + 1

    return render_template(
        "admin/view_reports.html",
        reports=reports,
        portfolio_counts=portfolio_counts
    )
# =========================
# ✏ EDIT REPORT
# =========================
@admin_bp.route('/edit_report/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_report(id):
    report = Report.query.get_or_404(id)

    if request.method == 'POST':
        report.description = request.form.get('description')
        report.category = request.form.get('category')

        db.session.commit()

        flash("Report updated", "success")
        return redirect(url_for('admin.view_reports'))

    return render_template('admin/edit_report.html', report=report)


# =========================
# 🗑 DELETE REPORT
# =========================
@admin_bp.route('/delete_report/<int:id>')
@admin_required
def delete_report(id):
    report = Report.query.get_or_404(id)

    db.session.delete(report)
    db.session.commit()

    flash("Report deleted", "success")
    return redirect(url_for('admin.view_reports'))
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
@admin_bp.route('/surveys')
@admin_required
def view_surveys():
    surveys = Survey.query.all()
    return render_template('admin/surveys.html', surveys=surveys)


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
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("admin/add_survey.html")

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
@admin_bp.route("/audit_logs")
@login_required
@role_required("admin")
def audit_logs():
    from phola_park_app.model import AuditLog
    from flask import render_template, request

    action = request.args.get("action")
    user_id = request.args.get("user_id")

    query = AuditLog.query

    # 🔍 Filter by action
    if action:
        query = query.filter(AuditLog.action == action)

    # 🔍 Filter by user
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    logs = query.order_by(AuditLog.timestamp.desc()).all()

    return render_template("admin/audit_logs.html", logs=logs)
# ================================
# EXPORT AUDIT LOGS(CVS$PDF)
# ================================
@admin_bp.route("/export_audit_logs")
@login_required
@role_required("admin")
def export_audit_logs():
    from phola_park_app.model import AuditLog
    from flask import Response

    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()

    def generate():
        yield "ID,Action,Description,User,Date\n"
        for log in logs:
            yield f"{log.id},{log.action},{log.description},{log.user_id},{log.timestamp}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=audit_logs.csv"}
    )
    # ==================
    # LOGS DELETES
    # =====================
@admin_bp.route("/delete_audit_log/<int:log_id>", methods=["POST"])
@login_required
@role_required("admin")
def delete_audit_log(log_id):
    from phola_park_app.model import AuditLog
    from phola_park_app.extensions import db
    from flask import redirect, url_for, flash

    log = AuditLog.query.get_or_404(log_id)

    db.session.delete(log)
    db.session.commit()

    flash("Audit log deleted", "success")
    return redirect(url_for("admin.audit_logs"))