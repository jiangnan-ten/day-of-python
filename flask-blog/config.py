# -*- coding: utf-8 -*-

# 配置类


class config():

    SECRET_KEY = 'ten love jj'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class localConf(config):

    SQLALCHEMY_DATABASE_URI = 'mysql://root:111@127.0.0.1/blog'


class officeConf(config):

    SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1/blog'


configdic = {
    'home': localConf,
    'office': officeConf
}
