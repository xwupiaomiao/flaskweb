#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =
# pip install netifaces
# pip install Flask
# pip install gevent
# pip install gevent-websocket
# pip install Flask-SocketIO
# pip install flask-sqlalchemy
# pip install func-timeout

# 解决requests  post请求递归次数太多的问题，一定要在导入gevent模块前导入
from gevent import monkey

monkey.patch_all()

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from views import app
from views.alertws import background_thread
from views.sse import generate_data
import threading
import logging
import os, socket, netifaces
from views.models import db

LOGPATH = f"{os.path.splitext(os.path.abspath(__file__))[0]}.log"

# 配置基本日志设置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(LOGPATH),  # 输出日志到文件
                        logging.StreamHandler()  # 输出日志到控制台
                    ])


# 获取hosts文件中主机名解析的IP
# local_ip = socket.gethostbyname(socket.gethostname())


# 获取默认网关
def get_default_gateway():
    gateways = netifaces.gateways()
    default_gateway = gateways.get('default', {})
    ipv4_gateway = default_gateway.get(netifaces.AF_INET)
    if ipv4_gateway:
        return ipv4_gateway[0]
    return None


# 获取当前可连接网络的IP
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接一个外部地址，不真正发送数据，用以获取本机IP
        s.connect((get_default_gateway(), 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


local_ip = get_local_ip()

# 启动 WSGI 服务器
if __name__ == "__main__":
    # 启动flask时创建数据库表，表结构在models.py文件中
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # 启动后台线程从队列中发送数据到websocket client
    threading.Thread(target=background_thread, daemon=True).start()
    # 启动一个线程，从全局队列中读取数据并推送到所有sse客户端
    threading.Thread(target=generate_data, daemon=True).start()
    # 绑定到所有网络接口，端口为 5000
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    print(f"WebSocket server started on http://{local_ip}:5000")
    # 启动服务器
    server.serve_forever()
