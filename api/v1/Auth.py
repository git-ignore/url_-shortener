from flask_httpauth import HTTPTokenAuth
from api.v1.models import User

auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token):
    return token == '111'

# @auth.get_password
# def get_password(login):
#     try:
#         user = User.get(User.login == login)
#         return user.password
#     except():
#         return None