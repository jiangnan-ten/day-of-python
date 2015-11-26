# -*- coding: utf-8 -*-

from flask import flash

'''
表单错误收集  用于html显示
form 表单对象
label model类
'''


def error(form, label):
    for key in form.errors:
        for i in form.errors[key]:
            error_info = "%s : %s" % (label.zh[key], i)

    flash(error_info, 'error')
