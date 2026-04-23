"""
User Repository - Database access layer for User model.
"""
from app.extensions import db
from app.models.user import User


class UserRepository:
    @staticmethod
    def list(limit=None, offset=None):
        query = User.query
        if limit:
            query = query.limit(limit).offset(offset or 0)
        return query.all()
    
    @staticmethod
    def get(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def create(name, email, password):
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update(user_id, **kwargs):
        user = User.query.get(user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user_id):
        user = User.query.get(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True
    
    @staticmethod
    def count():
        return User.query.count()
