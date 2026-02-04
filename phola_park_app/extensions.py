# phola_park_app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
db = SQLAlchemy()
login_manager = LoginManager()
# migrate = Migrate()    # if you use Flask-Migrate
csrf = CSRFProtect()