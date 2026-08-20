"""
====================================================
JJCORETECH
Phola Park App

Application Factory
====================================================
"""

# ------------------------------------------------------------------
# Compatibility patches
# ------------------------------------------------------------------

import flask as _flask

try:
    # Flask 3 compatibility
    from markupsafe import Markup as _Markup
    setattr(_flask, "Markup", _Markup)
except Exception:
    pass

try:
    import werkzeug.urls as _w_urls

    if not hasattr(_w_urls, "url_encode"):
        from urllib.parse import urlencode as _url_encode
        setattr(_w_urls, "url_encode", _url_encode)

except Exception:
    pass


# ------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from config import Config

from .extensions import (
    db,
    migrate,
    login_manager,
    csrf,
    jwt
)

from .models import User


# ------------------------------------------------------------------
# Application Factory
# ------------------------------------------------------------------

def create_app():

    app = Flask(__name__)

    # --------------------------------------------------------------
    # Load configuration
    # --------------------------------------------------------------

    app.config.from_object(Config)

    # --------------------------------------------------------------
    # Initialize Extensions
    # --------------------------------------------------------------

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )
    csrf.init_app(app)
    login_manager.init_app(app)

    jwt.init_app(app)

    login_manager.login_view = "auth.login"

    login_manager.login_message_category = "warning"

    # --------------------------------------------------------------
    # Flask-Login
    # --------------------------------------------------------------

    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(
            User,
            int(user_id)
        )

    # --------------------------------------------------------------
    # Register Website Routes
    # --------------------------------------------------------------

    from .routes import register_routes

    register_routes(app)

    # --------------------------------------------------------------
    # Register Admin Blueprint
    # --------------------------------------------------------------

    from .routes.admin import admin_bp

    app.register_blueprint(admin_bp)

    # --------------------------------------------------------------
    # Register API Blueprint
    # --------------------------------------------------------------

    from .api.auth import auth_api
    from .api.notifications import notifications_api
    from .api.reports import reports_api
    from .api.health import health_api
    from .api.surveys import surveys_api
    from .api.analytics import analytics_api
    announcements_api = None
    try:
        from .api.announcements import announcements_api
    except ImportError:
        pass

    from .api.dashboard import dashboard_api

    announcements_api = None
    uploads_api = None
    try:
        import importlib

        announcements_module = importlib.import_module(
            "phola_park_app.api.announcements"
        )
        announcements_api = getattr(announcements_module, "announcements_api", None)

        uploads_module = importlib.import_module(
            "phola_park_app.api.uploads"
        )
        uploads_api = getattr(uploads_module, "uploads_api", None)
    except ImportError:
        pass

    from flask import Blueprint

    api_bp = Blueprint(
        "api",
        __name__,
        url_prefix="/api/v1"
    )

    api_bp.register_blueprint(auth_api)

    api_bp.register_blueprint(reports_api)

    api_bp.register_blueprint(notifications_api)

    api_bp.register_blueprint(health_api)

    api_bp.register_blueprint(surveys_api)

    api_bp.register_blueprint(analytics_api)

    if announcements_api is not None:
        api_bp.register_blueprint(announcements_api)

    api_bp.register_blueprint(dashboard_api)

    if uploads_api is not None:
        api_bp.register_blueprint(uploads_api)

    app.register_blueprint(api_bp)

    print("✓ API v1 Registered")

    # --------------------------------------------------------------
    # Health Check
    # --------------------------------------------------------------

    @app.route("/health")

    def health():

        return jsonify({

            "status": "OK",

            "application": "Phola Park App",

            "version": "1.0"

        })

    # --------------------------------------------------------------
    # JSON HTTP Errors
    # --------------------------------------------------------------

    @app.errorhandler(HTTPException)

    def handle_http_error(error):

        response = error.get_response()

        response.data = jsonify({

            "success": False,

            "error": error.name,

            "message": error.description

        }).data

        response.content_type = "application/json"

        return response

    # --------------------------------------------------------------
    # Unexpected Errors
    # --------------------------------------------------------------

    @app.errorhandler(Exception)

    def handle_exception(error):

        app.logger.exception(error)

        return jsonify({

            "success": False,

            "error": "Internal Server Error",

            "message": str(error)

        }), 500

    # --------------------------------------------------------------
    # Create Database (Development Only)
    # --------------------------------------------------------------

    with app.app_context():

        db.create_all()

    print("✓ Database Ready")

    print("✓ Application Started Successfully")

    return app