from playhouse.shortcuts import model_to_dict
from flask_restful import Resource
from api.v1.models import User, Url
from api.v1.auth import auth


class CurrentUser(Resource):

    @auth.login_required
    def get(self):
        return self.get_user_by_login(auth.username())

    @staticmethod
    def get_user_by_login(login):
        try:
            user_info = model_to_dict(User.get(User.login == login))
        except User.DoesNotExist:
            user_info = None

        if user_info:
            user_info["links_created"] = Url.select().where(Url.author_id == user_info["id"]).count()
            del user_info["password"]
            return user_info
        else:
            return False
