from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from phola_park_app.extensions import db
from phola_park_app.model import User
from phola_park_app.model import UserRole
from phola_park_app.decorators import role_required  # Make sure this import path is correct

admin_manage_bp = Blueprint('admin_manage', __name__)

@admin_manage_bp.route("/admin/assign-portfolio", methods=["GET", "POST"])
def admin_assign_portfolio():
    users = User.query.all()

    if request.method == "POST":
        user_id = request.form["user_id"]
        role = request.form["role"]
        portfolio = request.form.get("portfolio")

        new_role = UserRole(user_id=user_id, role=role, portfolio=portfolio)
        db.session.add(new_role)
        db.session.commit()

        return redirect(url_for("admin_manage.admin_assign_portfolio"))

    return render_template("admin_assign_portfolio.html", users=users)

@admin_manage_bp.route("/assign-portfolio", methods=["POST"])
@login_required
@role_required("admin")
def assign_portfolio():
    user_id = request.form.get("user_id")
    portfolio = request.form.get("portfolio")

    user = User.query.get_or_404(user_id)
    user.portfolio = portfolio

    db.session.commit()
    flash("Portfolio assigned", "success")
    return redirect(url_for("admin.users"))
