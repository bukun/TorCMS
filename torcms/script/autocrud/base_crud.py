# -*- coding:utf-8 -*-

'''
Basic configuration for CRUD.
'''

import os

CRUD_PATH = os.path.abspath('./templates/autogen')

XLSX_FILE = './database/meta/info_tags.xlsx'
#  The filter key stored in the colomns below.


RAW_LIST = ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

FILTER_COLUMNS = RAW_LIST + ["A" + x for x in RAW_LIST + ['A', 'B', 'C', 'D']]


def build_dir():
    '''
    Build the directory used for templates.
    :return:
    '''
    tag_arr = ['add', 'edit', 'view', 'list', 'infolist']
    path_arr = [os.path.join(CRUD_PATH, x) for x in tag_arr]
    for wpath in path_arr:
        if os.path.exists(wpath):
            continue
        os.makedirs(wpath)


INPUT_ARR = ['digits', 'text', 'date', 'number', 'email', 'url', 'download']
