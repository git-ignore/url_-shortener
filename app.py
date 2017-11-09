from api.v1.UsersAPI import UsersAPI
from flask import Flask

from flask_restful import Api


app = Flask(__name__)
api = Api(app)

api.add_resource(UsersAPI, '/api/v1/users', endpoint='users')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
