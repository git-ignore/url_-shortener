from flask_restful import Resource
from playhouse.shortcuts import model_to_dict

from api.v1.Auth import auth
from api.v1.CurrentUser import CurrentUser
from api.v1.models import Url, FollowUrl


class SingleUrl(Resource):

    @auth.login_required
    def get(self, id):
        user = CurrentUser.get_user_by_login(auth.username())

        # TODO: Если нет подходящей под условия ссылки
        link = Url.get(Url.id == id, Url.author_id == user["id"])
        return self.handle_raw_link(link)

    @staticmethod
    def handle_raw_link(r_link):
        r_link = model_to_dict(r_link)
        return {
            "id": r_link["id"],
            "origUrl": r_link["url"],
            "shortUrl": "http://localhost:8080/api/v1/shorten_urls/" + r_link["hash"],
            "countOfRedirects":  FollowUrl.select().where(FollowUrl.url_hash == r_link["hash"]).count()
        }
