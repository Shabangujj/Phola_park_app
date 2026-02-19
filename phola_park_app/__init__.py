from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from .extensions import db, migrate, login_manager, jwt
from .model import User

def create_app():
    app = Flask(__name__)

    # 🔐 Required secrets
    app.config["SECRET_KEY"] = "phola-park-session-secret-2026"
    app.config["JWT_SECRET_KEY"] = "phola-park-super-secure-jwt-secret-key-2026"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///phola_park.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)

    # routes
    from phola_park_app.main_routes import main_bp
    app.register_blueprint(main_bp, url_prefix="/api/v1")

    from flask import Blueprint
    from phola_park_app.api.auth import auth_api
    from phola_park_app.api.reports import reports_api
    from phola_park_app.api.health import health_api
    from phola_park_app.api.surveys import surveys_api
    from phola_park_app.api.dashboard import dashboard_api

    api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

    api_bp.register_blueprint(auth_api)
    api_bp.register_blueprint(reports_api)
    api_bp.register_blueprint(health_api)
    api_bp.register_blueprint(surveys_api)
    api_bp.register_blueprint(dashboard_api)

    app.register_blueprint(api_bp)

    print("✅ API v1 blueprint registered")

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

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
