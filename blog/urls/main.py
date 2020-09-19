
import os
from blog.views.index import *
from blog.views.user import *


def init_url(app):
    app.add_url_rule('/', view_func=Index.as_view('index'))
    app.add_url_rule('/user/login', view_func=Login.as_view('login'))
    app.add_url_rule('/user/register', view_func=Register.as_view('register'))