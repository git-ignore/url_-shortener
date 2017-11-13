from flask_httpauth import HTTPBasicAuth
from api.v1.models import User
import hashlib


auth = HTTPBasicAuth()


def hash_password(psw):
    return hashlib.md5(psw.encode("utf")).hexdigest()


@auth.get_password
def get_password(login):
    try:
        user = User.get(User.login == login)
        return user.password
    except User.DoesNotExist:
        return None


@auth.hash_password
def hash_pw(password):
    return hash_password(password)



