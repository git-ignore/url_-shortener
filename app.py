import os

from flask import Flask, jsonify


app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


user = {
    'id': 1,
    'login': 'admin',
    'password': 1234
}


@app.route('/api/v1/users/me', methods=['GET'])
def get_curr_user_info():
    return jsonify(user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
