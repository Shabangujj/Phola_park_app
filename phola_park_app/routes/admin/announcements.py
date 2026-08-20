"""
====================================================
JJCORETECH
Phola Park App

Admin Announcement Management
====================================================
"""

from datetime import datetime

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
    Announcement
)
from phola_park_app.extensions import db
@admin_bp.route("/announcements")
@login_required
@role_required("admin")
def announcements():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    )

    query = Announcement.query

    if search:

        query = query.filter(
            Announcement.title.ilike(
                f"%{search}%"
            )
        )

    announcements = query.order_by(
        Announcement.created_at.desc()
    ).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    return render_template(

        "admin/announcements.html",

        announcements=announcements,

        search=search

    )
@admin_bp.route(
    "/announcements/<int:announcement_id>"
)
@login_required
@role_required("admin")
def view_announcement(
    announcement_id
):

    announcement = Announcement.query.get_or_404(
        announcement_id
    )

    return render_template(

        "admin/view_announcement.html",

        announcement=announcement

    )
@admin_bp.route(
    "/announcements/create",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def create_announcement():

    # =================================================
    # CREATE ANNOUNCEMENT
    # =================================================

    if request.method == "POST":

        # ---------------------------------------------
        # Get form data
        # ---------------------------------------------

        title = request.form.get(
            "title",
            ""
        ).strip()

        message = request.form.get(
            "message",
            ""
        ).strip()

        target_role = request.form.get(
            "target_role",
            ""
        ).strip()

        portfolio = request.form.get(
            "portfolio",
            ""
        ).strip()

        priority = request.form.get(
            "priority",
            "Normal"
        ).strip()

        # ---------------------------------------------
        # Validate required fields
        # ---------------------------------------------

        if not title or not message:

            flash(
                "Title and message are required.",
                "danger"
            )

            return redirect(
                url_for("admin.create_announcement")
            )

        # ---------------------------------------------
        # Create announcement
        # ---------------------------------------------

        announcement = Announcement(

            title=title,

            message=message,

            target_role=target_role
                if target_role
                else None,

            portfolio=portfolio
                if portfolio
                else None,

            priority=priority,

            is_active=True,

            publish_date=datetime.utcnow()

        )

        # ---------------------------------------------
        # Save
        # ---------------------------------------------

        try:

            db.session.add(
                announcement
            )

            db.session.commit()

        except Exception as e:

            db.session.rollback()

            print(
                "ANNOUNCEMENT ERROR:",
                e
            )

            flash(
                "Unable to create announcement.",
                "danger"
            )

            return redirect(
                url_for("admin.create_announcement")
            )

        # ---------------------------------------------
        # Success
        # ---------------------------------------------

        flash(
            "Announcement created successfully.",
            "success"
        )

        return redirect(
            url_for("admin.announcements")
        )

    # =================================================
    # GET
    # =================================================

    return render_template(
        "admin/create_announcement.html"
    )
@admin_bp.route(
    "/announcements/<int:announcement_id>/edit",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def edit_announcement(
    announcement_id
):

    announcement = Announcement.query.get_or_404(
        announcement_id
    )

    if request.method == "POST":

        announcement.title = request.form.get(
            "title"
        )

        announcement.message = request.form.get(
            "message"
        )

        announcement.portfolio = request.form.get(
            "portfolio"
        )

        announcement.target = request.form.get(
            "target"
        )

        db.session.commit()

        flash(
            "Announcement updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "admin.view_announcement",
                announcement_id=announcement.id
            )
        )

    return render_template(

        "admin/edit_announcement.html",

        announcement=announcement

    )
@admin_bp.route(
    "/announcements/<int:announcement_id>/delete",
    methods=["POST"]
)
@login_required
@role_required("admin")
def delete_announcement(
    announcement_id
):

    announcement = Announcement.query.get_or_404(
        announcement_id
    )

    db.session.delete(
        announcement
    )

    db.session.commit()

    flash(
        "Announcement deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "admin.announcements"
        )
    )
@admin_bp.route(
    "/announcements/<int:announcement_id>/publish",
    methods=["POST"]
)
@login_required
@role_required("admin")
def publish_announcement(
    announcement_id
):

    announcement = Announcement.query.get_or_404(
        announcement_id
    )

    announcement.status = "Published"

    db.session.commit()

    flash(
        "Announcement published.",
        "success"
    )

    return redirect(
        url_for(
            "admin.view_announcement",
            announcement_id=announcement.id
        )
    )
@admin_bp.route(
    "/announcements/<int:announcement_id>/unpublish",
    methods=["POST"]
)
@login_required
@role_required("admin")
def unpublish_announcement(
    announcement_id
):

    announcement = Announcement.query.get_or_404(
        announcement_id
    )

    announcement.status = "Draft"

    db.session.commit()

    flash(
        "Announcement moved to Draft.",
        "warning"
    )

    return redirect(
        url_for(
            "admin.view_announcement",
            announcement_id=announcement.id
        )
    )
@admin_bp.route("/announcements/dashboard")
@login_required
@role_required("admin")
def announcement_dashboard():

    total = Announcement.query.count()

    published = Announcement.query.filter_by(
        status="Published"
    ).count()

    drafts = Announcement.query.filter_by(
        status="Draft"
    ).count()

    archived = Announcement.query.filter_by(
        status="Archived"
    ).count()

    return render_template(

        "admin/announcement_dashboard.html",

        total=total,

        published=published,

        drafts=drafts,

        archived=archived

    )