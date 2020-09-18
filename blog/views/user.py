
from flask import jsonify
from flask import request
from flask.views import MethodView
from flask import render_template
from blog.libs.db_api import UserTable

user_api = UserTable()

__all__ = [
    "Login", "Logout", "Register"
]

class Login(MethodView):

    def post(self):
        data = request.get_json()
        if not user_api.verify_user(data.get('username'), data.get('password')):
            return jsonify(
                {'code': 60204, 'message': 'Account and password are incorrect.'}
            )
        return jsonify({'code': 20000, 'data': {'token': "12312312312"}})

    def get(self):
        return render_template("login.html")

class Logout(MethodView):
    def post(self):
        pass

class Register(MethodView):
    def post(self):
        data = request.get_json()
        