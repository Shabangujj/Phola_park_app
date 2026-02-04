# phola_park_app/settings.py
import os

class DevConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///phola.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
