# Import route blueprints
from .auth_routes import auth_bp
from .survey_routes import surveys_bp
from .reports_routes import reports_bp
from .health_routes import health_bp
from .dashboard_routes import dashboard_bp
from .main_routes import main_bp
from .web_routes import web
from .admin_routes import admin_bp
from .supervisor_routes import supervisor_bp
from .user_routes import user_bp

# Optional blueprint (safe import)
try:
    from .notifications_routes import notifications_bp
except ImportError:
    notifications_bp = None


def register_routes(app):
    """
    Register all application blueprints
    """

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(supervisor_bp)
    app.register_blueprint(user_bp)

    app.register_blueprint(surveys_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(health_bp)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(web)

    # register only if exists
    if notifications_bp:
        app.register_blueprint(notifications_bp)