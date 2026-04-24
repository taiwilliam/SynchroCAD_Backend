"""
Part Service - Business logic layer for Part.
"""
from app.repositories.part import PartRepository
from datetime import datetime

class PartService:
    @staticmethod
    def list():
        return PartRepository.list()

    @staticmethod
    def get(part_id):
        part = PartRepository.get(part_id)
        if not part:
            raise ValueError(f"Part with ID {part_id} not found")
        return part

    @staticmethod
    def create(data):
        # 處理 updated_at 格式
        if data.get('updated_at'):
            data['updated_at'] = datetime.strptime(data['updated_at'], '%Y/%m/%d')
        return PartRepository.create(**data)

    @staticmethod
    def update(part_id, data):
        if data.get('updated_at'):
            data['updated_at'] = datetime.strptime(data['updated_at'], '%Y/%m/%d')
        part = PartRepository.update(part_id, **data)
        if not part:
            raise ValueError(f"Part with ID {part_id} not found")
        return part

    @staticmethod
    def delete(part_id):
        ok = PartRepository.delete(part_id)
        if not ok:
            raise ValueError(f"Part with ID {part_id} not found")
        return True

    @staticmethod
    def list_categories():
        return PartRepository.list_categories()

    @staticmethod
    def get_category_by_name(name):
        return PartRepository.get_category_by_name(name)

    @staticmethod
    def create_category(name):
        return PartRepository.create_category(name)
