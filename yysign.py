import json
import requests
import os
import logging

# 配置日志
logging.basicConfig(filename='rainyun_sign.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 定义API接口URL
API_BASE_URL = 'https://api.v2.rainyun.com'
LOGIN_URL = f'{API_BASE_URL}/user/login'
SIGN_IN_URL = f'{API_BASE_URL}/user/reward/tasks'

def login_and_sign(username, password):
    session = requests.Session()
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'field': username, 'password': password})

    try:
        response = session.post(LOGIN_URL, headers=headers, data=data)
        response.raise_for_status()  # 抛出异常，如果响应状态码不是 200

        csrf_token = session.cookies.get_dict()['X-CSRF-Token']
        headers['x-csrf-token'] = csrf_token

        sign_in_data = json.dumps({'task_name': '每日签到', 'verifyCode': ''})
        sign_in_response = session.post(SIGN_IN_URL, headers=headers, data=sign_in_data)
        sign_in_response.raise_for_status()

        logging.info(f"用户 {username} 签到成功：{sign_in_response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"用户 {username} 签到失败：{e}")

if __name__ == '__main__':
    yyusernames = os.getenv("yyusername").split('#')
    yypasswords = os.getenv("yypassword").split('#')

    for username, password in zip(yyusernames, yypasswords):
        login_and_sign(username, password)
