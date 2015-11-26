# -*- coding: utf-8 -*-

from .. import db


class label(db.Model):
    __tablename = 'label',
    label_id = db.Column(db.Integer, primary_key=True)
    label_name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(50))

    # 中文字段名
    zh = {
        'label_name': u'标签名',
        'description': u'标签描述'
    }

    def __init__(self, label_name, description):
        self.label_name = label_name
        self.description = description

    def insert(self):
        db.session.add(self)
