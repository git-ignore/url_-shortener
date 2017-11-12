from flask_restful import Resource
from api.v1.models import Url, FollowUrl
from playhouse.shortcuts import model_to_dict
from flask import redirect, request


class Redirect(Resource):

    def get(self, hash):
        FollowUrl.insert(url_hash=hash, referrer=str(request.referrer)).execute()
        link = model_to_dict(Url.get(Url.hash == hash))
        return redirect(link["url"], code=302)
