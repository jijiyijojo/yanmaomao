#!/usr/bin/python3  
# -- coding: utf-8 --
# @Time : 2023/6/30 10:23
# -------------------------------
# cron "0 0 6,8,20 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('雨云签到');

import json
import requests
import os

## 变量雨云账号密码 注册地址https://www.rainyun.com/MzU4NTk=_   登录后积分中心里面 赚钱积分 (如绑定微信 直接就有2000分）就可以用积分兑换主机 需要每天晚上八点蹲点

# yyusername = os.getenv("yyusername")  # line:12
# yypassword = os.getenv("yypassword")  # line:13

def login_sign():
    session = requests.session()
    response = session.post(
        'https://api.v2.rainyun.com/user/login',
        headers={"Content-Type": "application/json"},
        data=json.dumps({"field": f"{yyusername}", "password": f"{yypassword}"})
    )
    
    if response.text.find("200") > -1:
        print("登录成功")
        csrf_token = response.cookies.get_dict()['X-CSRF-Token']
    else:
        print(f"登录失败，响应信息：{response.text}")
        return  # 退出函数，避免后续代码执行

    headers = {'x-csrf-token': csrf_token}
    reward_response = session.post(
        'https://api.v2.rainyun.com/user/reward/tasks',
        headers=headers,
        data=json.dumps({"task_name": "每日签到", "verifyCode": ""})
    )
    print('开始签到：签到结果 ' + reward_response.text)

if __name__ == '__main__':
    for i in range(len(os.getenv("yyusername").split('#'))):
        yyusername = os.getenv("yyusername").split('#')[i]
        yypassword = os.getenv("yypassword").split('#')[i]
        login_sign()
