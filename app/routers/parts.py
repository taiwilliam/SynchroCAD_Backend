"""
Parts Router - RESTful API routes for parts.
"""
import os
from flasgger import swag_from
from flask import Blueprint
from app.controllers.part import PartController
from app.http import json_body

part_bp = Blueprint('parts', __name__, url_prefix='/api/parts')
_docs = os.path.join(os.path.dirname(__file__), '..', 'docs', 'parts')

@part_bp.route('', methods=['GET'])
@swag_from(os.path.join(_docs, 'index.yml'))
def index():
    return PartController.list()

@part_bp.route('/<int:part_id>', methods=['GET'])
@swag_from(os.path.join(_docs, 'show.yml'))
def show(part_id):
    return PartController.get(part_id)

@part_bp.route('', methods=['POST'])
@swag_from(os.path.join(_docs, 'store.yml'))
def store():
    data = json_body()
    return PartController.create(data)

@part_bp.route('/<int:part_id>', methods=['PUT'])
@swag_from(os.path.join(_docs, 'update.yml'))
def update(part_id):
    data = json_body()
    return PartController.update(part_id, data)

@part_bp.route('/<int:part_id>', methods=['DELETE'])
@swag_from(os.path.join(_docs, 'destroy.yml'))
def destroy(part_id):
    return PartController.delete(part_id)
