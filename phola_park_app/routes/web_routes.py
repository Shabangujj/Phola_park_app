from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from phola_park_app.model import db, User, Report, Survey, Announcement
from datetime import datetime
from functools import wraps

web = Blueprint('web', __name__)
# =========================
# 🚪PUBLIC ROAD
# =========================
@web.route('/')
def home():
    return render_template('login.html')
# =========================
# 🔐 ROLE-BASED ACCESS
# =========================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first", "warning")
            return redirect(url_for('web.login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get('role') != role:
                flash("Access denied", "danger")
                return redirect(url_for('web.dashboard'))
            return f(*args, **kwargs)
        return wrapper
    return decorator


# =========================
# 🔑 AUTH ROUTES
# =========================
@web.route('/login')
def login_redirect():
    return redirect(url_for('login'))
@web.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            session['portfolio'] = user.portfolio

            return redirect(url_for('web.dashboard'))
        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html')


@web.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('web.login'))


# =========================
# 📊 DASHBOARD REDIRECT
# =========================
@web.route('/dashboard')
@login_required
def dashboard():
    role = session.get('role')

    if role == 'admin':
        return redirect(url_for('web.admin_dashboard'))
    elif role == 'supervisor':
        return redirect(url_for('web.supervisor_dashboard'))
    else:
        return redirect(url_for('web.user_dashboard'))


# =========================
# 👑 ADMIN DASHBOARD
# =========================
@web.route('/admin')
@login_required
@role_required('admin')
def admin_dashboard():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    users = User.query.all()

    return render_template('admin_dashboard.html', reports=reports, users=users)


# =========================
# 👨‍💼 SUPERVISOR DASHBOARD
# =========================
@web.route('/supervisor')
@login_required
@role_required('supervisor')
def supervisor_dashboard():
    portfolio = session.get('portfolio')

    reports = Report.query.filter_by(portfolio=portfolio).order_by(Report.created_at.desc()).all()

    return render_template('supervisor_dashboard.html', reports=reports)


# =========================
# 👤 USER DASHBOARD
# =========================
@web.route('/user')
@login_required
@role_required('user')
def user_dashboard():
    surveys = Survey.query.all()

    return render_template('user_dashboard.html', surveys=surveys)


# =========================
# 📝 SURVEYS
# =========================
@web.route('/survey/<int:survey_id>', methods=['GET', 'POST'])
@login_required
def take_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)

    if request.method == 'POST':
        response = request.form.get('response')

        new_report = Report(
            report_type="survey",
            description=response,
            survey_type=survey.title,
            portfolio=survey.portfolio,
            user_id=session.get('user_id'),
            created_at=datetime.utcnow()
        )

        db.session.add(new_report)
        db.session.commit()

        flash("Survey submitted successfully", "success")
        return redirect(url_for('web.user_dashboard'))

    return render_template('survey_form.html', survey=survey)


# =========================
# 📢 ADMIN UPLOAD SURVEY
# =========================
@web.route('/admin/add_survey', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_survey():
    if request.method == 'POST':
        title = request.form.get('title')
        portfolio = request.form.get('portfolio')

        new_survey = Survey(title=title, portfolio=portfolio)

        db.session.add(new_survey)
        db.session.commit()

        flash("Survey added", "success")
        return redirect(url_for('web.admin_dashboard'))

    return render_template('add_survey.html')


# =========================
# 🗑 DELETE SURVEY
# =========================
@web.route('/admin/delete_survey/<int:id>')
@login_required
@role_required('admin')
def delete_survey(id):
    survey = Survey.query.get_or_404(id)

    db.session.delete(survey)
    db.session.commit()

    flash("Survey deleted", "success")
    return redirect(url_for('web.admin_dashboard'))


# =========================
# 🚨 REPORT SUBMISSION
# =========================
@web.route('/report', methods=['GET', 'POST'])
@login_required
def submit_report():
    if request.method == 'POST':
        report_type = request.form.get('report_type')
        description = request.form.get('description')
        category = request.form.get('category')

        new_report = Report(
            report_type=report_type,
            description=description,
            category=category,
            portfolio=session.get('portfolio'),
            user_id=session.get('user_id'),
            created_at=datetime.utcnow()
        )

        db.session.add(new_report)
        db.session.commit()

        flash("Report submitted", "success")
        return redirect(url_for('web.dashboard'))

    return render_template('report_form.html')


# =========================
# 📂 VIEW REPORTS (ADMIN)
# =========================
@web.route('/admin/reports')
@login_required
@role_required('admin')
def admin_reports():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return render_template('admin_reports.html', reports=reports)


# =========================
# 📂 VIEW REPORTS (SUPERVISOR)
# =========================
@web.route('/supervisor/reports')
@login_required
@role_required('supervisor')
def supervisor_reports():
    portfolio = session.get('portfolio')

    reports = Report.query.filter_by(portfolio=portfolio).order_by(Report.created_at.desc()).all()

    return render_template('supervisor_reports.html', reports=reports)


# =========================
# ✏ EDIT REPORT (ADMIN)
# =========================
@web.route('/admin/edit_report/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_report(id):
    report = Report.query.get_or_404(id)

    if request.method == 'POST':
        report.description = request.form.get('description')
        report.category = request.form.get('category')

        db.session.commit()

        flash("Report updated", "success")
        return redirect(url_for('web.admin_reports'))

    return render_template('edit_report.html', report=report)


# =========================
# 🗑 DELETE REPORT
# =========================
@web.route('/admin/delete_report/<int:id>')
@login_required
@role_required('admin')
def delete_report(id):
    report = Report.query.get_or_404(id)

    db.session.delete(report)
    db.session.commit()

    flash("Report deleted", "success")
    return redirect(url_for('web.admin_reports'))