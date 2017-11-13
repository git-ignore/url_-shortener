from flask_restful import Resource
from playhouse.shortcuts import model_to_dict
from api.v1.helpers import error_message, success_message
from api.v1.Resourses.User.CurrentUser import CurrentUser
from api.v1.auth import auth
from api.v1.models import Url


class SingleUrl(Resource):

    @auth.login_required
    def get(self, url_id):
        user = CurrentUser.get_user_by_login(auth.username())

        try:
            link = Url.get(Url.id == url_id, Url.author_id == user["id"])
            return success_message("Success", 200, self.handle_raw_link(link))
        except Url.DoesNotExist:
            return error_message("User hasn't link with provided id", 400)

    @auth.login_required
    def delete(self, url_id):
        user = CurrentUser.get_user_by_login(auth.username())
        deleted = bool(Url.delete().where(Url.id == url_id, Url.author_id == user["id"]).execute())

        if deleted:
            return success_message("link successfully deleted", 200, False)
        else:
            return error_message("User hasn't link with provided id", 400)

    @staticmethod
    def handle_raw_link(r_link):
        r_link = model_to_dict(r_link)
        props_to_exclude = ["hash", "author_id"]

        for prop in props_to_exclude:
            del r_link[prop]
        return r_link

