from flask import (
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from phola_park_app import db
from phola_park_app.reports import reports_bp
from phola_park_app.reports.forms import ReportForm
from phola_park_app.model import Report


@reports_bp.route("/reports")
@login_required
def reports():

    my_reports = Report.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "reports/my_reports.html",
        reports=my_reports
    )


@reports_bp.route(
    "/reports/create",
    methods=["GET", "POST"]
)
@login_required
def create_report():

    form = ReportForm()

    if form.validate_on_submit():

        report = Report(
            title=form.title.data,
            category=form.category.data,
            description=form.description.data,
            user_id=current_user.id
        )

        db.session.add(report)
        db.session.commit()

        flash(
            "Report submitted successfully.",
            "success"
        )

        return redirect(
            url_for("reports.reports")
        )

    return render_template(
        "reports/create_report.html",
        form=form
    )