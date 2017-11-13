from playhouse.shortcuts import model_to_dict
import base64
import hashlib
from api.v1.auth import auth


def select_all(model):
    result = []
    for row in model.select().execute():
        print(model_to_dict(row))
        result.append(model_to_dict(row))
    return result


def b64_encode(string):
    return base64.b64encode(string.encode())


def hash_string(string):
        return hashlib.sha1((string+auth.username()).encode("UTF-8")).hexdigest()[:12]



