from flask_restful import Resource
from playhouse.shortcuts import model_to_dict
from api.v1.Resourses.User.CurrentUser import CurrentUser
from api.v1.auth import auth
from api.v1.models import Url, FollowUrl
from api.v1.helpers import select_all


class ReferrersReport(Resource):

    @auth.login_required
    def get(self, id):
        # user = CurrentUser.get_user_by_login(auth.username())
        redirects = FollowUrl.select().where(FollowUrl.link_id == id).execute()
        referer_stat = {}
        for row in redirects:
            redirect = model_to_dict(row)
            if redirect["referrer"] not in referer_stat:
                referer_stat[redirect["referrer"]] = 1
            else:
                referer_stat[redirect["referrer"]] += 1
        return referer_stat
        # return select_all(redirects)

    # @auth.login_required
    # def delete(self, id):
    #     user = CurrentUser.get_user_by_login(auth.username())
    #     return bool(Url.delete().where(Url.id == id, Url.author_id == user["id"]).execute())
    #
    # @staticmethod
    # def handle_raw_link(r_link):
    #     r_link = model_to_dict(r_link)
    #     return {
    #         "id": r_link["id"],
    #         "origUrl": r_link["url"],
    #         "shortUrl": "http://localhost:8080/api/v1/shorten_urls/" + r_link["hash"],
    #         "countOfRedirects":  FollowUrl.select().where(FollowUrl.url_hash == r_link["hash"]).count()
    #     }
