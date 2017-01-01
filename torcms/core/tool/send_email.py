# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from config import smtp_cfg

def send_mail(to_list, sub, content):
    me = smtp_cfg['name'] + "<" + smtp_cfg['user'] + ">"
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(smtp_cfg['host'])
        s.login(smtp_cfg['user'], smtp_cfg['pass'])
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except:
        return False
