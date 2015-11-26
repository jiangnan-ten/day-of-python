# -*- coding: utf-8 -*-

# 第三方类导入, 初始化

from flask import Flask
from config import configdic
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

moment = Moment()
csrf = CsrfProtect()
db = SQLAlchemy()


def create_app(config_name):

    # flask创建实例
    app = Flask(__name__)

    # 根据配置类初始化
    app.config.from_object(configdic[config_name])

    # 初始化
    configdic[config_name].init_app(app)

    # 数据库初始化
    # global db
    # app.config['SQLALCHEMY_DATABASE_URI'] = configdic[config_name].connection
    # db = SQLAlchemy(app)
    db.init_app(app)

    # 时间库初始化
    moment.init_app(app)

    # main蓝本注册
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # admin蓝本注册
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # csrf初始化
    csrf.init_app(app)

    return app
