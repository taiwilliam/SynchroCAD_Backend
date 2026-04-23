"""
User Controller - API logic layer.
Handles user request/response processing.
"""
from app.services import UserService
from app.http import error_response, success_response


class UserController:

    @staticmethod
    def list():
        try:
            users = UserService.list()
            users_data = [
                {
                    "id": u.id,
                    "name": u.name,
                    "email": u.email
                }
                for u in users
            ]
            return success_response(users_data, "Users retrieved successfully")
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def get(user_id):
        try:
            user = UserService.get(user_id)
            user_data = {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            return success_response(user_data, "User retrieved successfully")
        except ValueError as e:
            return error_response(str(e), 404)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def create(data):
        try:
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            
            user = UserService.create(name, email, password)
            user_data = {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            return success_response(user_data, "User created successfully", 201)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def update(user_id, data):
        try:
            # 只允許更新 name 和 email
            update_data = {}
            if "name" in data:
                update_data["name"] = data["name"]
            if "email" in data:
                update_data["email"] = data["email"]
            
            if not update_data:
                return error_response("No fields to update", 400)
            
            user = UserService.update(user_id, **update_data)
            user_data = {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            return success_response(user_data, "User updated successfully")
        except ValueError as e:
            return error_response(str(e), 400 if "not found" not in str(e) else 404)
        except Exception as e:
            return error_response(str(e), 500)
    
    @staticmethod
    def delete(user_id):
        try:
            UserService.delete(user_id)
            return success_response(None, "User deleted successfully")
        except ValueError as e:
            return error_response(str(e), 404)
        except Exception as e:
            return error_response(str(e), 500)
