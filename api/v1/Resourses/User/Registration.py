from flask_restful import Resource, reqparse
from api.v1.models import User
from api.v1.auth import hash_password


class Registration(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('login', type=str, required=True, help='No login provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided', location='json')
        super(Registration, self).__init__()

    def post(self):
        new_user = self.reqparse.parse_args()
        return self.add_new_user(new_user), 201

    @staticmethod
    def add_new_user(new_user):
        user, created = User.get_or_create(
            login=new_user["login"],
            defaults={
                'password': hash_password(new_user["password"])
            }
        )
        return created
    # TODO: Если таблицы не существует!
