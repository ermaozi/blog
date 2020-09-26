from flask import current_app, request, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


#在上面的基础上导入
import functools

def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        try:
            #在请求头上拿到token
            token = request.headers["Authorization"]
        except Exception:
            #没接收的到token,给前端抛出错误
            return jsonify(code = 4103,msg = '缺少参数token')
        
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            s.loads(token)
        except Exception:
            return jsonify(code = 401,msg = "登录已过期")

        return view_func(*args,**kwargs)

    return verify_token


def create_token(data):
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600)
    token = s.dumps(data).decode("ascii")
    return token

def verify_token(token):
    #参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        #转换为字典
        data = s.loads(token)
    except Exception:
        return None
    return data