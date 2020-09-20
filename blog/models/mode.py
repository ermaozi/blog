from blog.models.exts import db
from blog.models.exts import bcrypt

import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.INTEGER, primary_key=True)
    domainname = db.Column(db.String(80), default="")
    name = db.Column(db.String(80), unique=True)
    _password_hash_ = db.Column(db.String(256))
    email = db.Column(db.String(80), default="")
    profile_photo = db.Column(db.String(200), default="")
    registration_time = db.Column(db.DateTime, default=datetime.datetime.now())
    birthday = db.Column(db.DateTime, default=datetime.datetime.now())
    telephone = db.Column(db.String(80), default="")
    nickname = db.Column(db.String(80), nullable=False)

    @property
    def password(self):
        raise Exception('密码不能被读取')
    # 赋值password，则自动加密存储。
    @password.setter
    def password(self, value):
        self._password_hash_ = bcrypt.generate_password_hash(value)
        
    # 使用check_password,进行密码校验，返回True False。
    def check_password(self, pasword):
        return bcrypt.check_password_hash(self._password_hash_, pasword)

class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    title = db.Column(db.String(80))
    author = db.Column(db.String(80))
    summary = db.Column(db.String(300))
    content = db.Column(db.String(5000), unique=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    article_read = db.Column(db.INTEGER, default=0)
    comment_count = db.Column(db.INTEGER, default=0)
    thumb_up = db.Column(db.INTEGER, default=0)



