from flask import Blueprint, render_template
from flask_login import login_required

web = Blueprint("web", __name__)

@web.route("/")
def home():
    return render_template("home.html")

@web.route("/login")
def login_page():
    return render_template("login.html")

@web.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")