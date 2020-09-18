
from flask import request, jsonify, render_template
from flask.views import MethodView
from blog.libs.db_api import UserTable
from blog.libs.auth_api import create_token


user_api = UserTable()

__all__ = [
    "Login", "Logout", "Register"
]


class Login(MethodView):

    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        check_result, user_id = user_api.verify_user(username, password)

        if not check_result:
            return jsonify({
                    'code': 60204, 
                    'message': 'Account and password are incorrect.'
                })
        return jsonify({
                'code': 200, 
                'data': {'token': create_token({"user_id": user_id})}
            })

    def get(self):
        return render_template("login.html")

class Logout(MethodView):
    def post(self):
        pass

class Register(MethodView):
    def post(self):
        data = request.get_json()
        try:
            user_data = data
            user_api.add_user(**user_data)
        except:
            return jsonify({
                'code': 500,
                'message': ""
            })