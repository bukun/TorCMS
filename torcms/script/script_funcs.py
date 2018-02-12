# -*- coding: utf-8 -*-
'''
Serveral functions.

Checking the kind of post if it is valid.

Build the directory for Whoosh database.
and locale.
'''
import os

from config import router_post, kind_arr, post_type
from torcms.core.tool import run_whoosh as running_whoosh
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
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


def run_check_kind(_):
    '''
    Running the script.
    '''
    for kindv in router_post:
        for rec_cat in MCategory.query_all(kind=kindv):
            catid = rec_cat.uid
            catinfo = MCategory.get_by_uid(catid)
            for rec_post2tag in MPost2Catalog.query_by_catid(catid):
                postinfo = MPost.get_by_uid(rec_post2tag.post_id)
                if postinfo.kind == catinfo.kind:
                    pass
                else:
                    print(postinfo.uid)


def run_create_admin(*args):
    '''
    creating the default administrator.
    '''
    post_data = {
        'user_name': 'giser',
        'user_email': 'giser@osgeo.cn',
        'user_pass': '131322',
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


def run_update_cat(_):
    '''
    Update the catagery.
    '''
    recs = MPost2Catalog.query_all().objects()
    for rec in recs:
        if rec.tag_kind != 'z':
            print('-' * 40)
            print(rec.uid)
            print(rec.tag_id)
            print(rec.par_id)

            MPost2Catalog.update_field(rec.uid, par_id=rec.tag_id[:2] + "00")
