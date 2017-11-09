from flask_restful import Resource, reqparse
from api.v1.helpers import select_all, b64_encode
from api.v1.models import User
from api.v1.Auth import auth


class UsersAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('login', type=str, required=True, help='No login provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided', location='json')
        super(UsersAPI, self).__init__()

    def post(self):
        new_user = self.reqparse.parse_args()
        return self.add_new_user(new_user), 201

    @auth.login_required
    def get(self):
        return self.get_all_users()

    def add_new_user(self, new_user):
        user, created = User.get_or_create(
            login=b64_encode(new_user["login"]),
            defaults={'password': b64_encode(new_user["password"])}
        )
        return created

    def get_all_users(self):
        return select_all(User)


