
from flask import request, jsonify, render_template
from flask.views import MethodView
from blog.libs.db_api import UserTable
from blog.libs.auth_api import create_token
import json


user_api = UserTable()

__all__ = [
    "Login", "Logout", "Register"
]


class Login(MethodView):

    def post(self):
        data = request.get_data()
        data = json.loads(data.decode("UTF-8"))
        elmail = data.get('email')
        password = data.get('password')

        check_result, user_id = user_api.verify_user(elmail, password)

        if check_result:
            ret = {
                    'code': 200, 
                    'data': {
                        'token': create_token({"user_id": user_id}),
                        'user_id': user_id
                    }
                }
        else:
            ret = {
                    'code': 401, 
                    'message': 'Account and password are incorrect.'
                }
        return jsonify(ret)

    def get(self):
        return render_template("login.html")

class Logout(MethodView):
    def post(self):
        pass

class Register(MethodView):
    def post(self):
        data = request.get_data()
        data = json.loads(data.decode("UTF-8"))
        try:
            email = data.get("email")
            if user_api.email_if_exist(email):
                raise Exception("邮箱已存在")
            user_data = data
            user_api.add_user(**user_data)
            return jsonify({
                'code': 200,
                'data': {}
            })
        except Exception as err:
            return jsonify({
                'code': 500,
                'message': str(err)
            })