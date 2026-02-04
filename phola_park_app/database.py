from phola_park_app import db
from phola_park_app.model import User, Report, Notice
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy

# Create database object
db = SQLAlchemy()

def get_db_path():
    """
    Returns the correct FULL PATH to the SQLite database file.
    Works on Windows, Linux, and inside VS Code.
    """
    # Folder where THIS file lives (phola_park_app)
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Go up one folder (to main project folder)
    project_root = os.path.abspath(os.path.join(base_dir, ".."))

    # Instance folder
    instance_folder = os.path.join(project_root, "instance")

    # Ensure instance folder exists
    if not os.path.exists(instance_folder):
        os.makedirs(instance_folder)

    # Final database file path
    db_path = os.path.join(instance_folder, "phola_park_app.db")

    return db_path


def init_db(app):
    """
    Initialize DB and create tables.
    """

    db_path = get_db_path()
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        from phola_park_app.model import User   # import your models
        db.create_all()

# ===================================================
# USER HELPERS
# ===================================================
def get_user_by_username(username):
    """Return a user object by username."""
    return User.query.filter_by(username=username).first()


def get_user_by_id(user_id):
    """Return a user object by ID."""
    return User.query.get(user_id)


# ===================================================
# REPORT HELPERS
# ===================================================
def get_user_reports(user_id, portfolio=None, start_date=None, end_date=None):
    """Return reports filtered by user, portfolio, and optional date range."""
    query = Report.query.filter_by(user_id=user_id)

    if portfolio:
        query = query.filter_by(portfolio=portfolio)
    if start_date:
        query = query.filter(Report.timestamp >= start_date)
    if end_date:
        query = query.filter(Report.timestamp <= end_date)

    return query.order_by(Report.timestamp.desc()).all()


def add_report(user_id, report_type, description, category=None, image=None, portfolio=None):
    """Add a new report to the database."""
    new_report = Report(
        user_id=user_id,
        report_type=report_type,
        description=description,
        category=category,
        image=image,
        portfolio=portfolio,
        timestamp=datetime.utcnow()
    )
    db.session.add(new_report)
    db.session.commit()
    return new_report


def delete_report(report_id):
    """Delete a report by ID."""
    report = Report.query.get(report_id)
    if report:
        db.session.delete(report)
        db.session.commit()
        return True
    return False


# ===================================================
# NOTICE HELPERS
# ===================================================
def get_user_notifications(portfolio=None):
    """Get all notices visible to the user or their portfolio."""
    query = Notice.query
    if portfolio:
        query = query.filter((Notice.portfolio == portfolio) | (Notice.portfolio.is_(None)))
    return query.order_by(Notice.created_at.desc()).all()


def add_notice(message, portfolio=None):
    """Create a new notice (for admin/supervisor use)."""
    new_notice = Notice(message=message, portfolio=portfolio, created_at=datetime.utcnow())
    db.session.add(new_notice)
    db.session.commit()
    return new_notice


# ===================================================
# UTILITY HELPERS
# ===================================================
def get_all_reports():
    """Return all reports (for admin dashboard)."""
    return Report.query.order_by(Report.timestamp.desc()).all()


def get_reports_by_portfolio(portfolio):
    """Return all reports filtered by portfolio (for supervisor dashboard)."""
    return Report.query.filter_by(portfolio=portfolio).order_by(Report.timestamp.desc()).all()


def get_reports_summary():
    """Return a dictionary of report counts per portfolio."""
    portfolios = db.session.query(Report.portfolio).distinct().all()
    summary = {}
    for (portfolio,) in portfolios:
        count = Report.query.filter_by(portfolio=portfolio).count()
        summary[portfolio] = count
    return summary
