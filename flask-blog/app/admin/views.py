# -*- coding: utf-8 -*-

# admin 路由定义
from importlib import import_module
from . import admin


'''
rule (string): 路由规则
endpoint (string): 方法名称
goto (string): controller文件夹下的文件前缀

endpoint 为模块名/方法名
'''


def url(rule, goto, methods=['get']):
    module_name, func = goto.rsplit('.', )
    f = import_module('.controller.' + module_name, 'app.admin')
    admin.add_url_rule(rule, module_name + '/' + func,
                       getattr(f, func), methods=methods)


# 首页
url('/', 'index.index')

# 发表文章页
url('/write', 'write.index')

# 标签
url('/label', 'manage.label', methods=['GET', 'POST'])

# 修改标签名
url('/changelabelname/<int:label_id>', 'manage.changelabelname', methods=["POST"])
