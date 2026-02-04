from flask import Flask

def create_app():
    app = Flask(__name__)

    # config
    app.config['SECRET_KEY'] = 'dev-key'

    # register blueprints here
    return app
