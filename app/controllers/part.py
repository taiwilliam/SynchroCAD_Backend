"""
Part Controller - API logic layer.
Handles part request/response processing.
"""
from app.services.part import PartService
from app.http.responses import success_response, error_response

class PartController:
    @staticmethod
    def list():
        try:
            parts = PartService.list()
            parts_data = [serialize_part(p) for p in parts]
            return success_response(parts_data, "Parts retrieved successfully")
        except Exception as e:
            return error_response(str(e), 500)

    @staticmethod
    def get(part_id):
        try:
            part = PartService.get(part_id)
            part_data = serialize_part(part)
            return success_response(part_data, "Part retrieved successfully")
        except ValueError as e:
            return error_response(str(e), 404)
        except Exception as e:
            return error_response(str(e), 500)

    @staticmethod
    def create(data):
        try:
            part = PartService.create(data)
            part_data = serialize_part(part)
            return success_response(part_data, "Part created successfully", 201)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)

    @staticmethod
    def update(part_id, data):
        try:
            part = PartService.update(part_id, data)
            part_data = serialize_part(part)
            return success_response(part_data, "Part updated successfully")
        except ValueError as e:
            return error_response(str(e), 404)
        except Exception as e:
            return error_response(str(e), 500)

    @staticmethod
    def delete(part_id):
        try:
            PartService.delete(part_id)
            return success_response({}, "Part deleted successfully")
        except ValueError as e:
            return error_response(str(e), 404)
        except Exception as e:
            return error_response(str(e), 500)

# Helper function for serialization

def serialize_part(part):
    return {
        "id": part.id,
        "part_number": part.part_number,
        "part_name": part.part_name,
        "category_id": part.category_id,
        "material": part.material,
        "status": part.status,
        "revision": part.revision,
        "updated_at": part.updated_at.isoformat() if part.updated_at else None,
        "owner": part.owner,
        "tolerance": part.tolerance,
        "cad_file_url": part.cad_file_url,
        "model_file_url": part.model_file_url,
        "description": part.description,
        "standard": part.standard,
        "specification": part.specification,
        "project_code": part.project_code,
        "drawing_number": part.drawing_number,
    }
