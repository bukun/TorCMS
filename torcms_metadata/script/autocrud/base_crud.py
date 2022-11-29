# -*- coding:utf-8 -*-
'''
Basic configuration for CRUD.
'''

import os

CRUD_PATH = os.path.abspath('./torcms_metadata/autogen')

META_DIR = './torcms_metadata'
META_TAG_DIR = './database/meta'
XLSX_FILE = './torcms_metadata/meta_元数据模板20220921.xlsx'

for wfile in os.listdir(META_DIR):
    if wfile.startswith('~'):
        continue
    if wfile.lower().endswith('.xlsx'):
        XLSX_FILE = os.path.join(META_DIR, wfile)

for wfile in os.listdir(META_TAG_DIR):
    if wfile.startswith('~'):
        continue
    if wfile.lower().endswith('.xlsx'):
        XLSX_FILE_TAG = os.path.join(META_TAG_DIR, wfile)
# The filter key stored in the colomns below.
RAW_LIST = [
    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
    'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

FILTER_COLUMNS = RAW_LIST + ["A" + x for x in ['A', 'B', 'C', 'D'] + RAW_LIST] + \
                 ["B" + x for x in ['A', 'B', 'C', 'D'] + RAW_LIST] + \
                 ["C" + x for x in ['A', 'B', 'C', 'D'] + RAW_LIST] + \
                 ["D" + x for x in ['A', 'B', 'C', 'D'] + RAW_LIST]


def build_dir():
    '''
    Build the directory used for templates.
    '''
    tag_arr = ['add', 'edit', 'view', 'list', 'infolist']
    path_arr = [os.path.join(CRUD_PATH, x) for x in tag_arr]
    for wpath in path_arr:
        if os.path.exists(wpath):
            continue
        os.makedirs(wpath)


INPUT_ARR = ['digits', 'text', 'date', 'number', 'email', 'url', 'download']
