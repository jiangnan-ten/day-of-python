# -*- coding: utf-8 -*-
from flask import render_template

# 后台首页


def index():
    return render_template('admin/index/index.html')
