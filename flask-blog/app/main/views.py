# -*- coding: utf-8 -*-

# 路由定义

from importlib import import_module
from . import main

'''
rule (string): 路由规则
endpoint (string): 方法名称
goto (string): controller文件夹下的文件前缀

'''


def url(rule, goto):
    module_name, func = goto.rsplit('.', )
    f = import_module('.controller.' + module_name, 'app.main')
    main.add_url_rule(rule, func, getattr(f, func))


# 首页
url('/', 'index.index')
