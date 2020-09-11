# -*- coding: utf-8 -*-
'''
Serveral functions.

Checking the kind of post if it is valid.

Build the directory for Whoosh database.
and locale.
'''
import os

from config import kind_arr, post_type
from torcms.core.tool import run_whoosh as running_whoosh
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.user_model import MUser

WHOOSH_DB_DIR = 'database/whoosh'


def build_directory():
    '''
    Build the directory for Whoosh database, and locale.
    '''
    if os.path.exists('locale'):
        pass
    else:
        os.mkdir('locale')
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
        'user_pass': '01234567',
        'role': '3300',
    }
    if MUser.get_by_name(post_data['user_name']):
        print('User {user_name} already exists.'.format(user_name='giser'))
    else:
        MUser.create_user(post_data)


def run_whoosh(*args):
    '''
    running whoosh
    '''
    running_whoosh.gen_whoosh_database(kind_arr=kind_arr, post_type=post_type)


