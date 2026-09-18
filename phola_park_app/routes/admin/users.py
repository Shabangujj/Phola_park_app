"""
JJCORETECH
Phola Park App

Admin User Management Routes
"""

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from . import admin_bp

from phola_park_app.decorators import role_required

from phola_park_app.models import (
    User,
    UserRole
)

from phola_park_app.extensions import db


# ============================================================
# AVAILABLE PORTFOLIOS
# ============================================================

PORTFOLIOS = [
    "Water",
    "Electricity",
    "Roads",
    "Crime",
    "Community Development",
    "Health",
    "Education",
    "Housing",
    "Environment",
]


# ============================================================
# USER MANAGEMENT
# ============================================================

@admin_bp.route("/users")
@login_required
@role_required("admin")
def users():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    query = User.query

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if search:

        search_term = f"%{search}%"

        query = query.filter(
            db.or_(
                User.username.ilike(search_term),
                User.full_name.ilike(search_term),
                User.email.ilike(search_term)
            )
        )

    # --------------------------------------------------------
    # PAGINATION
    # --------------------------------------------------------

    users = (
        query
        .order_by(User.id.asc())
        .paginate(
            page=page,
            per_page=10,
            error_out=False
        )
    )

    return render_template(
        "admin/users.html",
        users=users,
        search=search
    )


# ============================================================
# ADD USER
# ============================================================

@admin_bp.route(
    "/users/add",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def add_user():

    if request.method == "POST":

        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        role_id = request.form.get(
            "role_id",
            type=int
        )

        portfolio = request.form.get(
            "portfolio",
            ""
        ).strip()

        is_active = (
            request.form.get("is_active") == "1"
        )

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not full_name:

            flash(
                "Full name is required.",
                "warning"
            )

            return redirect(
                url_for("admin.add_user")
            )

        if not username:

            flash(
                "Username is required.",
                "warning"
            )

            return redirect(
                url_for("admin.add_user")
            )

        if not email:

            flash(
                "Email is required.",
                "warning"
            )

            return redirect(
                url_for("admin.add_user")
            )

        if not password:

            flash(
                "Password is required.",
                "warning"
            )

            return redirect(
                url_for("admin.add_user")
            )

        # ----------------------------------------------------
        # DUPLICATE USERNAME
        # ----------------------------------------------------

        existing_username = User.query.filter_by(
            username=username
        ).first()

        if existing_username:

            flash(
                "Username already exists.",
                "warning"
            )

            return redirect(
                url_for("admin.add_user")
            )

        # ----------------------------------------------------
        # DUPLICATE EMAIL
        # ----------------------------------------------------

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email:

            flash(
                "Email already exists.",
                "warning"
            )

            return redirect(
                url_for("admin.add_user")
            )

        # ----------------------------------------------------
        # ROLE
        # ----------------------------------------------------

        role = UserRole.query.get(role_id)

        if role is None:

            flash(
                "Invalid role selected.",
                "danger"
            )

            return redirect(
                url_for("admin.add_user")
            )

        # ----------------------------------------------------
        # NORMALIZE PORTFOLIO
        # ----------------------------------------------------

        portfolio = (
            portfolio
            if portfolio
            else None
        )

        # ----------------------------------------------------
        # SUPERVISOR MUST HAVE PORTFOLIO
        # ----------------------------------------------------

        if (
            role.name.lower() == "supervisor"
            and not portfolio
        ):

            flash(
                "A supervisor must have a portfolio assigned.",
                "warning"
            )

            return redirect(
                url_for("admin.add_user")
            )

        # ----------------------------------------------------
        # VALIDATE PORTFOLIO
        # ----------------------------------------------------

        if portfolio and portfolio not in PORTFOLIOS:

            flash(
                "Invalid portfolio selected.",
                "danger"
            )

            return redirect(
                url_for("admin.add_user")
            )

        # ----------------------------------------------------
        # CREATE USER
        # ----------------------------------------------------

        user = User(
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            role=role,
            portfolio=portfolio,
            is_active=is_active
        )

        user.set_password(password)

        db.session.add(user)

        db.session.commit()

        flash(
            "User created successfully.",
            "success"
        )

        return redirect(
            url_for("admin.users")
        )

    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    roles = (
        UserRole.query
        .order_by(UserRole.name.asc())
        .all()
    )

    return render_template(
        "admin/add_user.html",
        roles=roles,
        portfolios=PORTFOLIOS
    )


# ============================================================
# EDIT USER
# ============================================================

@admin_bp.route(
    "/users/edit/<int:user_id>",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def edit_user(user_id):

    user = User.query.get_or_404(
        user_id
    )

    roles = (
        UserRole.query
        .order_by(UserRole.name.asc())
        .all()
    )

    if request.method == "POST":

        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        portfolio = request.form.get(
            "portfolio",
            ""
        ).strip()

        role_id = request.form.get(
            "role_id",
            type=int
        )

        is_active = (
            request.form.get("is_active") == "1"
        )

        # ----------------------------------------------------
        # BASIC VALIDATION
        # ----------------------------------------------------

        if not full_name:

            flash(
                "Full name is required.",
                "warning"
            )

            return redirect(
                url_for(
                    "admin.edit_user",
                    user_id=user.id
                )
            )

        if not username:

            flash(
                "Username is required.",
                "warning"
            )

            return redirect(
                url_for(
                    "admin.edit_user",
                    user_id=user.id
                )
            )

        if not email:

            flash(
                "Email is required.",
                "warning"
            )

            return redirect(
                url_for(
                    "admin.edit_user",
                    user_id=user.id
                )
            )

        # ----------------------------------------------------
        # DUPLICATE USERNAME
        # ----------------------------------------------------

        existing_username = (
            User.query
            .filter(
                User.username == username,
                User.id != user.id
            )
            .first()
        )

        if existing_username:

            flash(
                "Username already exists.",
                "warning"
            )

            return redirect(
                url_for(
                    "admin.edit_user",
                    user_id=user.id
                )
            )

        # ----------------------------------------------------
        # DUPLICATE EMAIL
        # ----------------------------------------------------

        existing_email = (
            User.query
            .filter(
                User.email == email,
                User.id != user.id
            )
            .first()
        )

        if existing_email:

            flash(
                "Email already exists.",
                "warning"
            )

            return redirect(
                url_for(
                    "admin.edit_user",
                    user_id=user.id
                )
            )

        # ----------------------------------------------------
        # ROLE
        # ----------------------------------------------------

        role = UserRole.query.get(
            role_id
        )

        if role is None:

            flash(
                "Invalid role selected.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.edit_user",
                    user_id=user.id
                )
            )

        # ----------------------------------------------------
        # NORMALIZE PORTFOLIO
        # ----------------------------------------------------

        portfolio = (
            portfolio
            if portfolio
            else None
        )

        # ----------------------------------------------------
        # VALIDATE PORTFOLIO
        # ----------------------------------------------------

        if portfolio and portfolio not in PORTFOLIOS:

            flash(
                "Invalid portfolio selected.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.edit_user",
                    user_id=user.id
                )
            )

        # ----------------------------------------------------
        # SUPERVISOR PORTFOLIO REQUIREMENT
        # ----------------------------------------------------

        if (
            role.name.lower() == "supervisor"
            and not portfolio
        ):

            flash(
                "A supervisor must have a portfolio assigned.",
                "warning"
            )

            return redirect(
                url_for(
                    "admin.edit_user",
                    user_id=user.id
                )
            )

        # ----------------------------------------------------
        # PROTECT CURRENT ADMIN
        # ----------------------------------------------------

        if user.id == current_user.id:

            if not is_active:

                flash(
                    "You cannot disable your own administrator account.",
                    "danger"
                )

                return redirect(
                    url_for(
                        "admin.edit_user",
                        user_id=user.id
                    )
                )

            if role.name.lower() != "admin":

                flash(
                    "You cannot remove your own administrator role.",
                    "danger"
                )

                return redirect(
                    url_for(
                        "admin.edit_user",
                        user_id=user.id
                    )
                )

        # ----------------------------------------------------
        # UPDATE USER
        # ----------------------------------------------------

        user.full_name = full_name
        user.username = username
        user.email = email
        user.phone = phone

        # Empty portfolio becomes None
        user.portfolio = portfolio

        user.role = role
        user.is_active = is_active

        db.session.commit()

        flash(
            "User updated successfully.",
            "success"
        )

        return redirect(
            url_for("admin.users")
        )

    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    return render_template(
        "admin/edit_user.html",
        user=user,
        roles=roles,
        portfolios=PORTFOLIOS
    )


