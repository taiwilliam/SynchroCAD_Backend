from flask import Flask
from app.extensions import db, migrate
from app.routers import main_bp, users_bp
from app.models import *
from app.cli import register_cli_commands

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.settings.Config')
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    register_cli_commands(app)
    return app