#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =

from flask import Flask, request, session, redirect, render_template
from flask_socketio import SocketIO

# 创建 Flask 应用
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_pyfile("../settings.py")
socketio = SocketIO(app)


@app.before_request
def process_request(*args, **kwargs):
    reqpath = request.path
    if reqpath == '/' or reqpath == '/login' or '/static/' or '/chpwd' in reqpath:
        return None
    else:
        if session.get('user_info'):
            return None
        return redirect('/')


@app.after_request
def process_response(response):
    request.args.get('name')
    return response


@app.errorhandler(404)
def not_found(*args, **kwargs):
    return render_template('404-not-found.html')


from .websocket import blue_ws
from .alertpost import blue_alertpost
from .sse import blue_sse
from .alertws import blue_alertws
from .wschat import blue_chat
from .webssh import blue_webssh
from .base import blue_base

app.register_blueprint(blue_ws)
app.register_blueprint(blue_alertpost)
app.register_blueprint(blue_sse)
app.register_blueprint(blue_alertws)
app.register_blueprint(blue_chat)
app.register_blueprint(blue_webssh)
app.register_blueprint(blue_base)
