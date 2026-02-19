import os

class Config:
    SECRET_KEY = "dev-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///phola_park.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = SECRET_KEY

    # Upload settings
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "phola_park_app", "uploads")

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
