from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth_bp.login"

def create_app(config_name):
    from . import routes
    from . import auth
    # from .assets import compile_assets

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


    app.register_blueprint(routes.main_bp)
    app.register_blueprint(auth.auth_bp)

    # # Compile static assets
    # if app.config['FLASK_ENV'] == 'development':
    #     compile_assets(app)

    db.init_app(app)
    login_manager.init_app(app)

    # Create Database Models
    
    with app.app_context():
        db.create_all() 

    return app