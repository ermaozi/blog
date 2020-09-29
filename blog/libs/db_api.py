from blog.models.mode import *
from blog.models.modetool import Database


class UserTable(object):

    def __init__(self) -> None:
        self.db = Database(User)

    def add_user(self, email, password, domainname="", profile_photo="",
                 birthday="", telephone="", nickname=""):
        db_data = {
            "email": email,
            "password": password,
            "domainname": domainname,
            "profile_photo": profile_photo,
            "birthday": birthday,
            "telephone": telephone,
            "nickname": nickname
        }
        if not birthday:
            del db_data["birthday"]
        self.db.insert(db_data)
    
    def verify_user(self, email, password):
        usr = db.session.query(User).filter_by(email=email).first()
        if usr:
            return usr.check_password(password), usr.id
        return False, -1

    def get_user_info_for_id(self, id):
        return self.db.select({"id": id})[0]

    def email_if_exist(self, email):
        return bool(self.db.select({"email": email}, ["id"]))


class ArticlesTable(object):

    def __init__(self) -> None:
        self.db = Database(Articles)

    def add_articles(self, user_id, title, content, summary):
        """
        新增文章
        """
        db_data = {
            "user_id": user_id,
            "title": title,
            "content": content,
            "summary": summary
        }
        self.db.insert(db_data)

    def del_articles(self, id):
        self.db.delete({"id": id})

    def get_articles_user_id(self, id):
        return self.db.select(condition={"id": id}, result=["user_id"])

    def get_articles_all_id(self):
        """
        查询所有文章 id
        """
        id_list = self.db.select(result=["id"])
        return [i.get("id") for i in id_list]

    def get_articles_all_mininfo(self):
        """
        查询所有文章的精简信息(id, user_id, title, author, create_time, 
                            article_read, comment_count, thumb_up, summary)
        """
        return self.db.select(result=["id", "user_id", "title", "author", "create_time",
                                      "article_read", "comment_count", "thumb_up", "summary"])

    def get_articles_mininfo_for_id(self, id_list: list):
        """
        根据 id 列表查询所有文章的精简信息(id, user_id, title, author, create_time, 
                                      article_read, comment_count, thumb_up, summary)
        """
        result = ["id", "user_id", "title", "author", "create_time",
                                             "article_read", "comment_count", "thumb_up", "summary"]
        mininfo_list = []
        for id in id_list:
            mininfo = self.db.select({"id": id}, result)[0]
            mininfo_list.append(mininfo)
        return mininfo_list

    def get_articles_info_for_id(self, articles_id):
        """
        通过文章 id 查询所有内容
        """
        return self.db.select(condition={"id": articles_id})[0]

    def title_if_exist(self, title):
        return bool(self.db.select({"title": title}, ["id"]))