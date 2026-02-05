from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # --------------------------------------------------
    # CONFIG
    # --------------------------------------------------
    app.config.from_object("phola_park_app.settings")

    # --------------------------------------------------
    # EXTENSIONS
    # --------------------------------------------------
    from phola_park_app.extensions import db, login_manager, csrf

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # --------------------------------------------------
    # WEB (UI) ROUTES
    # --------------------------------------------------
    from phola_park_app.routes import main_bp
    app.register_blueprint(main_bp)

    # --------------------------------------------------
    # API ROUTES
    # --------------------------------------------------
    from phola_park_app.api import api_bp
    app.register_blueprint(api_bp)

    print("✅ API blueprint registered")

    return app
