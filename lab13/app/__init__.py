from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'supersecretkey'

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

        from .views import main_bp
        app.register_blueprint(main_bp, url_prefix='/')  # Ensure URL prefix is correct

    return app
