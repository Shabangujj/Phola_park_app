"""
JJCORETECH
Phola Park App

Admin Report Management Routes
"""

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required

from sqlalchemy import or_

from . import admin_bp

from phola_park_app.decorators import role_required
from phola_park_app.models import Report, User
from phola_park_app.extensions import db


# =====================================================
# ALL REPORTS
# =====================================================

@admin_bp.route("/reports", methods=["GET"])
@login_required
@role_required("admin")
def reports():

    # -------------------------------------------------
    # GET FILTERS
    # -------------------------------------------------

    search = request.args.get(
        "search",
        "",
        type=str
    ).strip()

    status = request.args.get(
        "status",
        "",
        type=str
    ).strip()

    category = request.args.get(
        "category",
        "",
        type=str
    ).strip()

    portfolio = request.args.get(
        "portfolio",
        "",
        type=str
    ).strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )


    # -------------------------------------------------
    # BASE QUERY
    # -------------------------------------------------

    query = Report.query


    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------

    if search:

        query = query.filter(
            or_(
                Report.title.ilike(
                    f"%{search}%"
                ),

                Report.description.ilike(
                    f"%{search}%"
                ),

                Report.category.ilike(
                    f"%{search}%"
                )
            )
        )


    # -------------------------------------------------
    # STATUS
    # -------------------------------------------------

    if status:

        query = query.filter(
            Report.status == status
        )


    # -------------------------------------------------
    # CATEGORY
    # -------------------------------------------------

    if category:

        query = query.filter(
            Report.category == category
        )


    # -------------------------------------------------
    # PORTFOLIO
    # -------------------------------------------------

    if portfolio:

        query = query.filter(
            Report.portfolio == portfolio
        )


    # -------------------------------------------------
    # PAGINATION
    # -------------------------------------------------

    reports = db.paginate(
        query.order_by(
            Report.created_at.desc()
        ),
        page=page,
        per_page=10,
        error_out=False
    )


    # -------------------------------------------------
    # STATUS OPTIONS
    # -------------------------------------------------

    statuses = [
        "Pending",
        "Assigned",
        "In Progress",
        "Resolved",
        "Closed",
    ]


    # -------------------------------------------------
    # CATEGORY OPTIONS
    # -------------------------------------------------

    categories = [
        row[0]
        for row in (
            db.session.query(
                Report.category
            )
            .filter(
                Report.category.isnot(None)
            )
            .distinct()
            .order_by(
                Report.category
            )
            .all()
        )
    ]


    # -------------------------------------------------
    # PORTFOLIO OPTIONS
    # -------------------------------------------------

    portfolios = [
        row[0]
        for row in (
            db.session.query(
                Report.portfolio
            )
            .filter(
                Report.portfolio.isnot(None)
            )
            .distinct()
            .order_by(
                Report.portfolio
            )
            .all()
        )
    ]


    # -------------------------------------------------
    # DEBUG CHECK
    # -------------------------------------------------

    print(
        "REPORTS TYPE:",
        type(reports)
    )

    print(
        "REPORTS TOTAL:",
        reports.total
    )


    # -------------------------------------------------
    # TEMPLATE
    # -------------------------------------------------

    return render_template(
        "admin_reports.html",

        reports=reports,

        statuses=statuses,

        categories=categories,

        portfolios=portfolios,

        search=search,

        selected_status=status,

        selected_category=category,

        selected_portfolio=portfolio,
    )


# =====================================================
# REPORT DETAILS
# =====================================================

@admin_bp.route(
    "/admin_reports/<int:report_id>",
    methods=["GET"]
)
@login_required
@role_required("admin")
def report_details(report_id):

    report = Report.query.get_or_404(
        report_id
    )
    users = (
        User.query.filter_by(is_active=True)
        .order_by(User.username)
        .all()
    )
    return render_template(
        "admin/report_details.html",
        report=report,
        users=users
    )
# =====================================================
# UPDATE REPORT STATUS
# =====================================================

@admin_bp.route(
    "/reports/<int:report_id>/status",
    methods=["POST"]
)
@login_required
@role_required("admin")
def update_report_status(report_id):

    report = Report.query.get_or_404(report_id)

    status = request.form.get("status", "").strip()

    allowed_statuses = [
        "Pending",
        "Assigned",
        "In Progress",
        "Resolved",
        "Closed",
    ]

    if status not in allowed_statuses:
        flash(
            "Invalid report status.",
            "danger"
        )

        return redirect(
            url_for(
                "admin.report_details",
                report_id=report.id
            )
        )

    report.status = status

    db.session.commit()

    flash(
        "Report status updated successfully.",
        "success"
    )

    return redirect(
        url_for(
            "admin.report_details",
            report_id=report.id
        )
    ) 
# =====================================================
# ASSIGN REPORT
# =====================================================

@admin_bp.route(
    "/reports/<int:report_id>/assign",
    methods=["POST"]
)
@login_required
@role_required("admin")
def assign_report(report_id):

    report = Report.query.get_or_404(report_id)

    user_id = request.form.get(
        "assigned_to",
        type=int
    )

    if not user_id:
        flash(
            "Please select a user.",
            "warning"
        )

        return redirect(
            url_for(
                "admin.report_details",
                report_id=report.id
            )
        )

    user = User.query.get(user_id)

    if not user:
        flash(
            "Selected user does not exist.",
            "danger"
        )

        return redirect(
            url_for(
                "admin.report_details",
                report_id=report.id
            )
        )

    report.assigned_to = user.id

    if report.status == "Pending":
        report.status = "Assigned"

    db.session.commit()

    flash(
        "Report assigned successfully.",
        "success"
    )

    return redirect(
        url_for(
            "admin.report_details",
            report_id=report.id
        )
    )       