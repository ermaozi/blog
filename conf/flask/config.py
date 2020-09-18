from conf.flask.private.private import *


class ProductionConfig(PriProduction):
    DEBUG = False
    MAIL_DEBUG = False

class DevelopmentConfig(PriDevelopment):
    DEBUG = True
    MAIL_DEBUG = True

class TestingConfig(PriTesting):
    DEBUG = True
    TESTING = True
    MAIL_DEBUG = True