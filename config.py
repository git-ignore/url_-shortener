import os
from playhouse.db_url import connect

DB_PASSWORD = 'password'
DB_USER = 'user'
DB_NAME = 'url_shortener_db'
POSTGRE_PORT = '5432'


db = connect(
    os.environ.get('DATABASE') or
    'postgresql://%s:%s@db:%s/%s' % (DB_USER, DB_PASSWORD, POSTGRE_PORT, DB_NAME)
)

