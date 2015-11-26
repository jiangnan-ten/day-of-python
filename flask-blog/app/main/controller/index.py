# -*- coding: utf-8 -*-
from flask import request, render_template, flash, url_for, redirect


def index():
    return render_template('index/index.html')
