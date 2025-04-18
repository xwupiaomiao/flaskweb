#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =


import queue
from flask import Blueprint
from flask import request, jsonify, json
from settings import alertmsg, recovermsg
blue_alertpost = Blueprint('blue_alertpost', __name__, url_prefix='/alertpost')

# 创建队列用于sse推送数据
allques = queue.Queue()
oneques = queue.Queue()
# 创建队列用于存储需要websocket推送的数据
wsques = queue.Queue()


# 接收client发送的消息，把接收的消息使用websocket和sse推送到web浏览器
@blue_alertpost.route('/', methods=['GET', 'POST'])
def reqpost():
    if request.method == 'POST':
        if request.is_json:
            recmsg = request.get_json()
            if recmsg.get('states'):
                alertmsg['告警主机'] = recmsg.get('name')
                alertmsg['告警详情'] = recmsg.get('description')
                alertmsg['触发时间'] = recmsg.get('date')
                # 把消息推送到所有websocket客户端
                wsques.put(alertmsg)
                # 把消息推送到一个sse客户端
                oneques.put(alertmsg)
                # 把消息推送到所有sse客户端
                allques.put(f"data: {json.dumps(alertmsg)}\n\n")
            else:
                recovermsg['告警主机'] = recmsg.get('name')
                recovermsg['告警详情'] = recmsg.get('description')
                recovermsg['触发时间'] = recmsg.get('date')
                # 把消息推送到所有websocket客户端
                wsques.put(recovermsg)
                # 把消息推送到一个sse客户端
                oneques.put(recovermsg)
                # 把消息推送到所有sse客户端
                allques.put(f"data: {json.dumps(recovermsg)}\n\n")
            return jsonify('success')
        else:
            return jsonify({"error": "请求类型必须是JSON"}), 400
