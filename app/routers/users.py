"""
User Router - RESTful API routes for users.
"""
import os
from flasgger import swag_from
from flask import Blueprint
from app.controllers import UserController
from app.http import json_body

# 建立 blueprint
users_bp = Blueprint('users', __name__, url_prefix='/api/users')

_docs = os.path.join(os.path.dirname(__file__), '..', 'docs', 'users')


@users_bp.route('', methods=['GET'])
@swag_from(os.path.join(_docs, 'index.yml'))
def index():
    return UserController.list()


@users_bp.route('/<int:user_id>', methods=['GET'])
@swag_from(os.path.join(_docs, 'show.yml'))
def show(user_id):
    return UserController.get(user_id)


@users_bp.route('', methods=['POST'])
@swag_from(os.path.join(_docs, 'store.yml'))
def store():
    data = json_body()
    return UserController.create(data)


@users_bp.route('/<int:user_id>', methods=['PUT'])
@swag_from(os.path.join(_docs, 'update.yml'))
def update(user_id):
    data = json_body()
    return UserController.update(user_id, data)


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@swag_from(os.path.join(_docs, 'destroy.yml'))
def destroy(user_id):
    return UserController.delete(user_id)
