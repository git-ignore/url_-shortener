from flask_restful import Resource
from playhouse.shortcuts import model_to_dict

from api.v1.Resourses.User.CurrentUser import CurrentUser
from api.v1.auth import auth
from api.v1.models import Url, FollowUrl


class SingleUrl(Resource):

    @auth.login_required
    def get(self, id):
        user = CurrentUser.get_user_by_login(auth.username())

        # TODO: Если нет подходящей под условия ссылки
        link = Url.get(Url.id == id, Url.author_id == user["id"])
        return self.handle_raw_link(link)

    @auth.login_required
    def delete(self, id):
        user = CurrentUser.get_user_by_login(auth.username())
        return bool(Url.delete().where(Url.id == id, Url.author_id == user["id"]).execute())

    @staticmethod
    def handle_raw_link(r_link):
        r_link = model_to_dict(r_link)
        props_to_exclude = ["hash", "author_id"]

        for prop in props_to_exclude:
            del r_link[prop]

        return r_link

