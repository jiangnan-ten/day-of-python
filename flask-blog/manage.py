# -*- coding: utf-8 -*-
#
from app import create_app

from flask.ext.script import Manager


app = create_app('office')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
