# -*- coding: utf-8 -*-
import sys
from flask import render_template, request, flash, url_for, redirect, jsonify
from ..forms import labelForm
from ...helper import error

reload(sys)
sys.setdefaultencoding("utf-8")


# 管理页  分类 标签 评论 等


def label():
    form = labelForm(request.form)
    from ..models import label as label_m

    if request.method == 'POST':
        if form.validate():
            label_name = request.form['label_name']
            description = request.form['description']

            if not label_m.query.filter_by(label_name=label_name).first():
                label_model = label_m(label_name, description)
                label_model.insert()

                flash(u'添加成功', 'success')
                return redirect(url_for('admin.manage/label'))
            else:
                flash(u'标签名不能重复', 'error')
        else:
            error(form, label_m)

    label_data = label_m.query.all()

    return render_template('admin/manage/label.html', form=form, label_data=label_data)


def changelabelname(label_id):
    name = request.values['change_label_name']
    if request.method == 'POST' and 0 < len(name) < 20:
        from ..models import label as label_m
        if not label_m.query.filter_by(label_name=name).filter(label_m.label_id != label_id).first():
            label_m.query.filter_by(label_id=label_id).update({'label_name': name})
            flash(u'更新成功', 'success')
            return jsonify(res=True)
        else:
            return jsonify(res=False)
    else:
        return jsonify(res=False)
