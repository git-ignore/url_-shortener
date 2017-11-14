from flask_restful import Resource
from playhouse.shortcuts import model_to_dict
from api.v1.helpers import api_response_error, api_response_success
from api.v1.Resourses.User.CurrentUser import CurrentUser
from api.v1.auth import auth
from api.v1.models import Url
from api.v1.helpers import time_to_string


class SingleUrl(Resource):

    @auth.login_required
    def get(self, url_id):
        user = CurrentUser.get_user_by_login(auth.username())

        try:
            link = Url.get(Url.id == url_id, Url.author_id == user["id"])
            return api_response_success(self.handle_raw_link(link), 200)
        except Url.DoesNotExist:
            return api_response_error("User hasn't link with provided id", 404)

    @auth.login_required
    def delete(self, url_id):
        user = CurrentUser.get_user_by_login(auth.username())
        deleted = bool(Url.delete().where(Url.id == url_id, Url.author_id == user["id"]).execute())

        if deleted:
            return api_response_success("Link was successfully deleted", 204)
        else:
            return api_response_error("User hasn't link with provided id", 404)

    @staticmethod
    def handle_raw_link(r_link):
        r_link = model_to_dict(r_link)
        props_to_exclude = ["hash", "author_id"]
        r_link["created"] = time_to_string(r_link["created"])

        for prop in props_to_exclude:
            del r_link[prop]
        return r_link

