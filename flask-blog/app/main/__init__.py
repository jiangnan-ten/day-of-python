# -*- coding: utf-8 -*-

# 蓝本初始化

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors, forms
