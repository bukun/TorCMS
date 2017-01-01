# -*- coding:utf-8 -*-
'''
建立
'''
import os

whoosh_database = 'database/whoosh'

def build_directory():
    if os.path.exists('locale'):
        pass
    else:
        os.mkdir('locale')
    if os.path.exists(whoosh_database):
        pass
    else:
        os.makedirs(whoosh_database)

