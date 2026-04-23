from flask import request


def json_body(default=None):
    if default is None:
        default = {}
    return request.get_json(silent=True) or default
