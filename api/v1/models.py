# -*- coding: utf-8 -*-
import os

from peewee import *
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE') or 'postgresql://user:password@db:5432/url_shortener_db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = PrimaryKeyField()
    login = CharField()
    password = CharField()


class Url(BaseModel):
    id = PrimaryKeyField()
    url = CharField()
    hash = CharField()
    author_id = IntegerField()


db.create_tables([User, Url], safe=True)



