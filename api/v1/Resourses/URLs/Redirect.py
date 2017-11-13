from flask_restful import Resource
from api.v1.models import Url, FollowUrl
from playhouse.shortcuts import model_to_dict
from flask import redirect, request, abort


class Redirect(Resource):

    def get(self, hash):
        try:
            raw_curr_url = Url.get(Url.hash == hash)
            raw_curr_url.count_of_redirects += 1
            raw_curr_url.save()
            cur_url = model_to_dict(raw_curr_url)
            FollowUrl.insert(link_id=cur_url["id"], referrer=str(request.referrer)).execute()
            return redirect(cur_url["url"], code=302)
        except Url.DoesNotExist:
            abort(404)
