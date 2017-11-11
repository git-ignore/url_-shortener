from flask_restful import Resource
from api.v1.models import Url
from playhouse.shortcuts import model_to_dict
from flask import redirect


class Redirect(Resource):

    def get(self, hash):
        link = model_to_dict(Url.get(Url.hash == hash))
        return redirect(link["url"], code=302)
