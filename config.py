import os
from playhouse.db_url import connect

# DB config
DB_PASSWORD = 'password'
DB_USER = 'user'
DB_NAME = 'url_shortener_db'
POSTGRE_PORT = '5432'


db = connect(
    os.environ.get('DATABASE') or
    'postgresql://%s:%s@db:%s/%s' % (DB_USER, DB_PASSWORD, POSTGRE_PORT, DB_NAME)
)

# API response messages
MSG_USER_REGISTERED = "User successfully registered"
MSG_LOGIN_EXISTS = "User with this login already exists"
MSG_WRONG_LOGIN = "Login is wrong"


# Other config
WRONG_RESPONSE_CODES = [400, 403, 404, 502, 503, 504]
INCLUDE_NONE_REFERRER_IN_REF_REPORT = True
