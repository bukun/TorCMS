# from bears import loger
import subprocess
from pathlib import Path

import requests

def send_email(subject, to_email, html, sender='', check=''):
    '''
    发送邮件
    :param subject: 邮件主题
    :param to_email: 收件人邮箱
    :param html: 邮件内容
    :return: True or False
    '''
    email_handler = 'https://poster.igadc.cn/email'
    headers = {'Content-Type': 'application/json'}

    payload = {
        "subject": subject,
        "email": to_email,
        "html": html,
        'sender': sender,
        'check': check,
    }
    print(payload)
    response = requests.post(email_handler, json=payload, headers=headers)
    if response.status_code == 200:
        print('请求成功:', response.text)
        # return True
    else:
        print('请求失败，状态码：', response.status_code)
        # return False
    return response.json()
#
#
# def send_email(subject, to_email, html, sender='', checker=''):
#     '''
#     发送邮件
#     :param subject: 邮件主题
#     :param to_email: 收件人邮箱
#     :param html: 邮件内容
#     :return: True or False
#     '''
#     email_handler = 'https://poster.igadc.cn/email'
#     headers = {'Content-Type': 'application/json'}
#
#     payload = {"subject": subject, "email": to_email, "html": html, 'check': ''}
#     print(payload)
#     response = requests.post(email_handler, json=payload, headers=headers)
#     if response.status_code == 200:
#         print('请求成功:', response.text)
#         return True
#     else:
#         print('请求失败，状态码：', response.status_code)
#         return False


cmd_tmpl = '/home/bk/.cache/pypoetry/virtualenvs/torcms-CsEnU2xJ-py3.11/bin/python3 -m pytest'

email_list = [
    '118171@qq.com',
    # 'bukun@live.cn',
    # '486936@qq.com',
    # '790974751@qq.com',
    # '1057246055@qq.com',
    # '478747656@qq.com',
]

for wfile in Path('.').rglob('test*.py'):
    # print(wfile)
    mdname = str(wfile)
    cmd_str = cmd_tmpl + ' ' + mdname
    print(cmd_str)
    if 'nltk' in cmd_str:
        continue
    elif 'selenium' in cmd_str:
        continue
    else:
        pass
    resuult = subprocess.run(cmd_str.split())
    re_code = resuult.returncode
    if re_code != 0:
        # loger.error('=' * 40)
        # loger.error(cmd_str)
        cnt = f'''
在单元测试中，发现以下文件未通过测试，请进行检查： <br />
{wfile}  <br /><br />

请使用以下命令进行复核：<br />
python3 -m pytest {mdname}
        '''
        send_email('TorCMS单元测试问题', email_list, cnt, sender='osgeo', check='bk')
