from flask_restful import Resource, reqparse
from api.v1.models import User
from api.v1.auth import hash_password
from api.v1.helpers import api_response_error, api_response_success
from api.v1.messages import MSG_LOGIN_EXISTS, MSG_USER_REGISTERED, MSG_WRONG_LOGIN, MSG_NO_LIGON_PROVIDED, MSG_NO_PSW_PROVIDED
import re


class Registration(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('login', type=str, required=True, help=MSG_NO_LIGON_PROVIDED, location='json')
        self.reqparse.add_argument('password', type=str, required=True, help=MSG_NO_PSW_PROVIDED, location='json')
        super(Registration, self).__init__()

    def post(self):
        new_user = self.reqparse.parse_args()
        if not re.match("^[A-Za-z0-9_-]*$", new_user["login"]):
            return api_response_error(MSG_WRONG_LOGIN, 400)
        if self.add_new_user(new_user):
            return api_response_success(MSG_USER_REGISTERED, 201)
        else:
            return api_response_error(MSG_LOGIN_EXISTS, 400)

    @staticmethod
    def add_new_user(new_user):
        user, created = User.get_or_create(
            login=new_user["login"],
            defaults={
                'password': hash_password(new_user["password"])
            }
        )
        return created
