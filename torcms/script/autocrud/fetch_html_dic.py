# -*- coding: utf-8
'''
Generate the dic of Python from xlsx file.
Only using the first and the second row of the XLSX file.
'''

import os
import sys

from openpyxl.reader.excel import load_workbook

from torcms.script.autocrud.base_crud import xlsx_file, FILTER_COLUMNS

if os.path.exists(xlsx_file):
    wb = load_workbook(filename=xlsx_file)
else:
    sys.exit(0)


def write_filter_dic(wk_sheet, column):
    '''
    return filter dic for certain column
    :param fo:
    :param wk_sheet:
    :param column:
    :return:
    '''
    row1_val = wk_sheet['{0}1'.format(column)].value
    row2_val = wk_sheet['{0}2'.format(column)].value
    if row1_val and row1_val.strip() != '':
        row2_val = row2_val.strip()
        # c_name, slug_name = row1_val.strip().split(',')
        c_name, slug_name = [x.strip() for x in row1_val.strip().split(',')]

        tags1 = [x.strip() for x in row2_val.split(',')]
        tags_dic = {}

        #  if only one tag,
        if len(tags1) == 1:
            ctr_type = 'text'  # HTML text input control.
            tags_dic[1] = row2_val

        else:
            ctr_type = 'select'  # HTML selectiom control.
            for index, tag_val in enumerate(tags1):
                # the index of tags_dic starts from 1.
                tags_dic[index + 1] = tag_val.strip()

        outkey = 'html_{0}'.format(slug_name)
        outval = {
            'en': 'tag_{0}'.format(slug_name),
            'zh': c_name,
            'dic': tags_dic,
            'type': ctr_type,
        }
        return (outkey, outval)
    else:
        return (None, None)


def gen_html_dic():
    '''
    生成 Filter .
    :return:
    '''

    if wb:
        pass
    else:
        return False

    html_dics = {}
    for wk_sheet in wb:
        for column in FILTER_COLUMNS:
            kkey, kval = write_filter_dic(wk_sheet, column)
            if kkey:
                html_dics[kkey] = kval
    return html_dics
