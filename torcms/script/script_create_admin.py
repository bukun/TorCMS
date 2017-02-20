# -*- coding: utf-8

'''
creating the default administrator.
'''

from torcms.model.user_model import MUser


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
