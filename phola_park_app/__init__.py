import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import current_user
from flask_wtf import CSRFProtect
from .extensions import db, login_manager, csrf
from .model import User
from .utils.notifications import get_unread_notifications
def create_app():
    app = Flask(__name__)

    # ─────────────────────────────────────────────
    # CONFIG
    # ─────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///phola_park_app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["WTF_CSRF_ENABLED"] = True
    
    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "static", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ─────────────────────────────────────────────
    # EXTENSIONS
    # ─────────────────────────────────────────────
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    Migrate(app, db)
    csrf = CSRFProtect()
    csrf.init_app(app)

    # ─────────────────────────────────────────────
    # LOGIN MANAGER
    # ─────────────────────────────────────────────
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ─────────────────────────────────────────────
    # ERROR HANDLERS
    # ─────────────────────────────────────────────
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    # ─────────────────────────────────────────────
    # CONTEXT PROCESSORS
    # ─────────────────────────────────────────────
    @app.context_processor
    def inject_notifications():
        if current_user.is_authenticated:
            return {
                "unread_notifications": get_unread_notifications(current_user)
            }
        return {}

    # ─────────────────────────────────────────────
    # BLUEPRINTS
    # ─────────────────────────────────────────────
    from phola_park_app.auth_old import auth_bp, setup_defaults
    from phola_park_app.main_routes import main_bp
    from phola_park_app.admin_routes import admin_bp
    from phola_park_app.supervisor_routes import supervisor_bp
    from phola_park_app.user_routes import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(supervisor_bp)
    app.register_blueprint(user_bp)

    # ─────────────────────────────────────────────
    # DEFAULT DATA (SAFE TO RUN MULTIPLE TIMES)
    # ─────────────────────────────────────────────
    with app.app_context():
        setup_defaults()
       # print("CSRF token available:", hasattr(csrf, 'csrf_token'))
        
        
        

    return app
