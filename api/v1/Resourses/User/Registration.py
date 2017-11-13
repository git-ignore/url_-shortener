from flask_restful import Resource, reqparse
from api.v1.models import User
from api.v1.auth import hash_password
from api.v1.helpers import error_message, success_message


class Registration(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('login', type=str, required=True, help='No login provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided', location='json')
        super(Registration, self).__init__()

    def post(self):
        new_user = self.reqparse.parse_args()
        if self.add_new_user(new_user):
            return success_message("User successfully registered", 201, False)
        else:
            return error_message("User with this login already exists", 400)

    @staticmethod
    def add_new_user(new_user):
        user, created = User.get_or_create(
            login=new_user["login"],
            defaults={
                'password': hash_password(new_user["password"])
            }
        )
        return created
