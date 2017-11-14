# -*- coding: utf-8 -*-
from config import db
from peewee import *
import datetime


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
    short_url = CharField()
    hash = CharField()
    author_id = IntegerField()
    count_of_redirects = IntegerField(default=0)
    created = DateTimeField(default=datetime.datetime.now)


class FollowUrl(BaseModel):
    id = PrimaryKeyField()
    link_id = IntegerField()
    referrer = CharField()
    datetime = DateTimeField(default=datetime.datetime.now)


db.create_tables([User, Url, FollowUrl], safe=True)



