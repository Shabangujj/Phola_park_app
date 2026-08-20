"""
====================================================
JJCORETECH
Phola Park App

Admin Project Management
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
    Project,
    User
)
from phola_park_app.extensions import db
@admin_bp.route("/projects")
@login_required
@role_required("admin")
def projects():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    )

    query = Project.query

    if search:

        query = query.filter(
            Project.name.ilike(
                f"%{search}%"
            )
        )

    projects = query.order_by(
        Project.created_at.desc()
    ).paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    return render_template(

        "admin/projects.html",

        projects=projects,

        search=search

    )
@admin_bp.route("/projects/<int:project_id>")
@login_required
@role_required("admin")
def view_project(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    return render_template(

        "admin/view_project.html",

        project=project

    )
@admin_bp.route(
    "/projects/create",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def create_project():

    if request.method == "POST":

        project = Project(

            name=request.form.get("name"),

            description=request.form.get(
                "description"
            ),

            portfolio=request.form.get(
                "portfolio"
            ),

            status="Planning",

            start_date=request.form.get(
                "start_date"
            ),

            end_date=request.form.get(
                "end_date"
            )

        )

        db.session.add(project)

        db.session.commit()

        flash(
            "Project created successfully.",
            "success"
        )

        return redirect(
            url_for(
                "admin.projects"
            )
        )

    return render_template(
        "admin/create_project.html"
    )
@admin_bp.route(
    "/projects/<int:project_id>/edit",
    methods=["GET","POST"]
)
@login_required
@role_required("admin")
def edit_project(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    if request.method == "POST":

        project.name = request.form.get(
            "name"
        )

        project.description = request.form.get(
            "description"
        )

        project.portfolio = request.form.get(
            "portfolio"
        )

        project.status = request.form.get(
            "status"
        )

        project.start_date = request.form.get(
            "start_date"
        )

        project.end_date = request.form.get(
            "end_date"
        )

        db.session.commit()

        flash(
            "Project updated.",
            "success"
        )

        return redirect(
            url_for(
                "admin.view_project",
                project_id=project.id
            )
        )

    return render_template(

        "admin/edit_project.html",

        project=project

    )
@admin_bp.route(
    "/projects/<int:project_id>/delete",
    methods=["POST"]
)
@login_required
@role_required("admin")
def delete_project(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    db.session.delete(project)

    db.session.commit()

    flash(
        "Project deleted.",
        "success"
    )

    return redirect(
        url_for(
            "admin.projects"
        )
    )
@admin_bp.route(
    "/projects/<int:project_id>/status",
    methods=["POST"]
)
@login_required
@role_required("admin")
def update_project_status(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    project.status = request.form.get(
        "status"
    )

    db.session.commit()

    flash(
        "Project status updated.",
        "success"
    )

    return redirect(
        url_for(
            "admin.view_project",
            project_id=project.id
        )
    )
@admin_bp.route(
    "/projects/<int:project_id>/assign",
    methods=["GET","POST"]
)
@login_required
@role_required("admin")
def assign_project(project_id):

    project = Project.query.get_or_404(
        project_id
    )

    users = User.query.order_by(
        User.username
    ).all()

    if request.method == "POST":

        project.assigned_to = request.form.get(
            "assigned_to"
        )

        db.session.commit()

        flash(
            "Project assigned successfully.",
            "success"
        )

        return redirect(
            url_for(
                "admin.view_project",
                project_id=project.id
            )
        )

    return render_template(

        "admin/assign_project.html",

        project=project,

        users=users

    )
@admin_bp.route("/projects/dashboard")
@login_required
@role_required("admin")
def project_dashboard():

    total = Project.query.count()

    planning = Project.query.filter_by(
        status="Planning"
    ).count()

    progress = Project.query.filter_by(
        status="In Progress"
    ).count()

    completed = Project.query.filter_by(
        status="Completed"
    ).count()

    cancelled = Project.query.filter_by(
        status="Cancelled"
    ).count()

    return render_template(

        "admin/project_dashboard.html",

        total=total,

        planning=planning,

        progress=progress,

        completed=completed,

        cancelled=cancelled

    )