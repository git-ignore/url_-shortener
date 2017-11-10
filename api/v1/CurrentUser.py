from flask_restful import Resource
from api.v1.models import User
from api.v1.Auth import auth
from playhouse.shortcuts import model_to_dict


class CurrentUser(Resource):

    @auth.login_required
    def get(self):
        return self.get_user_by_login(auth.username())

    @staticmethod
    def get_user_by_login(login):
        user_info = User.get(User.login == login)
        return model_to_dict(user_info)
