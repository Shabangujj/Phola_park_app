import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "phola_park.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
