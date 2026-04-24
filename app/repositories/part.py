"""
Part Repository - Database access layer for Part model.
"""
from app.extensions import db
from app.models.part import Part, PartCategory

class PartRepository:
    @staticmethod
    def list():
        return Part.query.all()

    @staticmethod
    def get(part_id):
        return Part.query.get(part_id)

    @staticmethod
    def create(**kwargs):
        part = Part(**kwargs)
        db.session.add(part)
        db.session.commit()
        return part

    @staticmethod
    def update(part_id, **kwargs):
        part = Part.query.get(part_id)
        if not part:
            return None
        for key, value in kwargs.items():
            if hasattr(part, key):
                setattr(part, key, value)
        db.session.commit()
        return part

    @staticmethod
    def delete(part_id):
        part = Part.query.get(part_id)
        if not part:
            return False
        db.session.delete(part)
        db.session.commit()
        return True

    @staticmethod
    def list_categories():
        return PartCategory.query.all()

    @staticmethod
    def get_category_by_name(name):
        return PartCategory.query.filter_by(name=name).first()

    @staticmethod
    def create_category(name):
        category = PartCategory(name=name)
        db.session.add(category)
        db.session.commit()
        return category
