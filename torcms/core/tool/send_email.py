# -*- coding:utf-8 -*-

'''
sending email via Python.
'''

import smtplib
from email.mime.text import MIMEText
from config import SMTP_CFG


def send_mail(to_list, sub, content):
    '''
    Sending email via Python.
    '''
    sender = SMTP_CFG['name'] + "<" + SMTP_CFG['user'] + ">"
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = sender
    msg['To'] = ";".join(to_list)
    try:
        # Using SMTP_SSL. The alinyun ECS has masked the 25 port since 9,2016.
        smtper = smtplib.SMTP_SSL(SMTP_CFG['host'], port=994)
        smtper.login(SMTP_CFG['user'], SMTP_CFG['pass'])
        smtper.sendmail(sender, to_list, msg.as_string())
        smtper.close()
        return True
    except:
        return False
