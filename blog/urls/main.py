
import os
from blog.views.index import *
from blog.views.user import *
from blog.views.articles import *


def init_url(app):
    app.add_url_rule('/', view_func=Index.as_view('index'))
    app.add_url_rule('/user/login', view_func=Login.as_view('login'))
    app.add_url_rule('/user/register', view_func=Register.as_view('register'))
    
    app.add_url_rule('/articles/get_all_articles', view_func=AllArticles.as_view('get_all_articles'))
    app.add_url_rule('/articles/get_article_for_id', view_func=ArticlesForID.as_view('get_article_for_id'))
    app.add_url_rule('/articles/add_article', view_func=AddArticle.as_view('add_article'))
    app.add_url_rule('/articles/del_article', view_func=DelArticle.as_view('del_article'))