# ============================================================
# DELETE USER
# ============================================================

@admin_bp.route(
    "/users/<int:user_id>/delete",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def delete_user(user_id):

    user = User.query.get_or_404(
        user_id
    )

    # --------------------------------------------------------
    # PREVENT SELF DELETE
    # --------------------------------------------------------

    if user.id == current_user.id:

        flash(
            "You cannot delete your own account.",
            "danger"
        )

        return redirect(
            url_for("admin.users")
        )

    # --------------------------------------------------------
    # PREVENT LAST ADMIN DELETE
    # --------------------------------------------------------

    if user.role and user.role.name.lower() == "admin":

        admin_count = (
            db.session.query(UserRole)
            .filter(
                db.func.lower(UserRole.name) == "admin"
            )
            .count()
        )

        if admin_count <= 1:

            flash(
                "Cannot delete the last administrator.",
                "warning"
            )

            return redirect(
                url_for("admin.users")
            )

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    if request.method == "POST":

        db.session.delete(user)

        db.session.commit()

        flash(
            "User deleted successfully.",
            "success"
        )

        return redirect(
            url_for("admin.users")
        )

    # --------------------------------------------------------
    # CONFIRMATION PAGE
    # --------------------------------------------------------

    return render_template(
        "admin/delete_user.html",
        user=user
    )


# ============================================================
# ASSIGN PORTFOLIO
# ============================================================

@admin_bp.route(
    "/users/<int:user_id>/portfolio",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def assign_portfolio(user_id):

    user = User.query.get_or_404(
        user_id
    )

    # --------------------------------------------------------
    # ONLY SUPERVISORS
    # --------------------------------------------------------

    if not user.is_supervisor:

        flash(
            "Portfolio assignment is only available for supervisors.",
            "warning"
        )

        return redirect(
            url_for(
                "admin.user_details",
                user_id=user.id
            )
        )

    if request.method == "POST":

        portfolio = request.form.get(
            "portfolio",
            ""
        ).strip()

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not portfolio:

            flash(
                "Please select a portfolio.",
                "warning"
            )

            return redirect(
                url_for(
                    "admin.assign_portfolio",
                    user_id=user.id
                )
            )

        if portfolio not in PORTFOLIOS:

            flash(
                "Invalid portfolio selected.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.assign_portfolio",
                    user_id=user.id
                )
            )

        # ----------------------------------------------------
        # ASSIGN
        # ----------------------------------------------------

        user.assign_portfolio(
            portfolio
        )

        db.session.commit()

        flash(
            f"Portfolio '{portfolio}' assigned to "
            f"{user.username}.",
            "success"
        )

        return redirect(
            url_for(
                "admin.user_details",
                user_id=user.id
            )
        )

    return render_template(
        "admin/assign_portfolio.html",
        user=user,
        portfolios=PORTFOLIOS
    )


# ============================================================
# ASSIGN ROLE
# ============================================================

@admin_bp.route(
    "/users/<int:user_id>/role",
    methods=["POST"]
)
@login_required
@role_required("admin")
def assign_role(user_id):

    user = User.query.get_or_404(
        user_id
    )

    role_name = request.form.get(
        "role",
        ""
    ).strip()

    if not role_name:

        flash(
            "Please select a role.",
            "warning"
        )

        return redirect(
            url_for("admin.users")
        )

    role = (
        db.session.query(UserRole)
        .filter(
            db.func.lower(UserRole.name)
            == role_name.lower()
        )
        .first()
    )

    if role is None:

        flash(
            "Invalid role selected.",
            "danger"
        )

        return redirect(
            url_for("admin.users")
        )

    # --------------------------------------------------------
    # PROTECT CURRENT ADMIN
    # --------------------------------------------------------

    if user.id == current_user.id:

        if role.name.lower() != "admin":

            flash(
                "You cannot remove your own administrator role.",
                "danger"
            )

            return redirect(
                url_for("admin.users")
            )

    # --------------------------------------------------------
    # SUPERVISOR REQUIRES PORTFOLIO
    # --------------------------------------------------------

    if (
        role.name.lower() == "supervisor"
        and not user.has_portfolio
    ):

        flash(
            "A supervisor must have a portfolio assigned.",
            "warning"
        )

        return redirect(
            url_for(
                "admin.user_details",
                user_id=user.id
            )
        )

    user.role = role

    db.session.commit()

    flash(
        "Role updated successfully.",
        "success"
    )

    return redirect(
        url_for("admin.users")
    )


# ============================================================
# USER DETAILS
# ============================================================

@admin_bp.route(
    "/users/<int:user_id>"
)
@login_required
@role_required("admin")
def user_details(user_id):

    user = User.query.get_or_404(
        user_id
    )

    return render_template(
        "admin/user_details.html",
        user=user
    )


# ============================================================
# TOGGLE USER
# ============================================================

@admin_bp.route(
    "/users/<int:user_id>/toggle",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def toggle_user(user_id):

    user = User.query.get_or_404(
        user_id
    )

    # --------------------------------------------------------
    # PREVENT SELF DISABLE
    # --------------------------------------------------------

    if user.id == current_user.id:

        flash(
            "You cannot disable your own account.",
            "warning"
        )

        return redirect(
            url_for("admin.users")
        )

    user.is_active = not user.is_active

    db.session.commit()

    if user.is_active:

        flash(
            f"{user.username} has been activated.",
            "success"
        )

    else:

        flash(
            f"{user.username} has been deactivated.",
            "warning"
        )

    return redirect(
        url_for("admin.users")
    )


# ============================================================
# RESET PASSWORD
# ============================================================

@admin_bp.route(
    "/users/<int:user_id>/reset-password",
    methods=["GET", "POST"]
)
@login_required
@role_required("admin")
def reset_password(user_id):

    user = User.query.get_or_404(
        user_id
    )

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

        confirm = request.form.get(
            "confirm_password",
            ""
        )

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not password:

            flash(
                "Password is required.",
                "warning"
            )

            return redirect(
                url_for(
                    "admin.reset_password",
                    user_id=user.id
                )
            )

        if password != confirm:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.reset_password",
                    user_id=user.id
                )
            )

        # ----------------------------------------------------
        # UPDATE PASSWORD
        # ----------------------------------------------------

        user.set_password(
            password
        )

        db.session.commit()

        flash(
            "Password reset successfully.",
            "success"
        )

        return redirect(
            url_for(
                "admin.user_details",
                user_id=user.id
            )
        )

    return render_template(
        "admin/reset_password.html",
        user=user
    )