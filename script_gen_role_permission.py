# -*- coding: utf-8
'''
Genereting catetory.
'''
import os

import yaml
from openpyxl.reader.excel import load_workbook

from torcms.model.category_model import MCategory

from torcms.model.permission_model import MPermission
from torcms.model.role_model import MRole

XLSX_FILE = './database/role_perm.xlsx'


def gen_xlsx_category():
    '''
    Genereting role,permission from xlsx file.
    '''


    all_cate_arr = []

    for sheet_ranges in load_workbook(filename=XLSX_FILE):
        kind_sig = str(sheet_ranges['A1'].value).strip()


        for row_num in range(3, 10000):

            # 父类
            a_cell_val = sheet_ranges['A{0}'.format(row_num)].value
            b_cell_val = sheet_ranges['B{0}'.format(row_num)].value
            c_cell_val = sheet_ranges['C{0}'.format(row_num)].value
            d_cell_val = sheet_ranges['D{0}'.format(row_num)].value

            if a_cell_val and a_cell_val != '':
                cell_arr = a_cell_val.strip()
                uid = kind_sig + cell_arr.split(":")[0]
                name = cell_arr.split(":")[1]
                pid = '0000'
                auid=uid
            elif b_cell_val and b_cell_val != '':
                cell_arr = b_cell_val
                uid = kind_sig + cell_arr.split(":")[0]
                pid = auid
                name =  name = cell_arr.split(":")[1]
                buid=uid
            elif c_cell_val and c_cell_val != '':
                cell_arr = c_cell_val
                uid = kind_sig + cell_arr.split(":")[0]
                pid = buid
                name = name = cell_arr.split(":")[1]
                cuid=uid
            elif d_cell_val and d_cell_val != '':
                cell_arr = d_cell_val
                uid = kind_sig + cell_arr.split(":")[0]
                pid = cuid
                name = name = cell_arr.split(":")[1]

            else:
                continue

            post_data = {
                'name': name,
                'uid': uid,
                'pid': pid
            }

            all_cate_arr.append(post_data)
            MRole.add_or_update(uid, post_data)

    return all_cate_arr





def run_gen_category(*args):
    '''
    to run
    '''
    gen_xlsx_category()

if __name__ == '__main__':
    gen_xlsx_category()