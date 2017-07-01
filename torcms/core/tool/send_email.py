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
        # Using SMTP_SSL. The alinyun ECS has masked the 25 port since 9,2016.
        s = smtplib.SMTP_SSL(SMTP_CFG['host'], port=994)
        s.login(SMTP_CFG['user'], SMTP_CFG['pass'])
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except:
        return False
