#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =


from flask_socketio import emit, join_room, leave_room
from flask import Blueprint, request
from views import socketio
from flask import render_template
import logging

blue_chat = Blueprint('blue_chat', __name__, url_prefix='/chat')


# 处理客户端连接
@socketio.on('connect', namespace='/allws')
def handle_connect():
    print('A client connected')


# 处理消息并广播给其他客户端
@socketio.on('message', namespace='/allws')
def handle_message(msg):
    print(f'Received message: {msg}')
    # 广播消息给所有其他客户端
    emit('message', msg, broadcast=True, include_self=False, namespace='/allws')


# 处理客户端断开连接
@socketio.on('disconnect', namespace='/allws')
def handle_disconnect():
    print('A client disconnected')


@blue_chat.route('/allws')
def allws():
    return render_template('allws.html')


# 以下代码为websocket一对一聊天代码
# 存储用户与房间的映射
user_rooms = {}
# 存储连接的用户信息
users = {}


@blue_chat.route('/onews')
def index():
    return render_template('onews.html')


# 用户连接时
@socketio.on('connect', namespace='/onews')
def handle_connect():
    username = request.args.get('username')  # 获取前端通过 query 参数传递用户名
    users[request.sid] = username  # 将用户名与当前的 session ID 关联
    logging.info('A client connected: %s', request.sid)


# 用户发送消息时
@socketio.on('send_message', namespace='/onews')
def handle_send_message(data):
    recipient_id = data['recipient_id']  # 接收者的 ID
    message = {}  # 消息内容
    message['msg'] = data['message']
    message['user'] = data['sendusername']
    # 向指定用户发送消息
    emit('receive_message', {'message': message}, room=user_rooms.get(recipient_id))


# 加入房间
@socketio.on('join', namespace='/onews')
def on_join(data):
    username = data['username']
    room = data['room']
    user_rooms[username] = room  # 保存用户与房间的映射
    join_room(room)
    print(f"{username} has joined room {room}")


# 用户离开房间时
@socketio.on('leave', namespace='/onews')
def on_leave(data):
    username = data['username']
    room = user_rooms.get(username)  # 获取用户的房间
    if room:
        leave_room(room)  # 离开房间
        print(f"{username} has leave room {room}")

    # 可选：在用户离开时，可以广播消息给房间中的其他用户
    # socketio.emit('user_leave', {'username': username}, room=room)

    # 从用户房间字典中移除用户
    if username in user_rooms:
        del user_rooms[username]


# 用户断开连接时
@socketio.on('disconnect', namespace='/onews')
def handle_disconnect():
    logging.info('A client disconnected: %s', request.sid)
