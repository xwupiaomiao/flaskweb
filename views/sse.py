#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =


from flask import Blueprint
from flask import Response, render_template
from .alertpost import oneques, allques
import queue, json

blue_sse = Blueprint('blue_sse', __name__, url_prefix='/sse')

# 用于存储所有sse连接的客户端
sseclients = []


# 从队列中获取数据并通过 SSE 发送，只支持一个客户端
def generate_events():
    while True:
        try:
            # 从队列中获取数据，超时时间为 1 秒
            reqdata = oneques.get(timeout=1)
            # 使用 SSE 格式发送数据
            yield f"data: {json.dumps(reqdata)}\n\n"
        except queue.Empty:
            # 如果队列为空，继续等待
            continue


# 只能向一个sse客户端推送数据
@blue_sse.route('/onestream', methods=['GET', 'POST'])
def onestream():
    # 返回一个流式响应，内容类型为 text/event-stream
    return Response(generate_events(), content_type='text/event-stream')


# 从全局队列中读取数据并推送到所有客户端
def generate_data():
    while True:
        try:
            # 从全局队列中获取数据
            data = allques.get(timeout=1)
            # 将数据推送到所有客户端的队列中
            for client in sseclients:
                client.put(data)
        except queue.Empty:
            # 如果队列为空，继续等待
            continue


# 用于接收所有 SSE 连接的函数
def event_stream(client_queue):
    while True:
        try:
            # 从客户端队列中获取数据
            data = client_queue.get(timeout=1)
            yield data
        except queue.Empty:
            # 如果队列为空，继续等待
            continue
        except Exception as e:
            # 如果发生异常，断开连接
            print(f"Client disconnected: {e}")
            break


# 向多个sse客户端推送数据
@blue_sse.route('/allstream', methods=['GET', 'POST'])
def stream():
    # 创建一个队列用于存储客户端的数据
    client_queue = queue.Queue()
    # 将客户端添加到全局列表中
    sseclients.append(client_queue)
    # 返回一个流式响应，内容类型为 text/event-stream
    return Response(event_stream(client_queue), content_type='text/event-stream')


@blue_sse.route('/', methods=['GET', 'POST'])
def sse():
    return render_template('sse.html')
