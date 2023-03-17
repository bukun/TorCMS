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
    Genereting catetory from xlsx file.
    '''

    # 在分类中排序
    order_index = 1

    all_cate_arr = []

    for sheet_ranges in load_workbook(filename=XLSX_FILE):
        kind_sig = sheet_ranges.get_sheet_names()
        print(kind_sig)

    #     for row_num in range(3, 10000):
    #
    #         # 父类
    #         a_cell_val = sheet_ranges['A{0}'.format(row_num)].value
    #         b_cell_val = sheet_ranges['B{0}'.format(row_num)].value
    #         c_cell_val = sheet_ranges['C{0}'.format(row_num)].value
    #
    #         if a_cell_val or b_cell_val or c_cell_val:
    #             pass
    #         else:
    #             break
    #
    #         if a_cell_val and a_cell_val != '':
    #             cell_arr = a_cell_val.strip()
    #             p_uid = cell_arr[1:]  # 所有以 t 开头
    #             t_slug = sheet_ranges['C{0}'.format(row_num)].value.strip()
    #             t_title = sheet_ranges['D{0}'.format(row_num)].value.strip()
    #             u_uid = p_uid + (4 - len(p_uid)) * '0'
    #             pp_uid = '0000'
    #         elif b_cell_val and b_cell_val != '':
    #             cell_arr = b_cell_val
    #             c_iud = cell_arr[1:]
    #             t_slug = sheet_ranges['C{0}'.format(row_num)].value.strip()
    #             t_title = sheet_ranges['D{0}'.format(row_num)].value.strip()
    #             if len(c_iud) == 4:
    #                 u_uid = c_iud
    #             else:
    #                 u_uid = '{0}{1}'.format(p_uid, c_iud)
    #             pp_uid = p_uid + (4 - len(p_uid)) * '0'
    #         else:
    #             continue
    #
    #         post_data = {
    #             'name': t_title,
    #             'slug': t_slug,
    #             'order': order_index,
    #             'uid': u_uid,
    #             'pid': pp_uid,
    #             'kind': kind_sig,
    #         }
    #         all_cate_arr.append(post_data)
    #         MCategory.add_or_update(u_uid, post_data)
    #         order_index += 1
    # return all_cate_arr





def run_gen_role_permission(*args):
    '''
    to run
    '''
    gen_xlsx_category()

if __name__ == '__main__':
    run_gen_role_permission()