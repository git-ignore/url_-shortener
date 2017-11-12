import requests
from flask_restful import Resource, reqparse

from api.helpers import select_all, hash_string
from api.v1.Auth import auth
from api.v1.CurrentUser import CurrentUser
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
                # TODO: current server adress
                "shortlink": "http://localhost:8080/api/v1/shorten_urls/" + link["hash"]
            })
        return user_links

    @auth.login_required
    def post(self):
        link = self.reqparse.parse_args()
        user = CurrentUser.get_user_by_login(auth.username())
        return self.add_url(link, user), 201

    def add_url(self, link, user):

        if self.is_url_valid(link["url"]):
            url_hash = hash_string(link["url"])
            url, created = Url.get_or_create(
                hash=url_hash,
                author_id=user["id"],
                defaults={
                    'url': link["url"]
                }
            )
            return created
        else:
            return False

    @staticmethod
    def is_url_valid(link):

        # TODO: add http if link doesnt starts with it
        if not link.startswith("http://"):
            link = "http://" + link

        try:
            r_status = requests.get(link).status_code
        except requests.exceptions.ConnectionError:
            return False
        return r_status < 400
