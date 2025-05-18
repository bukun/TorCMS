# -*- coding: utf-8 -*-
'''
Serveral functions.

Checking the kind of post if it is valid.

Build the directory for Whoosh database.
and locale.
'''
import os

import torcms.core.tool.whoosh_tool
from config import post_cfg
from torcms.model.role2permission_model import MRole2Permission
from torcms.model.role_model import MRole
from torcms.model.staff2role_model import MStaff2Role

# from torcms.core.tool import run_whoosh as running_whoosh
from torcms.model.user_model import MUser


def build_directory():
    '''
    Build the directory for Whoosh database, and locale.
    '''
    if os.path.exists('locale'):
        pass
    else:
        os.mkdir('locale')

    WHOOSH_DB_DIR = 'database/whoosh'
    if os.path.exists(WHOOSH_DB_DIR):
        pass
    else:
        os.makedirs(WHOOSH_DB_DIR)


def run_create_admin(*args):
    '''
    creating the default administrator.
    '''
    post_data = {
        'user_name': 'admin',
        'user_email': 'admin@osgeo.cn',
        'user_pass': 'Gg01234567',
        'role': '3300',
    }
    userinfo = MUser.get_by_name(post_data['user_name'])

    if userinfo:
        role = MRole.get_by_uid('administrators')
        if role:
            MStaff2Role.add_or_update(userinfo.uid, role.uid)
            cur_per = MRole2Permission.query_permission_by_role(role.uid)
            extinfo = {}
            extinfo['roles'] = [role.uid]
            for per in cur_per:
                extinfo[f'_per_{per["uid"]}'] = 0

            MUser.update_extinfo(userinfo.uid, extinfo)
        print(f'User `{post_data["user_name"]}` already exists.')
    else:
        out_dic = MUser.create_user(post_data)
        print('=' * 40)
        print(out_dic)
        print('=' * 40)
        role = MRole.get_by_uid('administrators')
        if 'uid' in out_dic and role:
            MStaff2Role.add_or_update(out_dic['uid'], role.uid)

            cur_per = MRole2Permission.query_permission_by_role(role.uid)
            extinfo = {}
            extinfo['roles'] = [role.uid]
            for per in cur_per:
                extinfo[f'_per_{per["uid"]}'] = 0

            MUser.update_extinfo(out_dic['uid'], extinfo)


def run_whoosh(*args):
    '''
    running whoosh
    '''
    kind_arr = []
    for key, value in post_cfg.items():
        kind_arr.append(key)

    torcms.core.tool.whoosh_tool.gen_whoosh_database(kind_arr=kind_arr)
