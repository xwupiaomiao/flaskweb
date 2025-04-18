#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =
# pip install func-timeout


from flask import Blueprint, render_template, request
from views import socketio
import re
import time
from paramiko import SSHClient, AutoAddPolicy
from func_timeout import func_set_timeout, exceptions

blue_webssh = Blueprint('blue_webssh', __name__, url_prefix='/webssh')
clients = {}


class RemoteCMD():
    """执行远程命令
    """

    def __init__(self, ip, port, user, passwd, timeout=5):
        self.ip = ip
        self.port = port
        self.user = user
        self.pwd = passwd
        self.timeout = timeout
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            self.client.connect(hostname=self.ip,
                                port=int(self.port),
                                username=self.user,
                                password=self.pwd,
                                timeout=self.timeout,
                                allow_agent=False,
                                look_for_keys=False)

            self.client = self.client.invoke_shell()
        except Exception as err:  # pylint: disable=broad-except
            self.client.close()
            print(f"SSH 连接出现异常：{err}")

    def _match_prompt(self, content: str, regex: str):
        if re.search(regex, content):
            return True
        return False

    @func_set_timeout(5)
    def _send_cmd(self,
                  cmd: str,
                  recv_end_prompt: str,
                  recv_size: int = 512):
        self.client.send(f"{str(cmd).strip()}\n")
        # 等待就绪
        while not self.client.recv_ready():
            time.sleep(0.2)

        result = ""
        while not self._match_prompt(result, recv_end_prompt):
            result += self.client.recv(recv_size).decode()
        return result

    def command(self,
                cmd: str,
                end_prompt: str = r"#\s$"):
        try:
            return self._send_cmd(cmd, end_prompt)
        except exceptions.FunctionTimedOut:
            self.client.close()
            return "SSH 执行出现超时错误！"
        except Exception as err:  # pylint: disable=broad-except
            self.client.close()
            return f"SSH 执行出现其他异常：{err}"

    def close(self):
        self.client.close()


@blue_webssh.route('/')
def websshindex():
    return render_template('webssh.html')


@socketio.on('connect', namespace="/webssh/ws")
def handle_connect():
    print('Client connected')


@socketio.on('disconnect', namespace="/webssh/ws")
def handle_disconnect():
    print('Client disconnected')
    # 清理会话
    session = clients.pop(request.sid, None)
    if session:
        session.close()


@socketio.on('set_session', namespace="/webssh/ws")
def set_session(data):
    hostname = data['hostname']
    port = data.get('port', 22)
    username = data['username']
    password = data['password']

    session = RemoteCMD(hostname, port, username, password)
    clients[request.sid] = session
    if session:
        socketio.emit('output', {'data': 'success'}, room=request.sid, namespace="/webssh/ws")
        print(f"连接信息: {hostname}:{port} 用户名: {username}")


@socketio.on('send_data', namespace="/webssh/ws")
def handle_send_data(data):
    session = clients.get(request.sid)
    if session:
        if data.get('data'):
            sshdata = session.command(data.get('data'))
            socketio.emit('output', {'data': sshdata}, room=request.sid, namespace="/webssh/ws")
    else:
        socketio.emit('output', {'data': '未找到会话，请先连接。'}, room=request.sid, namespace="/webssh/ws")


@socketio.on('close_session', namespace="/webssh/ws")
def close_session():
    session = clients.pop(request.sid, None)
    if session:
        session.close()
