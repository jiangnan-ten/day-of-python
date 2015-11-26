# -*- coding: utf-8 -*-

from wtforms import Form, TextField, validators, TextAreaField

# 标签form


class labelForm(Form):
    label_name = TextField(
        'label_name',
        [
            validators.Length(max=20),
            validators.Required(),
        ]
    )

    description = TextAreaField('description', [validators.Length(max=50)])
