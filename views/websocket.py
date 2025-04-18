#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =


from flask import Blueprint
from flask import render_template
from flask import request
from views import socketio
import subprocess

blue_ws = Blueprint('blue_ws', __name__, url_prefix='/websocket')


# 定义一个路由，用于处理 WebSocket 连接，可以发送和接收消息
# @blue_ws.route('/ws')
# def websocket():
#     if request.environ.get('wsgi.websocket'):  # 检查是否为 WebSocket 请求
#         ws = request.environ['wsgi.websocket']  # 获取 WebSocket 对象
#         while True:
#             message = ws.receive()  # 接收客户端发送的消息
#             if message is None:  # 如果客户端断开连接
#                 break
#             print(f"Received: {message}")
#             ws.send(f"{message}")  # 将消息回显给客户端

# @blue_ws.route('/', methods=['POST', 'GET'])
# def websockethtml():
#     return render_template("websocket.html", serverip=serverip)


@socketio.on('message', namespace='/websocket/ws')
def websocket(msg):
    print(f"Received message: {msg} {request.sid} {request.args.get('username')}")
    if msg:
        process = subprocess.Popen(
            msg,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # text=True  # 默认使用系统编码,使得输入/输出以字符串形式处理（Python 3.7 及以后的版本可以使用，之前的版本应该使用 universal_newlines=True
        )
        # 逐行读取输出，直接向前端发送二进制数据
        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                socketio.emit('response', output, namespace='/websocket/ws')
        # 逐行读取输出，直接向前端发送二进制数据
        while True:
            outputerr = process.stderr.readline()
            if outputerr == b'' and process.poll() is not None:
                break
            if outputerr:
                socketio.emit('response', outputerr, namespace='/websocket/ws')
        # 检查命令返回状态码
        return_code = process.poll()
        if return_code != 0:
            print(f"命令执行失败，返回码：{return_code}")
        socketio.emit('response', {'data': 'success'}, namespace='/websocket/ws')


@blue_ws.route('/', methods=['POST', 'GET'])
def websockethtml():
    return render_template("websocket.html")
