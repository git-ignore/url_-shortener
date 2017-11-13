from playhouse.shortcuts import model_to_dict
import base64
import hashlib
from api.v1.auth import auth


def select_all(model):
    result = []
    for row in model.select().execute():
        result.append(model_to_dict(row))
    return result


def b64_encode(string):
    return base64.b64encode(string.encode())


def hash_string(string):
        return hashlib.sha1((string+auth.username()).encode("UTF-8")).hexdigest()[:12]


def error_message(error_text, status_code):
    return {
        "error": error_text
    }, status_code


# TODO: Рефакторить саксес месэдж
def success_message(message, status_code, add_info):
    if not add_info:
        return {
            "message": message
        }, status_code
    else:
        return {
            "message": message,
            "data": add_info
        }, status_code

