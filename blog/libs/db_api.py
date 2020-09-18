from blog.models.mode import *
from blog.models.modetool import Database


class UserTable(object):

    def __init__(self) -> None:
        self.db = Database(User)

    def add_user(self, name, password, email, domainname="", profile_photo="",
                 birthday="", telephone="", nickname=""):
        db_data = {
            "domainname": domainname,
            "name": name,
            "password": password,
            "email": email,
            "profile_photo": profile_photo,
            "birthday": birthday,
            "telephone": telephone,
            "nickname": nickname
        }
        self.db.insert(db_data)
    
    def verify_user(self, name, password):
        usr = db.session.query(User).filter_by(name=name).first()
        if usr:
            return usr.check_password(password), usr.id
        return False, -1


class ArticlesTable(object):

    def __init__(self) -> None:
        self.db = Database(Articles)

    def add_articles(self, user_id, title, cover, content):
        """
        新增文章
        """

        db_data = {
            "user_id": user_id,
            "title": title,
            "cover": cover,
            "content": content
        }
        self.db.insert(db_data)

    def get_articles_all_id(self):
        """
        查询所有文章 id
        """

        return [i.get("id") for i in self.db.select(result=["id"])]

    def get_articles_all_mininfo(self):
        """
        查询所有文章的精简信息(id, user_id, title, cover, create_time, 
                            views, comment_count, like_count)
        """
        return self.db.select(result=["id", "user_id", "title", "cover", "create_time",
                                   "views", "comment_count", "like_count"])

    def get_articles_info_for_id(self, articles_id):
        """
        通过文章 id 查询所有内容
        """
        return self.db.select(condition={"id": articles_id})