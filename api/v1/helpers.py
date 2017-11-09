from playhouse.shortcuts import model_to_dict
import base64


def select_all(model):
    result = []
    for row in model.select().execute():
        result.append(model_to_dict(row))
    return result


def b64_encode(string):
    return base64.b64encode(string.encode())
