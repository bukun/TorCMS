# -*- coding: utf-8 -*-
'''
Serveral functions.

Checking the kind of post if it is valid.

Build the directory for Whoosh database.
and locale.
'''
import os

import torcms.core.tool.whoosh_tool
from config import DB_CON, kind_arr, post_type
from torcms.core.tool import run_whoosh as running_whoosh
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
    if MUser.get_by_name(post_data['user_name']):
        print(f'User `{post_data["user_name"]}` already exists.')
    else:
        MUser.create_user(post_data)


def run_whoosh(*args):
    '''
    running whoosh
    '''
    torcms.core.tool.whoosh_tool.gen_whoosh_database(kind_arr=kind_arr)
