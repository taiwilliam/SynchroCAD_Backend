from flask import Flask
from flasgger import Swagger
from app.extensions import db, migrate
from app.routers import main_bp, users_bp, part_bp
from app.models import *
from app.cli import register_cli_commands

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.settings.Config')

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "SynchroCAD Backend API",
            "description": "REST API documentation",
            "version": "1.0.0",
        },
        "basePath": "/",
        "schemes": ["http", "https"],
    }
    Swagger(app, template=swagger_template)

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(part_bp)
    register_cli_commands(app)
    return app