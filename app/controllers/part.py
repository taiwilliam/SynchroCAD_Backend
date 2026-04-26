"""
Part Controller - API logic layer.
Handles part request/response processing.
"""
from app.services.s3 import s3
from app.services.part import PartService
from app.http.responses import success_response, error_response


class PartController:
    @staticmethod
    def list():
        try:
            parts = PartService.list()
            return success_response([serialize_part(p) for p in parts], "Parts retrieved successfully")
        except Exception as e:
            return error_response(str(e), 500)

    @staticmethod
    def get(part_id):
        try:
            part = PartService.get(part_id)
            return success_response(serialize_part(part), "Part retrieved successfully")
        except ValueError as e:
            return error_response(str(e), 404)
        except Exception as e:
            return error_response(str(e), 500)

    @staticmethod
    def create(data):
        try:
            part = PartService.create(data)
            return success_response(serialize_part(part), "Part created successfully", 201)
        except ValueError as e:
            return error_response(str(e), 400)
        except Exception as e:
            return error_response(str(e), 500)

    @staticmethod
    def update(part_id, data):
        try:
            part = PartService.update(part_id, data)
            return success_response(serialize_part(part), "Part updated successfully")
        except ValueError as e:
            return error_response(str(e), 404)
        except Exception as e:
            return error_response(str(e), 500)

    @staticmethod
    def upload_file(part_id, folder, field, file):
        try:
            if not file or file.filename == "":
                return error_response("No file provided", 400)
            if not folder:
                return error_response("folder is required", 400)
            if field not in ("cad_file_url", "model_file_url"):
                return error_response("field must be 'cad_file_url' or 'model_file_url'", 400)
            key = s3.upload(file, folder, file.filename)
            part = PartService.update(part_id, {field: key})
            return success_response(serialize_part(part), "File uploaded successfully")
        except ValueError as e:
            return error_response(str(e), 400)
        except RuntimeError as e:
            return error_response(str(e), 502)
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
        "cad_file_url": s3.url(part.cad_file_url),
        "model_file_url": s3.url(part.model_file_url),
        "description": part.description,
        "standard": part.standard,
        "specification": part.specification,
        "project_code": part.project_code,
        "drawing_number": part.drawing_number,
    }
