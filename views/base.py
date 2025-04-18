#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =

from flask import request, session, redirect, render_template
from flask import Blueprint
from views import app
from views.models import Userinfo

blue_base = Blueprint('blue_base', __name__, url_prefix='/')


@blue_base.route('/', methods=['GET', 'POST'])
def index():
    # 创建用户
    # new_user = Userinfo(username='alix', email='alix@example.com')
    # db.session.add(new_user)
    # db.session.commit()
    # 查询用户
    # user = Userinfo.query.filter_by(username='john').first()
    # print(user.username)
    # print(user.email)
    # 删除用户
    # db.session.delete(user)
    # db.session.commit()
    app.logger.info('访问首页')
    return render_template("index.html")


@blue_base.route('/login', methods=['GET', 'POST'])
def login():
    # 创建用户
    # new_user = Userinfo(username='alix', email='alix@example.com')
    # db.session.add(new_user)
    # db.session.commit()
    # 查询用户
    # user = Userinfo.query.filter_by(username='john').first()
    # print(user.username)
    # print(user.email)
    # 删除用户
    # db.session.delete(user)
    # db.session.commit()
    return render_template("login.html")
