# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for
# 发表文章页


def index():
    return render_template('admin/write/index.html')
