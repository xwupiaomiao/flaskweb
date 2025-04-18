#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ =

import requests, time

# 目标 URL
url = 'http://127.0.0.1:5000/alertpost'

# POST请求的数据（可以是字典、JSON字符串等）
data = {
    'name': '192.168.1.1',
    'description': 'eth0 down',
    'states': False,
    'date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
}


def send():
    # 请求头（可选）
    headers = {
        'Content-Type': 'application/json',  # 设置内容类型为 JSON
    }

    # 发送 POST 请求
    response = requests.post(url, json=data, headers=headers)

    # 处理响应
    if response.status_code == 200:  # 检查请求是否成功
        print('Request was successful!')
        print('Response JSON:', response.json())  # 解析 JSON 响应
    else:
        print(f'Request failed with status code {response.status_code}')
        print('Response text:', response.text)  # 打印原始响应内容


if __name__ == '__main__':
    while True:
        send()
        time.sleep(10)