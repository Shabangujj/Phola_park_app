from flask import Flask, jsonify, Blueprint
from werkzeug.exceptions import HTTPException

from .extensions import db, migrate, login_manager, jwt
from .model import User
from config import Config   # ✅ import config class


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super_secret_key_123'  # Change this in production
    # ✅ Load configuration from config.py
    app.config.from_object(Config)

    # 🔧 Optional overrides (if needed)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600

    # -------------------------
    # Initialize extensions
    # -------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
      return User.query.get(int(user_id))

    # -------------------------
    # Register API blueprints
    # -------------------------
    from .routes import register_routes
    from phola_park_app.api.auth import auth_api
    from phola_park_app.api.notifications import notifications_api
    from phola_park_app.api.reports import reports_api
    from phola_park_app.api.health import health_api
    from phola_park_app.api.surveys import surveys_api
    from phola_park_app.api.dashboard import dashboard_api

    api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

    api_bp.register_blueprint(auth_api)
    api_bp.register_blueprint(reports_api)
    api_bp.register_blueprint(notifications_api)
    api_bp.register_blueprint(health_api)
    api_bp.register_blueprint(surveys_api)
    api_bp.register_blueprint(dashboard_api)
    register_routes(app)

    app.register_blueprint(api_bp)

    print("✅ API v1 blueprint registered")

    # -------------------------
    # Login manager
    # -------------------------
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # -------------------------
    # JSON error handling
    # -------------------------
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = e.get_response()
        response.data = jsonify({
            "error": e.name,
            "message": e.description
        }).data
        response.content_type = "application/json"
        return response

    return app
