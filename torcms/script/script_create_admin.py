# -*- coding: utf-8

from torcms.core.tool.send_email import send_mail

from torcms.model.user_model import MUser
import time
from config_email import email_cfg
from config import smtp_cfg
def run_create_admin():
    post_data = {
        'user_name': 'giser',
        'user_email': 'giser@osgeo.cn',
        'user_pass': '131322',
        'role': '3330',
    }
    muser = MUser()
    entry = muser.get_by_name(post_data['user_name'])
    if entry:
        pass
    else:
        muser.insert_data(post_data)


