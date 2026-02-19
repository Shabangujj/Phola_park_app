import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
import pytest
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""

    app = Flask(__name__)

    # Test configuration
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret"

    # Initialize JWT
    JWTManager(app)

    # ---------- Routes ----------

    @app.route("/user", methods=["GET"])
    def user_route():
        return jsonify(message="user"), 200

    @app.route("/admin", methods=["GET"])
    def admin_route():
        return jsonify(message="admin"), 200

    # ----------------------------

    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()




@pytest.fixture
def admin_token(app):
    with app.app_context():
        return create_access_token(
            identity=1,
            additional_claims={
                "role": "admin",
                "permissions": ["manage_users"]
            }
        )


@pytest.fixture
def user_token(app):
    with app.app_context():
        return create_access_token(
            identity=2,
            additional_claims={
                "role": "user",
                "permissions": []
            }
        )
