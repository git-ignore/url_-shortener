from playhouse.shortcuts import model_to_dict
from flask_restful import Resource
from api.v1.models import User, Url
from api.v1.auth import auth
from api.v1.helpers import api_response_success


class CurrentUser(Resource):

    @auth.login_required
    def get(self):
        user_data = self.get_user_by_login(auth.username())
        return api_response_success(user_data, 200)

    @staticmethod
    def get_user_by_login(login):
        try:
            user_data = model_to_dict(User.get(User.login == login))
        except User.DoesNotExist:
            user_data = None

        if user_data:
            user_data["links_created"] = Url.select().where(Url.author_id == user_data["id"]).count()
            del user_data["password"]
            return user_data
        else:
            return False
