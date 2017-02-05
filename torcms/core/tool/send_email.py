# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from config import SMTP_CFG


def send_mail(to_list, sub, content):
    me = SMTP_CFG['name'] + "<" + SMTP_CFG['user'] + ">"
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(SMTP_CFG['host'])
        s.login(SMTP_CFG['user'], SMTP_CFG['pass'])
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except:
        return False
