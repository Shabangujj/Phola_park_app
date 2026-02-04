from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

db = SQLAlchemy()

# ===================================================
# DATABASE SETUP
# ===================================================

def get_db_path():
    """
    Return absolute path to SQLite database.
    Cross-platform (Windows/Linux).
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, ".."))
    instance_folder = os.path.join(project_root, "instance")

    os.makedirs(instance_folder, exist_ok=True)

    return os.path.join(instance_folder, "phola_park_app.db")


def init_db(app):
    """
    Initialize database and create tables.
    """
    db_path = get_db_path()
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        from .model import User, Report, Notice
        db.create_all()


# ===================================================
# USER HELPERS
# ===================================================

def get_user_by_username(username):
    from .model import User
    return User.query.filter_by(username=username).first()


def get_user_by_id(user_id):
    from .model import User
    return User.query.get(user_id)


# ===================================================
# REPORT HELPERS
# ===================================================

def get_user_reports(user_id, portfolio=None, start_date=None, end_date=None):
    from .model import Report

    query = Report.query.filter_by(user_id=user_id)

    if portfolio:
        query = query.filter_by(portfolio=portfolio)
    if start_date:
        query = query.filter(Report.timestamp >= start_date)
    if end_date:
        query = query.filter(Report.timestamp <= end_date)

    return query.order_by(Report.timestamp.desc()).all()


def add_report(user_id, report_type, description, category=None, image=None, portfolio=None):
    from .model import Report

    report = Report(
        user_id=user_id,
        report_type=report_type,
        description=description,
        category=category,
        image=image,
        portfolio=portfolio,
        timestamp=datetime.utcnow()
    )

    db.session.add(report)
    db.session.commit()
    return report


def delete_report(report_id):
    from .model import Report

    report = Report.query.get(report_id)
    if not report:
        return False

    db.session.delete(report)
    db.session.commit()
    return True


# ===================================================
# NOTICE HELPERS
# ===================================================

def get_all_notifications():
    from .model import Notice
    return Notice.query.order_by(Notice.created_at.desc()).all()


def get_user_notifications(portfolio=None):
    from .model import Notice

    query = Notice.query
    if portfolio:
        query = query.filter(
            or_(Notice.portfolio == portfolio, Notice.portfolio.is_(None))
        )

    return query.order_by(Notice.created_at.desc()).all()


def add_notice(message, portfolio=None):
    from .model import Notice

    notice = Notice(
        message=message,
        portfolio=portfolio,
        created_at=datetime.utcnow()
    )

    db.session.add(notice)
    db.session.commit()
    return notice


def notifications_for_portfolio(portfolio):
    from .model import Notice
    return Notice.query.filter_by(portfolio=portfolio).order_by(Notice.created_at.desc()).all()


# ===================================================
# ADMIN / DASHBOARD HELPERS
# ===================================================

def get_all_reports():
    from .model import Report
    return Report.query.order_by(Report.timestamp.desc()).all()


def get_reports_by_portfolio(portfolio):
    from .model import Report
    return Report.query.filter_by(portfolio=portfolio).order_by(Report.timestamp.desc()).all()


def get_reports_summary():
    from .model import Report

    summary = {}
    portfolios = db.session.query(Report.portfolio).distinct().all()

    for (portfolio,) in portfolios:
        summary[portfolio] = Report.query.filter_by(portfolio=portfolio).count()

    return summary
