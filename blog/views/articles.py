from datetime import datetime

from flask import request, jsonify, render_template
from flask.views import MethodView
from blog.libs.db_api import ArticlesTable, UserTable


articles_aip = ArticlesTable()
user_api = UserTable()

class AllArticles(MethodView):
    def get(self):
        data_list = articles_aip.get_articles_all_mininfo()
        ret_list = []
        for data in data_list:
            data["create_time"] = datetime.strftime(data["create_time"], "%Y-%m-%d %H:%M:%S")
            ret_list.append(data)

        return jsonify({
            'code': 200, 
            'data': ret_list
        })

class ArticlesForID(MethodView):
    def get(self):
        id = int(request.args.get("id"))
        all_id_list = articles_aip.get_articles_all_id()
        id_index = all_id_list.index(id)
        pre_name = "这是第一篇"
        pre_route = "javascript:;"
        next_name = "后面竟然没有了"
        next_route = "javascript:;"
        if id_index == len(all_id_list) - 1:
            pre_id = all_id_list[id_index - 1]
            pre_data = articles_aip.get_articles_info_for_id(pre_id)
            pre_name = pre_data["title"]
            pre_route = pre_id
        elif id_index == 0:
            next_id = all_id_list[id_index + 1]
            next_data = articles_aip.get_articles_info_for_id(next_id)
            next_name = next_data["title"]
            next_route = next_id
        else:
            pre_id = all_id_list[id_index - 1]
            pre_data = articles_aip.get_articles_info_for_id(pre_id)
            pre_name = pre_data["title"]
            pre_route = pre_id
            next_id = all_id_list[id_index + 1]
            next_data = articles_aip.get_articles_info_for_id(next_id)
            next_name = next_data["title"]
            next_route = next_id
        
        article_next_pre_data = [{
                'type': 'pre',
                'name': pre_name,
                'route': pre_route
            }, {
                'type': 'next',
                'name': next_name,
                'route': next_route
            }]


        data = articles_aip.get_articles_info_for_id(id)
        user_info = user_api.get_user_info_for_id(data.get("user_id"))
        data["user_data"] = {
            "nickname": user_info.get("nickname"),
            "email": user_info.get("email")
        }
        data["article_next_pre_data"] = article_next_pre_data
        return jsonify({
            'code': 200, 
            'data': data
        })