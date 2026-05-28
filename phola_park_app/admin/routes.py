"""Admin routes and dashboards."""
from flask import Blueprint, render_template
from flask_login import login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard."""
    return render_template('admin/dashboard.html')


@admin_bp.route('/users')
@login_required
def manage_users():
    """Manage users page."""
    return render_template('admin/users.html')


@admin_bp.route('/portfolios')
@login_required
def manage_portfolios():
    """Manage portfolios page."""
    return render_template('admin/portfolios.html')


@admin_bp.route('/reports')
@login_required
def manage_reports():
    """Manage reports page."""
    return render_template('admin/reports.html')
