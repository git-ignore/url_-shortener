from api.v1.models import *



def select_all(model):
    result = []
    for row in model.select().execute():
        result.append(model_to_dict(row))
    return result


def get_users():
    return select_all(User)


def add_new_user(new_user):
    user, created = User.get_or_create(login=new_user["login"], defaults={'password': new_user["password"]})
    return created


class DB(Model):

    def select_all(self):
        result = []
        for row in self.select().execute():
            result.append(model_to_dict(row))
        return result


    def add_new_user(self, new_user):
        user, created = User.get_or_create(login=new_user["login"], defaults={'password': new_user["password"]})
        return created
