"""
====================================================
JJCORETECH
Phola Park App
Admin Settings
====================================================
"""

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required

from . import admin_bp

from phola_park_app.decorators import role_required

from phola_park_app.models import (
    SystemSettings
)
from phola_park_app.extensions import db
@admin_bp.route("/settings")
@login_required
@role_required("admin")
def settings():

    settings = SystemSettings.query.first()

    if settings is None:

        settings = SystemSettings()

        db.session.add(settings)

        db.session.commit()

    return render_template(

        "admin/settings.html",

        settings=settings

    )
@admin_bp.route(
    "/settings/update",
    methods=["POST"]
)
@login_required
@role_required("admin")
def update_settings():

    settings = SystemSettings.query.first()

    if settings is None:

        settings = SystemSettings()

        db.session.add(settings)

    settings.site_name = request.form.get(
        "site_name"
    )

    settings.company_name = request.form.get(
        "company_name"
    )

    settings.contact_email = request.form.get(
        "contact_email"
    )

    settings.contact_phone = request.form.get(
        "contact_phone"
    )

    settings.address = request.form.get(
        "address"
    )

    settings.theme = request.form.get(
        "theme"
    )

    settings.allow_registration = (
        request.form.get("allow_registration")
        == "on"
    )

    settings.maintenance_mode = (
        request.form.get("maintenance_mode")
        == "on"
    )

    db.session.commit()

    flash(
        "Settings updated successfully.",
        "success"
    )

    return redirect(
        url_for("admin.settings")
    )
@admin_bp.route(
    "/settings/maintenance/on",
    methods=["POST"]
)
@login_required
@role_required("admin")
def enable_maintenance():

    settings = SystemSettings.query.first()

    settings.maintenance_mode = True

    db.session.commit()

    flash(
        "Maintenance Mode Enabled.",
        "warning"
    )

    return redirect(
        url_for("admin.settings")
    )
@admin_bp.route(
    "/settings/maintenance/off",
    methods=["POST"]
)
@login_required
@role_required("admin")
def disable_maintenance():

    settings = SystemSettings.query.first()

    settings.maintenance_mode = False

    db.session.commit()

    flash(
        "Maintenance Mode Disabled.",
        "success"
    )

    return redirect(
        url_for("admin.settings")
    )
    
@admin_bp.route(
    "/settings/reset",
    methods=["POST"]
)
@login_required
@role_required("admin")
def reset_settings():

    settings = SystemSettings.query.first()

    settings.site_name = "Phola Park App"

    settings.company_name = "JJCORETECH"

    settings.contact_email = ""

    settings.contact_phone = ""

    settings.address = ""

    settings.theme = "default"

    settings.allow_registration = True

    settings.maintenance_mode = False

    db.session.commit()

    flash(
        "System settings reset successfully.",
        "success"
    )

    return redirect(
        url_for("admin.settings")
    )