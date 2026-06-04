from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from collections import Counter

from phola_park_app.extensions import db
from phola_park_app.model import Survey, Report, User, Announcement, Committee
from phola_park_app.utils.permissions import role_required

supervisor_bp = Blueprint('supervisor', __name__, url_prefix='/supervisor')


@supervisor_bp.route('/dashboard')
@login_required
@role_required('supervisor')
def dashboard():
    portfolio = current_user.portfolio
    if not portfolio:
        flash('No portfolio assigned for your supervisor account.', 'warning')
        return redirect(url_for('auth.login'))

    reports = Report.query.filter_by(portfolio=portfolio).all()
    announcements = Announcement.query.filter_by(portfolio=portfolio).order_by(Announcement.created_at.desc()).all()

    status_counts = {
        'Pending': 0,
        'In Progress': 0,
        'Completed': 0,
        'Rejected': 0
    }

    for report in reports:
        status_counts[report.status] = status_counts.get(report.status, 0) + 1

    category_counts = Counter([r.category for r in reports if r.category])

    return render_template(
        'supervisor_dashboard.html',
        portfolio=portfolio,
        stats={
            'total': len(reports),
            'open': status_counts.get('Pending', 0) + status_counts.get('In Progress', 0),
            'closed': status_counts.get('Completed', 0) + status_counts.get('Rejected', 0)
        },
        status_labels=list(status_counts.keys()),
        status_values=list(status_counts.values()),
        category_labels=list(category_counts.keys()),
        category_values=list(category_counts.values())
    )


@supervisor_bp.route('/reports')
@login_required
@role_required('supervisor')
def reports():
    portfolio = current_user.portfolio
    if not portfolio:
        flash('No portfolio assigned for your supervisor account.', 'warning')
        return redirect(url_for('auth.login'))

    status = request.args.get('status', 'all')
    keyword = request.args.get('keyword', '')
    start = request.args.get('start_date')
    end = request.args.get('end_date')

    query = Report.query.filter_by(portfolio=portfolio)

    if status != 'all':
        query = query.filter_by(status=status)

    if keyword:
        query = query.filter(Report.description.ilike(f'%{keyword}%'))

    if start:
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d')
            query = query.filter(Report.created_at >= start_date)
        except ValueError:
            flash('Invalid start date', 'warning')

    if end:
        try:
            end_date = datetime.strptime(end, '%Y-%m-%d')
            query = query.filter(Report.created_at <= end_date)
        except ValueError:
            flash('Invalid end date', 'warning')

    reports = query.order_by(Report.created_at.desc()).all()

    return render_template(
        'supervisor.reports.html',
        reports=reports,
        status=status,
        keyword=keyword,
        start=start,
        end=end,
        portfolio=portfolio,
    )


@supervisor_bp.route('/reports/<int:report_id>')
@login_required
@role_required('supervisor')
def report_detail(report_id):
    report = Report.query.get_or_404(report_id)

    if report.portfolio != current_user.portfolio:
        flash('Unauthorized access to this report.', 'danger')
        return redirect(url_for('supervisor.reports'))

    return render_template('supervisor_report_details.html', report=report)


@supervisor_bp.route('/reports/<int:report_id>/status', methods=['POST'])
@login_required
@role_required('supervisor')
def update_report_status(report_id):
    report = Report.query.get_or_404(report_id)

    if report.portfolio != current_user.portfolio:
        flash('Permission denied.', 'danger')
        return redirect(url_for('supervisor.reports'))

    new_status = request.form.get('status')
    if new_status not in {'pending', 'in progress', 'completed', 'rejected', 'Pending', 'In Progress', 'Completed', 'Rejected'}:
        flash('Invalid status.', 'danger')
        return redirect(url_for('supervisor.report_detail', report_id=report.id))

    report.status = new_status.title() if new_status.islower() else new_status
    comment = request.form.get('comment', '').strip()
    if comment:
        report.comment = comment
    db.session.commit()

    flash('Report status updated.', 'success')
    return redirect(url_for('supervisor.report_detail', report_id=report.id))


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
    surveys = Survey.query.order_by(Survey.created_at.desc()).all()
    return render_template('supervisor.surveys.html', surveys=surveys, portfolio=portfolio)


@supervisor_bp.route('/surveys/upload', methods=['GET', 'POST'])
@login_required
@role_required('supervisor')
def upload_new_survey():
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

    return render_template('supervisor.upload_new_survey.html')


@supervisor_bp.route('/surveys/<int:survey_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('supervisor')
def edit_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    if survey.portfolio != current_user.portfolio:
        flash('Permission denied.', 'danger')
        return redirect(url_for('supervisor.surveys'))

    if request.method == 'POST':
        survey.title = request.form.get('title')
        survey.description = request.form.get('description')
        survey.survey_type = request.form.get('survey_type')
        survey.link = request.form.get('link')
        db.session.commit()
        flash('Survey updated successfully.', 'success')
        return redirect(url_for('supervisor.surveys'))

    return render_template('edit_survey.html', survey=survey)


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
    committees = Committee.query.filter_by(portfolio=portfolio).order_by(Committee.created_at.desc()).all()
    return render_template('supervisor_committees.html', committees=committees, portfolio=portfolio)


@supervisor_bp.route('/committees/new', methods=['GET', 'POST'])
@login_required
@role_required('supervisor')
def add_committee():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        committee = Committee(
            name=name,
            description=description,
            portfolio=current_user.portfolio,
            created_by=current_user.id
        )
        db.session.add(committee)
        db.session.commit()
        flash('Committee created successfully.', 'success')
        return redirect(url_for('supervisor.committees'))

    return render_template('add_committee.html')
