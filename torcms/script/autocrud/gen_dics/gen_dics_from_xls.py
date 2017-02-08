# -*- coding: utf-8
'''
Generate the dic of Python from xlsx file.
'''

import os
import sys

from openpyxl.reader.excel import load_workbook

from torcms.script.autocrud.base_crud import xlsx_file, FILTER_COLUMNS

if os.path.exists(xlsx_file):
    wb = load_workbook(filename=xlsx_file)
else:
    sys.exit(0)


def write_filter_dic(fo, wk_sheet, column):
    '''
    write filter dic for certain column
    :param fo:
    :param wk_sheet:
    :param column:
    :return:
    '''
    row1_val = wk_sheet['{0}1'.format(column)].value
    row2_val = wk_sheet['{0}2'.format(column)].value
    if row1_val and row1_val != '':

        c_name, slug_name = row1_val.split(',')

        tags1 = row2_val.split(',')
        tags1 = [x.strip() for x in tags1]
        tags_dic = {}

        if len(tags1) == 1:
            tags_dic[1] = row2_val
            ctr_type = 'text'
        else:
            for index, tag_val in enumerate(tags1):
                tags_dic[index + 1] = tag_val.strip()
            ctr_type = 'select'

        fo.write('''html_{0} = {{
                        'en': 'tag_{0}',
                        'zh': '{1}',
                        'dic': {2},
                        'type': '{3}',
                        }}\n'''.format(slug_name, c_name, tags_dic, ctr_type))


def gen_html_dic():
    '''
    生成 Filter .
    :return:
    '''

    if wb:
        pass
    else:
        return False

    with open('xxtmp_html_dic.py', 'w') as fo:
        for wk_sheet in wb:
            for column in FILTER_COLUMNS:
                write_filter_dic(fo, wk_sheet, column)
