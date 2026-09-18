from flask import (
    Blueprint,
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

from datetime import datetime, timedelta

from collections import Counter

from phola_park_app.extensions import db

from phola_park_app.models import (
    Survey,
    Report,
    User,
    UserRole,
    Notice,
    Notification,
    Committee
)
from phola_park_app.utils.permissions import role_required


supervisor_bp = Blueprint(
    'supervisor',
    __name__,
    url_prefix='/supervisor'
)
@supervisor_bp.route('/dashboard')
@login_required
@role_required('supervisor')
def dashboard():

    portfolio = current_user.portfolio

    # Supervisor must have a portfolio
    if not portfolio:
        flash(
            'No portfolio assigned for your supervisor account.',
            'warning'
        )
        return redirect(url_for('auth.login'))

    # ---------------------------------------------------------
    # REPORTS FOR THIS PORTFOLIO
    # ---------------------------------------------------------
    reports = (
        Report.query
        .filter_by(portfolio=portfolio)
        .all()
    )

    # ---------------------------------------------------------
    # ACTIVE NOTICES FOR THIS PORTFOLIO
    # ---------------------------------------------------------
    notices = (
        Notice.query
        .filter(
            Notice.is_active.is_(True),
            Notice.portfolio == portfolio
        )
        .order_by(Notice.created_at.desc())
        .all()
    )

    # ---------------------------------------------------------
    # REPORT STATUS COUNTS
    # ---------------------------------------------------------
    status_counts = {
        'Pending': 0,
        'In Progress': 0,
        'Completed': 0,
        'Rejected': 0
    }

    for report in reports:
        status = report.status or 'Pending'
        status_counts[status] = (
            status_counts.get(status, 0) + 1
        )

    # ---------------------------------------------------------
    # REPORT CATEGORY COUNTS
    # ---------------------------------------------------------
    category_counts = Counter(
        report.category
        for report in reports
        if report.category
    )

    # ---------------------------------------------------------
    # DASHBOARD STATISTICS
    # ---------------------------------------------------------
    stats = {
        'total': len(reports),

        'open': (
            status_counts.get('Pending', 0)
            + status_counts.get('In Progress', 0)
        ),

        'closed': (
            status_counts.get('Completed', 0)
            + status_counts.get('Rejected', 0)
        ),

        'notices': len(notices)
    }

    # ---------------------------------------------------------
    # RENDER DASHBOARD
    # ---------------------------------------------------------
    return render_template(
        'supervisor/supervisor_dashboard.html',

        portfolio=portfolio,

        stats=stats,

        notices=notices,

        status_labels=list(status_counts.keys()),
        status_values=list(status_counts.values()),

        category_labels=list(category_counts.keys()),
        category_values=list(category_counts.values())
    )
# ============================================================
# SUPERVISOR NOTICES
# ============================================================
@supervisor_bp.route('/notices')
@login_required
@role_required('supervisor')
def notices():

    portfolio = current_user.portfolio

    # Supervisor must have a portfolio
    if not portfolio:
        flash(
            'No portfolio assigned for your supervisor account.',
            'warning'
        )
        return redirect(url_for('auth.login'))

    # Show active notices belonging to this supervisor's portfolio
    notices = (
        Notice.query
        .filter(
            Notice.is_active.is_(True),
            Notice.portfolio == portfolio
        )
        .order_by(
            Notice.created_at.desc()
        )
        .all()
    )

    return render_template(
        'supervisor/notices.html',
        notices=notices,
        portfolio=portfolio
    )
@supervisor_bp.route('/notices/new', methods=['GET', 'POST'])
@login_required
@role_required('supervisor')
def new_notice():

    portfolio = current_user.portfolio

    # Supervisor must have a portfolio
    if not portfolio:
        flash(
            'No portfolio assigned for your supervisor account.',
            'warning'
        )
        return redirect(url_for('supervisor.dashboard'))

    if request.method == 'POST':

        title = request.form.get('title', '').strip()
        message = request.form.get('message', '').strip()

        # Use safe defaults
        notice_type = request.form.get('notice_type') or 'Notice'
        priority = request.form.get('priority') or 'Normal'

        # Validate title
        if not title:
            flash(
                'Notice title is required.',
                'danger'
            )

            return render_template(
                'supervisor/new_notice.html',
                portfolio=portfolio
            )

        # Validate message
        if not message:
            flash(
                'Notice message is required.',
                'danger'
            )

            return render_template(
                'supervisor/new_notice.html',
                portfolio=portfolio
            )

        # Create notice
        notice = Notice(
            title=title,
            message=message,

            # IMPORTANT:
            # Portfolio comes from the logged-in supervisor.
            portfolio=portfolio,

            notice_type=notice_type,
            priority=priority,

            # New notices are active
            is_active=True,

            # Record who created the notice
            created_by=current_user.id
        )

        db.session.add(notice)
        db.session.commit()

        flash(
            'Notice created successfully.',
            'success'
        )

        return redirect(
            url_for('supervisor.notices')
        )

    return render_template(
        'supervisor/new_notice.html',
        portfolio=portfolio
    )     
@supervisor_bp.route('/notices/<int:notice_id>')
@login_required
@role_required('supervisor')
def notice_detail(notice_id):

    notice = Notice.query.get_or_404(notice_id)

    # Supervisor can only view notices
    # belonging to their portfolio.
    if notice.portfolio != current_user.portfolio:
        flash('Permission denied.', 'danger')
        return redirect(url_for('supervisor.notices'))

    return render_template(
        'supervisor/notice_detail.html',
        notice=notice,
        portfolio=current_user.portfolio
    )
@supervisor_bp.route('/notices/<int:notice_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('supervisor')
def edit_notice(notice_id):

    notice = Notice.query.get_or_404(notice_id)

    # Supervisor can only edit notices
    # belonging to their portfolio.
    if notice.portfolio != current_user.portfolio:
        flash('Permission denied.', 'danger')
        return redirect(url_for('supervisor.notices'))

    if request.method == 'POST':

        title = request.form.get('title', '').strip()
        message = request.form.get('message', '').strip()
        notice_type = request.form.get('notice_type', 'Notice')
        priority = request.form.get('priority', 'Normal')

        # Validate required fields
        if not title:
            flash('Notice title is required.', 'danger')

            return render_template(
                'supervisor/edit_notice.html',
                notice=notice,
                portfolio=current_user.portfolio
            )

        if not message:
            flash('Notice message is required.', 'danger')

            return render_template(
                'supervisor/edit_notice.html',
                notice=notice,
                portfolio=current_user.portfolio
            )

        # Update notice
        notice.title = title
        notice.message = message
        notice.notice_type = notice_type
        notice.priority = priority

        db.session.commit()

        flash(
            'Notice updated successfully.',
            'success'
        )

        return redirect(
            url_for(
                'supervisor.notice_detail',
                notice_id=notice.id
            )
        )

    return render_template(
        'supervisor/edit_notice.html',
        notice=notice,
        portfolio=current_user.portfolio
    )
@supervisor_bp.route('/notices/<int:notice_id>/archive', methods=['POST'])
@login_required
@role_required('supervisor')
def archive_notice(notice_id):

    notice = Notice.query.get_or_404(notice_id)

    if notice.portfolio != current_user.portfolio:
        flash('Permission denied.', 'danger')
        return redirect(url_for('supervisor.notices'))

    notice.archive()
    db.session.commit()

    flash('Notice archived successfully.', 'success')

    return redirect(
        url_for(
            'supervisor.notice_detail',
            notice_id=notice.id
        )
    )


@supervisor_bp.route('/notices/<int:notice_id>/publish', methods=['POST'])
@login_required
@role_required('supervisor')
def publish_notice(notice_id):

    notice = Notice.query.get_or_404(notice_id)

    if notice.portfolio != current_user.portfolio:
        flash('Permission denied.', 'danger')
        return redirect(url_for('supervisor.notices'))

    notice.publish()
    db.session.commit()

    flash('Notice published successfully.', 'success')

    return redirect(
        url_for(
            'supervisor.notice_detail',
            notice_id=notice.id
        )
    )
@supervisor_bp.route('/reports')
@login_required
@role_required('supervisor')
def reports():

    portfolio = current_user.portfolio

    # Supervisor must have a portfolio
    if not portfolio:
        flash(
            'No portfolio assigned for your supervisor account.',
            'warning'
        )
        return redirect(url_for('auth.login'))

    # ---------------------------------------------------------
    # FILTERS
    # ---------------------------------------------------------

    status = request.args.get('status', 'all')
    keyword = request.args.get('keyword', '').strip()
    start = request.args.get('start_date')
    end = request.args.get('end_date')

    # ---------------------------------------------------------
    # BASE QUERY
    # ---------------------------------------------------------

    query = Report.query.filter_by(
        portfolio=portfolio
    )

    # ---------------------------------------------------------
    # STATUS FILTER
    # ---------------------------------------------------------

    if status != 'all':
        query = query.filter_by(
            status=status
        )

    # ---------------------------------------------------------
    # KEYWORD SEARCH
    # ---------------------------------------------------------

    if keyword:
        search_term = f'%{keyword}%'

        query = query.filter(
            db.or_(
                Report.description.ilike(search_term),
                Report.category.ilike(search_term)
            )
        )

    # ---------------------------------------------------------
    # START DATE
    # ---------------------------------------------------------

    if start:

        try:

            start_date = datetime.strptime(
                start,
                '%Y-%m-%d'
            )

            query = query.filter(
                Report.created_at >= start_date
            )

        except ValueError:

            flash(
                'Invalid start date.',
                'warning'
            )

    # ---------------------------------------------------------
    # END DATE
    # ---------------------------------------------------------

    if end:

        try:

            # Include the entire selected end date.
            end_date = datetime.strptime(
                end,
                '%Y-%m-%d'
            )

            query = query.filter(
                Report.created_at < end_date + timedelta(days=1)
            )

        except ValueError:

            flash(
                'Invalid end date.',
                'warning'
            )

    # ---------------------------------------------------------
    # GET REPORTS
    # ---------------------------------------------------------

    reports = (
        query
        .order_by(Report.created_at.desc())
        .all()
    )

    # ---------------------------------------------------------
    # RENDER
    # ---------------------------------------------------------

    return render_template(
        'supervisor/reports.html',

        reports=reports,

        status=status,

        keyword=keyword,

        start=start,

        end=end,

        portfolio=portfolio,
    )


# =============================================================
# REPORT DETAIL
# =============================================================

@supervisor_bp.route('/reports/<int:report_id>')
@login_required
@role_required('supervisor')
def report_detail(report_id):

    report = Report.query.get_or_404(
        report_id
    )

    # Security:
    # Supervisor can only view reports
    # belonging to their portfolio.
    if report.portfolio != current_user.portfolio:

        flash(
            'Unauthorized access to this report.',
            'danger'
        )

        return redirect(
            url_for('supervisor.reports')
        )

    return render_template(
        'supervisor/report_details.html',
        report=report
    )


# =============================================================
# UPDATE REPORT STATUS
# =============================================================

@supervisor_bp.route(
    '/reports/<int:report_id>/status',
    methods=['POST']
)
@login_required
@role_required('supervisor')
def update_report_status(report_id):

    report = Report.query.get_or_404(
        report_id
    )

    # Security:
    # Supervisor cannot modify reports
    # belonging to another portfolio.
    if report.portfolio != current_user.portfolio:

        flash(
            'Permission denied.',
            'danger'
        )

        return redirect(
            url_for('supervisor.reports')
        )

    # ---------------------------------------------------------
    # VALID STATUSES
    # ---------------------------------------------------------

    allowed_statuses = {
        'Pending',
        'In Progress',
        'Completed',
        'Rejected'
    }

    new_status = request.form.get(
        'status',
        ''
    ).strip()

    # Normalize incoming status
    status_map = {
        'pending': 'Pending',
        'in progress': 'In Progress',
        'completed': 'Completed',
        'rejected': 'Rejected'
    }

    normalized_status = status_map.get(
        new_status.lower()
    )

    if normalized_status not in allowed_statuses:

        flash(
            'Invalid status.',
            'danger'
        )

        return redirect(
            url_for(
                'supervisor.report_detail',
                report_id=report.id
            )
        )

    # ---------------------------------------------------------
    # UPDATE STATUS
    # ---------------------------------------------------------

    report.status = normalized_status

    # ---------------------------------------------------------
    # OPTIONAL COMMENT
    # ---------------------------------------------------------

    comment = request.form.get(
        'comment',
        ''
    ).strip()

    if comment:
        report.comment = comment

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    db.session.commit()

    flash(
        'Report status updated successfully.',
        'success'
    )

    return redirect(
        url_for(
            'supervisor.report_detail',
            report_id=report.id
        )
    )

@supervisor_bp.route('/reports/<int:report_id>/comment', methods=['POST'])
@login_required
@role_required('supervisor')
def add_comment(report_id):
    report = Report.query.get_or_404(report_id)

    if report.portfolio != current_user.portfolio:
        flash('Permission denied.', 'danger')
        return redirect(url_for('supervisor.reports'))

    comment = request.form.get('comment', '').strip()
    if comment:
        report.comment = comment
        db.session.commit()
        flash('Comment added.', 'success')

    return redirect(url_for('supervisor.report_detail', report_id=report.id))


@supervisor_bp.route('/surveys')
@login_required
@role_required('supervisor')
def surveys():
    portfolio = current_user.portfolio
    surveys = Survey.query.filter_by(portfolio=portfolio).order_by(Survey.created_at.desc()).all()
    return render_template('supervisor/surveys.html', surveys=surveys, portfolio=portfolio)


@supervisor_bp.route('/surveys/upload', methods=['GET', 'POST'])
@login_required
@role_required('supervisor')
def create_survey():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        survey_type = request.form.get('survey_type')
        link = request.form.get('link')

        survey = Survey(
            title=title,
            description=description,
            survey_type=survey_type,
            link=link,
            portfolio=current_user.portfolio
        )
        db.session.add(survey)
        db.session.commit()

        flash('Survey uploaded successfully.', 'success')
        return redirect(url_for('supervisor.surveys'))

    return render_template('supervisor/create_survey.html')

@supervisor_bp.route(
    '/surveys/<int:survey_id>/edit',
    methods=['GET', 'POST']
)
@login_required
@role_required('supervisor')
def edit_survey(survey_id):

    survey = Survey.query.get_or_404(survey_id)

    # Supervisor can only edit surveys in their portfolio
    if survey.portfolio != current_user.portfolio:
        flash(
            'Permission denied.',
            'danger'
        )
        return redirect(
            url_for('supervisor.surveys')
        )

    if request.method == 'POST':

        survey.title = request.form.get(
            'title',
            ''
        ).strip()

        survey.description = request.form.get(
            'description',
            ''
        ).strip()

        survey.survey_type = request.form.get(
            'survey_type',
            ''
        ).strip()

        survey.link = request.form.get(
            'link',
            ''
        ).strip()

        db.session.commit()

        flash(
            'Survey updated successfully.',
            'success'
        )

        return redirect(
            url_for('supervisor.surveys')
        )

    return render_template(
        'supervisor/edit_survey.html',
        survey=survey
    )


@supervisor_bp.route('/surveys/<int:survey_id>/delete', methods=['POST'])
@login_required
@role_required('supervisor')
def delete_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    if survey.portfolio != current_user.portfolio:
        flash('Permission denied.', 'danger')
        return redirect(url_for('supervisor.surveys'))

    db.session.delete(survey)
    db.session.commit()
    flash('Survey deleted successfully.', 'success')
    return redirect(url_for('supervisor.surveys'))

@supervisor_bp.route('/committees')
@login_required
@role_required('supervisor')
def committees():

    portfolio = current_user.portfolio

    committees = (
        Committee.query
        .filter_by(portfolio=portfolio)
        .order_by(Committee.created_at.desc())
        .all()
    )

    return render_template(
        'supervisor/committees.html',
        committees=committees,
        portfolio=portfolio
    )


@supervisor_bp.route('/committees/new', methods=['GET', 'POST'])
@login_required
@role_required('supervisor')
def new_committee():

    if request.method == 'POST':

        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        # Validate committee name
        if not name:
            flash('Committee name is required.', 'danger')
            return render_template(
                'supervisor/new_committee.html',
                portfolio=current_user.portfolio
            )

        committee = Committee(
            name=name,
            description=description,
            portfolio=current_user.portfolio,
            created_by=current_user.id
        )

        db.session.add(committee)
        db.session.commit()

        flash(
            'Committee created successfully.',
            'success'
        )

        return redirect(
            url_for('supervisor.committees')
        )

    return render_template(
        'supervisor/new_committee.html',
        portfolio=current_user.portfolio
    )
@supervisor_bp.route('/committees/<int:committee_id>')
@login_required
@role_required('supervisor')
def committee_detail(committee_id):

    committee = Committee.query.get_or_404(committee_id)

    # Supervisor can only manage committees
    # belonging to their portfolio.
    if committee.portfolio != current_user.portfolio:
        flash('Permission denied.', 'danger')
        return redirect(
            url_for('supervisor.committees')
        )

    # IDs of users already in this committee
    existing_member_ids = [
        member.id
        for member in committee.members.all()
    ]

    # Only normal community users from this portfolio
    available_users = (
        User.query
        .join(UserRole)
        .filter(
            User.portfolio == current_user.portfolio,
            UserRole.name.ilike('user')
        )
        .filter(
            ~User.id.in_(existing_member_ids)
        )
        .order_by(User.full_name.asc())
        .all()
    )

    return render_template(
        'supervisor/committee_detail.html',
        committee=committee,
        available_users=available_users,
        portfolio=current_user.portfolio
    )
# ============================================================
# ADD COMMITTEE MEMBER
# ============================================================

@supervisor_bp.route(
    '/committees/<int:committee_id>/members/add',
    methods=['POST']
)
@login_required
@role_required('supervisor')
def add_committee_member(committee_id):

    committee = Committee.query.get_or_404(committee_id)

    # Portfolio security check
    if committee.portfolio != current_user.portfolio:
        flash('Permission denied.', 'danger')
        return redirect(url_for('supervisor.committees'))

    user_id = request.form.get('user_id')

    if not user_id:
        flash('Please select a community user.', 'warning')
        return redirect(
            url_for(
                'supervisor.committee_detail',
                committee_id=committee.id
            )
        )

    user = User.query.get(user_id)

    if not user:
        flash('User not found.', 'danger')
        return redirect(
            url_for(
                'supervisor.committee_detail',
                committee_id=committee.id
            )
        )

    # User must belong to the same portfolio
    if user.portfolio != current_user.portfolio:
        flash('You can only add users from your portfolio.', 'danger')
        return redirect(
            url_for(
                'supervisor.committee_detail',
                committee_id=committee.id
            )
        )

    # Prevent duplicate membership
    if committee.members.filter_by(id=user.id).first():
        flash('This user is already a committee member.', 'warning')
        return redirect(
            url_for(
                'supervisor.committee_detail',
                committee_id=committee.id
            )
        )

    committee.members.append(user)

    db.session.commit()

    flash(
        f'{user.full_name} added to the committee.',
        'success'
    )

    return redirect(
        url_for(
            'supervisor.committee_detail',
            committee_id=committee.id
        )
    )


# ============================================================
# REMOVE COMMITTEE MEMBER
# ============================================================

@supervisor_bp.route(
    '/committees/<int:committee_id>/members/<int:user_id>/remove',
    methods=['POST']
)
@login_required
@role_required('supervisor')
def remove_committee_member(committee_id, user_id):

    committee = Committee.query.get_or_404(committee_id)

    # Portfolio security check
    if committee.portfolio != current_user.portfolio:
        flash('Permission denied.', 'danger')
        return redirect(url_for('supervisor.committees'))

    user = User.query.get_or_404(user_id)

    # Check membership
    if not committee.members.filter_by(id=user.id).first():
        flash('User is not a member of this committee.', 'warning')
        return redirect(
            url_for(
                'supervisor.committee_detail',
                committee_id=committee.id
            )
        )

    committee.members.remove(user)

    db.session.commit()

    flash(
        f'{user.full_name} removed from the committee.',
        'success'
    )

    return redirect(
        url_for(
            'supervisor.committee_detail',
            committee_id=committee.id
        )
    )
# ============================================================
# SEND NOTICE TO COMMITTEE MEMBERS
# ============================================================
@supervisor_bp.route(
    '/committees/<int:committee_id>/notice',
    methods=['GET', 'POST']
)
@login_required
@role_required('supervisor')
def committee_notice(committee_id):

    # --------------------------------------------------------
    # GET COMMITTEE
    # --------------------------------------------------------

    committee = db.session.get(
        Committee,
        committee_id
    )

    if committee is None:

        flash(
            'Committee not found.',
            'danger'
        )

        return redirect(
            url_for('supervisor.committees')
        )

    # --------------------------------------------------------
    # SECURITY: SUPERVISOR PORTFOLIO
    # --------------------------------------------------------

    if committee.portfolio != current_user.portfolio:

        flash(
            'Permission denied.',
            'danger'
        )

        return redirect(
            url_for('supervisor.committees')
        )

    # --------------------------------------------------------
    # GET COMMITTEE MEMBERS
    # --------------------------------------------------------

    members = committee.members.all()

    # --------------------------------------------------------
    # SEND NOTICE
    # --------------------------------------------------------

    if request.method == 'POST':

        message = request.form.get(
            'message',
            ''
        ).strip()

        # ----------------------------------------------------
        # VALIDATE MESSAGE
        # ----------------------------------------------------

        if not message:

            flash(
                'Notice message is required.',
                'warning'
            )

            return render_template(
                'supervisor/committee_notice.html',
                committee=committee,
                members=members,
                portfolio=current_user.portfolio
            )

        # ----------------------------------------------------
        # CHECK MEMBERS
        # ----------------------------------------------------

        if not members:

            flash(
                'This committee has no members yet.',
                'warning'
            )

            return render_template(
                'supervisor/committee_notice.html',
                committee=committee,
                members=members,
                portfolio=current_user.portfolio
            )

        # ----------------------------------------------------
        # CREATE NOTIFICATION FOR EACH MEMBER
        # ----------------------------------------------------

        notification_count = 0

        for member in members:

            notification = Notification(
                title=f"Committee Notice: {committee.name}",
                message=message,
                user_id=member.id,
                role_target="user",
                portfolio=committee.portfolio,
                notification_type="committee",
                is_read=False
            )

            db.session.add(
                notification
            )

            notification_count += 1

        # ----------------------------------------------------
        # SAVE ALL NOTIFICATIONS
        # ----------------------------------------------------

        db.session.commit()

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        flash(
            f'Notice sent successfully to '
            f'{notification_count} committee member(s).',
            'success'
        )

        return redirect(
            url_for(
                'supervisor.committee_detail',
                committee_id=committee.id
            )
        )

    # --------------------------------------------------------
    # DISPLAY NOTICE FORM
    # --------------------------------------------------------

    return render_template(
        'supervisor/committee_notice.html',
        committee=committee,
        members=members,
        portfolio=current_user.portfolio
    )
