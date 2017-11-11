from api.v1.Registration import Registration
from api.v1.CurrentUser import CurrentUser
from api.v1.Urls import Urls
from api.v1.Redirect import Redirect
from flask import Flask

from flask_restful import Api


app = Flask(__name__)
api = Api(app)

api.add_resource(Registration, '/api/v1/users', endpoint='Registration')
api.add_resource(CurrentUser, '/api/v1/users/me', endpoint='CurrentUser')
api.add_resource(Urls, '/api/v1/users/me/shorten_urls', endpoint='Urls')
api.add_resource(Redirect, '/api/v1/shorten_urls/<string:hash>', endpoint='Redirect')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
