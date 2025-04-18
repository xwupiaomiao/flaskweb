#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =

from flask import Blueprint
from flask import render_template
from views import socketio
import paramiko

blue_oldwebssh = Blueprint('blue_oldwebssh', __name__, url_prefix='/oldwebssh')


@blue_oldwebssh.route("/")
def webssh():
    return render_template("oldwebssh.html")


# 出现消息后,率先执行此处
@socketio.on("message", namespace="/oldwebssh/ws")
def websshsocket(message):
    try:
        # hostname = message['hostname']
        # port = message['port']
        # username = message['username']
        # password = message['password']
        command = message['data']

        # 创建SSH客户端
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('192.168.140.130', port=22, username='root', password='123456')

        # 执行命令
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode() + stderr.read().decode()
        print(output)

        socketio.emit('command_response', {'data': output})

        client.close()
    except Exception as e:
        socketio.emit('command_response', {'data': str(e)})


# 当websocket连接成功时,自动触发connect默认方法
@socketio.on("connect", namespace="/oldwebssh/ws")
def connect():
    print("链接建立成功..")


# 当websocket连接失败时,自动触发disconnect默认方法
@socketio.on("disconnect", namespace="/oldwebssh/ws")
def disconnect():
    print("链接建立失败..")
