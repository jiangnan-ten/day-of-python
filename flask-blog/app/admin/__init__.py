# -*- coding: utf-8 -*-

# 蓝本初始化

from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views, errors, forms, models
