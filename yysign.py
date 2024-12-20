#!/usr/bin/python3
# -- coding: utf-8 --
# @Time : 2023/6/30 10:23
# -------------------------------
# cron "0 0 6,8,20 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('雨云签到');

import json
import requests
import os
import time


# 变量雨云账号密码 注册地址https://www.rainyun.com/MzU4NTk=_   登录后积分中心里面 赚钱积分 (如绑定微信 直接就有2000分）就可以用积分兑换主机 需要每天晚上八点蹲点

# yyusername = os.getenv("yyusername")  # line:12
# yypassword = os.getenv("yypassword")  # line:13

def login_sign():
    # 使用 session 来保持会话
    session = requests.session()
    
    # 请求登录
    response = session.post(
        'https://api.v2.rainyun.com/user/login',
        headers={"Content-Type": "application/json"},
        data=json.dumps({"field": f"{yyusername}", "password": f"{yypassword}"})
    )
    
    if "200" in response.text:
        print("登录成功")
        csrf_token = response.cookies.get_dict()['X-CSRF-Token']
    else:
        print(f"登录失败，响应信息：{response.text}")
        return
    
    # 执行每日签到任务
    headers = {'x-csrf-token': csrf_token}
    task_response = session.post(
        'https://api.v2.rainyun.com/user/reward/tasks',
        headers=headers,
        data=json.dumps({"task_name": "每日签到", "verifyCode": ""})
    )
    
    print(f'开始签到：签到结果 {task_response.text}')

if __name__ == '__main__':
    # 获取并处理多个账号
    usernames = os.getenv("yyusername", "").split('#')
    passwords = os.getenv("yypassword", "").split('#')

    if len(usernames) != len(passwords):
        print("用户名和密码数量不匹配")
    else:
        for i in range(len(usernames)):
            yyusername = usernames[i]
            yypassword = passwords[i]
            login_sign()
