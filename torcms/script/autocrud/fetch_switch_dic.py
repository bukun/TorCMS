# -*- coding: utf-8
'''
Return the dictionay of the switcher form XLXS file.
if valud of the column of the row is `1`,  it will be added to the array.
'''

import os
import sys
from openpyxl.reader.excel import load_workbook
from torcms.script.autocrud.base_crud import xlsx_file, FILTER_COLUMNS

if os.path.exists(xlsx_file):
    wb = load_workbook(filename=xlsx_file)
else:
    sys.exit(0)


def gen_array_crud():
    '''
    Return the dictionay of the switcher form XLXS file.
    '''
    if wb:
        pass
    else:
        return False

    papa_id = 0

    switch_dics = {}
    kind_dics = {}

    for work_sheet in wb:
        kind_sig = str(work_sheet['A1'].value).strip()
        # the number of the categories in a website won't greater than 1000.
        for row_num in range(3, 1000):
            # 父类, column A
            A_cell_value = work_sheet['A{0}'.format(row_num)].value
            # 子类, column B
            B_cell_val = work_sheet['B{0}'.format(row_num)].value

            if A_cell_value or B_cell_val:
                pass
            else:
                break
            if A_cell_value and A_cell_value != '':
                papa_id = A_cell_value.strip()[1:]
                u_dic = __get_switch_arr(work_sheet, row_num)
                switch_dics['dic_{0}00'.format(papa_id)] = u_dic
                kind_dics['kind_{0}00'.format(papa_id)] = kind_sig
            if B_cell_val and B_cell_val != '':
                sun_id = B_cell_val.strip()[1:]
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
    for ii in FILTER_COLUMNS:
        cell_val = work_sheet['{0}{1}'.format(ii, row_num)].value
        if cell_val == 1:
            '''
            Appending the slug name of the switcher.
            '''
            u_dic.append(work_sheet['{0}1'.format(ii)].value.strip().split(',')[-1])
    return u_dic
