from flask import request, jsonify, render_template
from flask.views import MethodView
from blog.libs.db_api import ArticlesTable


articles_aip = ArticlesTable()

class AllArticles(MethodView):
    def get(self):
        data = articles_aip.get_articles_all_mininfo()
        return jsonify({
            'code': 200, 
            'data': data
        })