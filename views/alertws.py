#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =

from flask import Blueprint
from flask import jsonify, render_template
from .alertpost import wsques
from views import socketio

blue_alertws = Blueprint('blue_alertws', __name__, url_prefix='/alertws')


# 处理从队列中读取的数据并推送到所有 WebSocket客户端
def background_thread():
    while True:
        # 从队列中获取数据，阻塞直到有数据
        data = wsques.get()
        # 通过 WebSocket 发送数据，namespace的值和url_prefix无关
        socketio.emit('data_received', {'data': data}, namespace='/alertws/ws')
        # 信号队列任务完成
        wsques.task_done()


# 定义一个路由，用于处理 WebSocket 连接，向websocket客户端推送消息
@socketio.on('connect', namespace='/alertws/ws')
def ws_connect():
    return jsonify('success')


@blue_alertws.route('/', methods=['GET', 'POST'])
def sendws():
    return render_template("alertws.html")
