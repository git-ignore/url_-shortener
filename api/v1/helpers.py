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


def api_response_error(error_text, status_code):
    return {
        "error": error_text
    }, status_code


def api_response_success(data, status_code):
    if type(data) in [dict, list]:
        return {
            "data": data
        }, status_code
    elif type(data) in [str, int]:
        return {
            "message": data
        }, status_code
    else:
        api_response_error("Internal server error", 500)


def time_to_string(time):
        return time.strftime('%d.%m.%Y %H:%M')
