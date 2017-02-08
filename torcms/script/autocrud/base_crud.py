# -*- coding:utf-8 -*-
import os

crud_path = os.path.abspath('./templates/autogen')

xlsx_file = './database/meta/info_tags.xlsx'
#  The filter key stored in the colomns below.
FILTER_COLUMNS = ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                  'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def build_dir():
    '''
    Build the directory used for templates.
    :return:
    '''
    tag_arr = ['add', 'edit', 'view', 'list', 'infolist']
    path_arr = [os.path.join(crud_path, x) for x in tag_arr]
    for wpath in path_arr:
        if os.path.exists(wpath):
            continue
        os.makedirs(wpath)