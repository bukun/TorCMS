# -*- coding: utf-8

from torcms.core.tool.send_email import send_mail

from torcms.model.user_model import MUser
import time
from config_email import email_cfg
from config import smtp_cfg

def run_send_all():
    muser = MUser()
    user_recs = muser.query_all()
    for user_rec in user_recs:
        email_add = user_rec.user_email
        print(email_add)
        send_mail([email_add], "{0}|{1}".format(smtp_cfg['name'], email_cfg['title']), email_cfg['content'])

def run_send_nologin():
    muser = MUser()
    user_recs = muser.query_nologin()
    for user_rec in user_recs:
        email_add = user_rec.user_email
        print(email_add)
        send_mail([email_add], "{0}|{1}".format(smtp_cfg['name'], email_cfg['title']), email_cfg['content'])
        muser.set_sendemail_time(user_rec.uid)
