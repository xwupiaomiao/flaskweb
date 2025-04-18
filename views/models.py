#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =
# 数据库初始化错误解决方法：https://www.cnblogs.com/skyvip/p/18164878
# 不建议使用db = SQLAlchemy(app)初始化数据库

from views import app
from flask_sqlalchemy import SQLAlchemy
import os

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 获取flaskrun文件的绝对路径
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "site.db")}'  # 使用自定义目录
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # 使用相对目录数据库文件会保存在instance目录
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用追踪修改


db = SQLAlchemy()


class Userinfo(db.Model):
    # 指定表名，没有就用类名做表名
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"repr方法_User('{self.username}', '{self.email}')"


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()  # 创建数据库表
