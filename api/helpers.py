from playhouse.shortcuts import model_to_dict
import base64
import hashlib
from api.v1.Auth import auth


def select_all(model):
    result = []
    for row in model.select().execute():
        result.append(model_to_dict(row))
    return result


def b64_encode(string):
    return base64.b64encode(string.encode())


def hash_string(string):
        return hashlib.sha1((string+auth.username()).encode("UTF-8")).hexdigest()[:12]

# def get_user_by_login(login):
#     user_info = User.get(User.login == auth.username())
#     return model_to_dict(user_info)