from flask import Blueprint
from app.controllers.main import hello

main_bp = Blueprint('main', __name__)

main_bp.route('/')(hello)
