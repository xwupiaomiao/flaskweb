#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =
import os

SECRET_KEY = "lyshark"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 获取flaskrun文件的绝对路径
SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "site.db")}'  # 使用自定义目录
# SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"  # 使用相对目录时，数据库文件会保存在instance目录
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 禁用追踪修改，默认禁用

alertmsg = {
    '告警主机': '',
    '告警详情': '',
    '告警级别': '严重',
    '告警状态': '正在告警',
    '触发时间': ''
}

recovermsg = {
    '告警主机': '',
    '告警详情': '',
    '告警级别': '严重',
    '告警状态': '已经恢复',
    '触发时间': ''
}
