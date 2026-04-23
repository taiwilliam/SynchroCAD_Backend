"""
User Service - Business logic layer.
"""
from app.repositories import UserRepository


class UserService:
    
    @staticmethod
    def list(limit=None, offset=None):
        return UserRepository.list(limit=limit, offset=offset)
    
    @staticmethod
    def get(user_id):
        user = UserRepository.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        return user
    
    @staticmethod
    def create(name, email, password):
        # 驗證
        if not name or not email or not password:
            raise ValueError("Name, email, and password are required")
        
        if len(name) < 2:
            raise ValueError("Name must be at least 2 characters")
        
        if "@" not in email:
            raise ValueError("Invalid email format")
        
        # 檢查 email 是否已存在
        existing = UserRepository.get_by_email(email)
        if existing:
            raise ValueError(f"Email {email} already exists")
        
        return UserRepository.create(name, email, password)
    
    @staticmethod
    def update(user_id, **kwargs):
        user = UserRepository.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        # 驗證
        if "email" in kwargs and kwargs["email"] != user.email:
            existing = UserRepository.get_by_email(kwargs["email"])
            if existing:
                raise ValueError(f"Email {kwargs['email']} already exists")
        
        return UserRepository.update(user_id, **kwargs)
    
    @staticmethod
    def delete(user_id):
        user = UserRepository.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        return UserRepository.delete(user_id)
