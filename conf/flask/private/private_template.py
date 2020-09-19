

"""
    警告: 
        本文件内所有内容均属于敏感信息
        切勿将本文件以及本文件所在目录下的任何内容暴露在公开环境
        如果不慎泄露, 请立即停止服务, 并修改相关内容以避免损失
"""

__all__ = [
    "PriProduction",
    "PriDevelopment",
    "PriTesting"
]

class Base(object):
    SECRET_KEY = ''  # 密钥, Flask 部分请求需要用到该密钥

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER= 'smtp.exmail.qq.com'  # 邮箱服务器
    MAIL_PROT= 465  # 邮箱端口
    MAIL_USE_SSL = True  # 是否需要 SSL 加密
    MAIL_USERNAME = "admin@ermao.net"  # 邮箱账户
    MAIL_PASSWORD = ""  # 邮箱密码或授权码



class PriProduction(Base):
    DIALECT = 'mysql'  # 数据库语法, 本项目使用 mariadb, 属于 mysql 语法
    DRIVER = 'pymysql'  # 数据库链接工具, 本项目使用 pymysql
    USERNAME = 'root'  # 数据库用户名, 默认 root
    PASSWORD = ''  # 你的数据库密码
    HOST = '127.0.0.1'  # 数据库地址, 默认 127.0.0.1, 若使用其他服务器, 请填写该服务器的公网 ip
    PORT = '3306'  # 数据库端口, 默认 3306
    DATABASE = 'blog'  # 数据库名称

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )


class PriDevelopment(Base):
    DIALECT = 'mysql'  # 数据库语法, 本项目使用 mariadb, 属于 mysql 语法
    DRIVER = 'pymysql'  # 数据库链接工具, 本项目使用 pymysql
    USERNAME = 'root'  # 数据库用户名, 默认 root
    PASSWORD = ''  # 你的数据库密码
    HOST = '127.0.0.1'  # 数据库地址, 默认 127.0.0.1, 若使用其他服务器, 请填写该服务器的公网 ip
    PORT = '3306'  # 数据库端口, 默认 3306
    DATABASE = 'test_blog'  # 数据库名称

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )


class PriTesting(Base):
    DIALECT = 'mysql'  # 数据库语法, 本项目使用 mariadb, 属于 mysql 语法
    DRIVER = 'pymysql'  # 数据库链接工具, 本项目使用 pymysql
    USERNAME = 'root'  # 数据库用户名, 默认 root
    PASSWORD = ''  # 你的数据库密码
    HOST = '127.0.0.1'  # 数据库地址, 默认 127.0.0.1, 若使用其他服务器, 请填写该服务器的公网 ip
    PORT = '3306'  # 数据库端口, 默认 3306
    DATABASE = 'test_blog'  # 数据库名称

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )

