import requests
from flask_restful import Resource, reqparse
from config import WRONG_RESPONSE_CODES
from flask import request


from api.v1.Resourses.User.CurrentUser import CurrentUser
from api.v1.auth import auth
from api.v1.helpers import select_all, hash_string
from api.v1.models import Url


class Urls(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, required=True, help='No link provided', location='json')
        super(Urls, self).__init__()

    @auth.login_required
    def get(self):
        user = CurrentUser.get_user_by_login(auth.username())
        raw_links = select_all(Url.select(Url.url, Url.hash).where(Url.author_id == user["id"]))
        user_links = []

        for link in raw_links:
            user_links.append({
                "id": link["id"],
                "url": link["url"],
                "shortlink": link["short_url"]
            })
        return user_links

    @auth.login_required
    def post(self):
        link = self.reqparse.parse_args()
        user = CurrentUser.get_user_by_login(auth.username())
        return self.add_url(link, user), 201

    def add_url(self, link, user):
        link["url"] = self.check_http(link["url"])
        if self.is_url_valid(link["url"]):
            url_hash = hash_string(link["url"])
            url, created = Url.get_or_create(
                hash=url_hash,
                author_id=user["id"],
                defaults={
                    'url': link["url"],
                    'short_url': '%sapi/v1/shorten_urls/%s' % (request.host_url, url_hash)
                }
            )
            return created
        else:
            return False

    @staticmethod
    def is_url_valid(link):

        try:
            r_status = requests.get(link).status_code
        except requests.exceptions.ConnectionError:
            return False

        print(r_status)
        print(WRONG_RESPONSE_CODES)
        # TODO: иногда существующие сайты отдают 403 и все идет мимо
        return r_status not in WRONG_RESPONSE_CODES

    @staticmethod
    def check_http(link):
        if not link.startswith("http"):
            link = "http://" + link
        return link
