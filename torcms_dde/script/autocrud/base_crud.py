# -*- coding:utf-8 -*-
'''
Basic configuration for CRUD.
'''

import os
from pathlib import Path

from torcms_dde._config import xlsx_src

CRUD_PATH = os.path.abspath('./templates/autogen')

META_TAG_DIR = './database/meta'
XLSX_FILE = xlsx_src

META_FILE_LIST = []

for wfile in Path(META_TAG_DIR).rglob('*.xlsx'):
    if wfile.name.startswith('~'):
        continue
    if wfile.name.startswith('torcms_dde_'):
        pass
    else:
        continue
    META_FILE_LIST.append(wfile)


# The filter key stored in the colomns below.
RAW_LIST = [
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z',
]

FILTER_COLUMNS = (
    RAW_LIST
    + ["A" + x for x in ['A', 'B', 'C', 'D'] + RAW_LIST]
    + ["B" + x for x in ['A', 'B', 'C', 'D'] + RAW_LIST]
    + ["C" + x for x in ['A', 'B', 'C', 'D'] + RAW_LIST]
    + ["D" + x for x in ['A', 'B', 'C', 'D'] + RAW_LIST]
)


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
