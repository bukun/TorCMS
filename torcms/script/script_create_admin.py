# -*- coding: utf-8

from torcms.model.user_model import MUser


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
        muser.create_wiki_history(post_data)


