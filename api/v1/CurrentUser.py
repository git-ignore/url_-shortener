from flask_restful import Resource
from api.v1.models import User
from api.v1.Auth import auth
from playhouse.shortcuts import model_to_dict


class CurrentUser(Resource):

    @auth.login_required
    def get(self):
        user_info = User.get(User.login == auth.username())
        return model_to_dict(user_info)
