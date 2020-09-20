
import os
from blog.views.index import *
from blog.views.user import *
from blog.views.articles import *


def init_url(app):
    app.add_url_rule('/', view_func=Index.as_view('index'))
    app.add_url_rule('/user/login', view_func=Login.as_view('login'))
    app.add_url_rule('/user/register', view_func=Register.as_view('register'))
    app.add_url_rule('/articles/get_all_articles', view_func=AllArticles.as_view('get_all_articles'))