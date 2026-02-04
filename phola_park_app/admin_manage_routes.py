from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from phola_park_app.extensions import db
from phola_park_app.model import User
from phola_park_app.model import UserRole, Notice, Report

admin_manage_bp = Blueprint('admin_manage_bp', __name__)

@admin_manage_bp.route("/manage/users")
def users_list():
    users = User.query.all()
    roles = UserRole.query.all()
    return render_template("admin_users.html", users=users, roles=roles)

@admin_manage_bp.route("/manage/notices")
def manage_notices():
    notices = Notice.query.order_by(Notice.created_at.desc()).all()
    return render_template("admin_view_notices.html", notices=notices)

@admin_manage_bp.route("/manage/reports")
def all_reports():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return render_template("admin_reports.html", reports=reports)

@admin_manage_bp.route("/manage/announcement", methods=["GET","POST"])
def create_announcement():
    if request.method == "POST":
        msg = request.form["message"]
        new_notice = Notice(message=msg)
        db.session.add(new_notice)
        db.session.commit()
        return redirect(url_for("admin_manage.manage_notices"))

    return render_template("admin_create_announcement.html")

@admin_manage_bp.route("/manage/export", methods=["GET"])
def export_all_data():
    users = User.query.all()
    reports = Report.query.all()
    notices = Notice.query.all()

    return "Export function will generate CSV files here."
