"""
User Router - RESTful API routes for users.
"""
from flask import Blueprint
from app.controllers import UserController
from app.http import json_body

# 建立 blueprint
users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('', methods=['GET'])
def index():
    return UserController.list()


@users_bp.route('/<int:user_id>', methods=['GET'])
def show(user_id):
    return UserController.get(user_id)


@users_bp.route('', methods=['POST'])
def store():
    data = json_body()
    return UserController.create(data)


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update(user_id):
    data = json_body()
    return UserController.update(user_id, data)


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def destroy(user_id):
    return UserController.delete(user_id)
