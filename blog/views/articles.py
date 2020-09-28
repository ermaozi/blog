import json

from flask import request, jsonify
from flask.views import MethodView
from blog.libs.db_api import ArticlesTable, UserTable
from blog.libs.auth_api import login_required


articles_aip = ArticlesTable()
user_api = UserTable()

class AllArticles(MethodView):
    def get(self):
        articles_aip = ArticlesTable()
        user_api = UserTable()
        current_page = int(request.args.get("current_page"))  # 当前页
        all_id_list = articles_aip.get_articles_all_id()[::-1]
        max_pages = 6
        all_id_list = [all_id_list[i:i+max_pages] for i in range(0,len(all_id_list),max_pages)]  # 分页
        pages_num = len(all_id_list)  # 总共页
        data_list = articles_aip.get_articles_mininfo_for_id(all_id_list[current_page - 1])
        ret_list = []
        for data in data_list:
            user_info = user_api.get_user_info_for_id(data.get("user_id"))
            data["icon"] = 'mdi-fountain-pen-tip'
            data["author"] = user_info.get("nickname")
            ret_list.append(data)

        return jsonify({
            'code': 200, 
            'data': {
                "articles": ret_list,
                "pages_num": pages_num
            }
        })

class ArticlesForID(MethodView):
    def get(self):
        articles_aip = ArticlesTable()
        user_api = UserTable()
        id = int(request.args.get("id"))
        all_id_list = articles_aip.get_articles_all_id()

        id_index = all_id_list.index(id) - 1

        pre_name = "这是第一篇"
        pre_route = "javascript:;"
        next_name = "后面竟然没有了"
        next_route = "javascript:;"
        
        pre_id = all_id_list[id_index - 1]
        next_id = all_id_list[id_index + 1]
        pre_data = articles_aip.get_articles_info_for_id(pre_id)
        next_data = articles_aip.get_articles_info_for_id(next_id)

        if pre_data:
            pre_name = pre_data["title"]
            pre_route = pre_id
        if next_data:
            next_name = next_data["title"]
            next_route = next_id
        
        article_next_pre_data = [{
                'type': 'pre',
                'name': pre_name,
                'id': pre_route
            }, {
                'type': 'next',
                'name': next_name,
                'id': next_route
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

class AddArticle(MethodView):
    @login_required
    def post(self):
        articles_aip = ArticlesTable()
        data = request.get_data()
        data = json.loads(data.decode("UTF-8"))
        try:
            title = data.get("title")
            if articles_aip.title_if_exist(title):
                raise Exception(f"标题: {title} 已存在")
            articles_aip.add_articles(**data)
        except Exception as err:
            return jsonify({
                'code': 500,
                'message': str(err)
            })
        return jsonify({
            'code': 200
        })