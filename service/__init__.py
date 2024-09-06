# service/__init__.py

from flask import Flask
from .config import DevelopmentConfig
from .extensions import db, migrate
from .auth import auth_bp
from .posts import posts_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)

    return app
