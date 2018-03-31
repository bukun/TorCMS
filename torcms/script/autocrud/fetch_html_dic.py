# -*- coding: utf-8
'''
Generate the dic of Python from xlsx file.
Only using the first and the second row of the XLSX file.
'''

import os
import sys

from openpyxl.reader.excel import load_workbook
from .base_crud import XLSX_FILE, FILTER_COLUMNS, INPUT_ARR

if os.path.exists(XLSX_FILE):
    WORK_BOOK = load_workbook(filename=XLSX_FILE)
else:
    print('There must be at least one XLSX file.')
    sys.exit(0)


def __write_filter_dic(wk_sheet, column):
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
        slug_name, c_name = [x.strip() for x in row1_val.strip().split(',')]
        # slug_name = slug_name.lower()

        tags1 = [x.strip() for x in row2_val.split(',')]
        tags_dic = {}

        #  if only one tag,
        if len(tags1) == 1:
            xx_1 = row2_val.split(':')  # 'text'  # HTML text input control.

            # The default type of the input is text
            # if xx_1[0].lower() == 'download':
            #     xx_1[0] = 'url'
            # elif xx_1[0].lower() in INPUT_ARR:


            if xx_1[0].lower() in INPUT_ARR:
                xx_1[0] = xx_1[0].lower()
            else:
                xx_1[0] = 'text'

            if len(xx_1) == 2:
                ctr_type, unit = xx_1
            else:
                ctr_type = xx_1[0]
                unit = ''
            tags_dic[1] = unit

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

    if WORK_BOOK:
        pass
    else:
        return False

    html_dics = {}
    for wk_sheet in WORK_BOOK:
        for column in FILTER_COLUMNS:
            kkey, kval = __write_filter_dic(wk_sheet, column)
            if kkey:
                html_dics[kkey] = kval
    return html_dics


def gen_array_crud():
    '''
    Return the dictionay of the switcher form XLXS file.
    if valud of the column of the row is `1`,  it will be added to the array.
    '''
    if WORK_BOOK:
        pass
    else:
        return False

    papa_id = 0

    switch_dics = {}
    kind_dics = {}

    for work_sheet in WORK_BOOK:
        kind_sig = str(work_sheet['A1'].value).strip()
        # the number of the categories in a website won't greater than 1000.
        for row_num in range(3, 1000):
            # 父类, column A
            a_cell_value = work_sheet['A{0}'.format(row_num)].value
            # 子类, column B
            b_cell_val = work_sheet['B{0}'.format(row_num)].value

            if a_cell_value or b_cell_val:
                pass
            else:
                break
            if a_cell_value and a_cell_value != '':
                papa_id = a_cell_value.strip()[1:]
                u_dic = __get_switch_arr(work_sheet, row_num)
                switch_dics['dic_{0}00'.format(papa_id)] = u_dic
                kind_dics['kind_{0}00'.format(papa_id)] = kind_sig
            if b_cell_val and b_cell_val != '':
                sun_id = b_cell_val.strip()[1:]
                if len(sun_id) == 4:
                    app_uid = sun_id
                else:
                    app_uid = '{0}{1}'.format(papa_id, sun_id)
                u_dic = __get_switch_arr(work_sheet, row_num)
                switch_dics['dic_{0}'.format(app_uid)] = u_dic
                kind_dics['kind_{0}'.format(app_uid)] = kind_sig

    return (switch_dics, kind_dics)


def __get_switch_arr(work_sheet, row_num):
    '''
    if valud of the column of the row is `1`,  it will be added to the array.
    :param work_sheet:
    :param row_num:
    :return:
    '''
    u_dic = []
    for col_idx in FILTER_COLUMNS:
        cell_val = work_sheet['{0}{1}'.format(col_idx, row_num)].value
        if cell_val in [1, '1']:
            # Appending the slug name of the switcher.
            u_dic.append(work_sheet['{0}1'.format(col_idx)].value.strip().split(',')[0])
    return u_dic
