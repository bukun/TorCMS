# -*- coding: utf-8
'''
Genereting catetory.
'''
import os

import yaml
from openpyxl.reader.excel import load_workbook

from torcms.model.category_model import MCategory

from .autocrud.base_crud import XLSX_FILE_LIST


def gen_xlsx_category():
    '''
    Genereting catetory from xlsx file.
    '''
    for XLSX_FILE in XLSX_FILE_LIST:
        if XLSX_FILE.exists():
            pass
        else:
            continue
        # 在分类中排序
        order_index = 1

        all_cate_arr = []

        for sheet_ranges in load_workbook(filename=XLSX_FILE):
            kind_sig = str(sheet_ranges['A1'].value).strip()

            for row_num in range(3, 10000):

                # 父类
                a_cell_val = sheet_ranges['A{0}'.format(row_num)].value
                b_cell_val = sheet_ranges['B{0}'.format(row_num)].value
                c_cell_val = sheet_ranges['C{0}'.format(row_num)].value

                if a_cell_val or b_cell_val or c_cell_val:
                    pass
                else:
                    break

                if a_cell_val and a_cell_val != '':
                    cell_arr = a_cell_val.strip()
                    p_uid = cell_arr[1:]  # 所有以 t 开头
                    t_slug = sheet_ranges['C{0}'.format(row_num)].value.strip()
                    t_title = sheet_ranges['D{0}'.format(row_num)].value.strip()
                    u_uid = p_uid + (4 - len(p_uid)) * '0'
                    pp_uid = '0000'
                elif b_cell_val and b_cell_val != '':
                    cell_arr = b_cell_val
                    c_iud = cell_arr[1:]
                    t_slug = sheet_ranges['C{0}'.format(row_num)].value.strip()
                    t_title = sheet_ranges['D{0}'.format(row_num)].value.strip()
                    if len(c_iud) == 4:
                        u_uid = c_iud
                    else:
                        u_uid = '{0}{1}'.format(p_uid, c_iud)
                    pp_uid = p_uid + (4 - len(p_uid)) * '0'
                else:
                    continue

                post_data = {
                    'name': t_title,
                    'slug': t_slug,
                    'order': order_index,
                    'uid': u_uid,
                    'pid': pp_uid,
                    'kind': kind_sig,
                }
                all_cate_arr.append(post_data)
                MCategory.add_or_update(u_uid, post_data)
                order_index += 1
    return all_cate_arr


def gen_category(yaml_file, sig):
    '''
    Genereting catetory from YAML file.
    '''

    out_dic = yaml.full_load(open(yaml_file))

    for key in out_dic:

        if key.endswith('00'):
            uid = key[1:]
            cur_dic = out_dic[key]
            porder = cur_dic['order']
            cat_dic = {
                'uid': uid,
                'slug': cur_dic['slug'],
                'name': cur_dic['name'],
                'count': 0,
                'tmpl': 1,
                'pid': '0000',
                'order': porder * 100,
                'kind': '{0}'.format(sig),
            }

            MCategory.add_or_update(uid, cat_dic)
        else:
            sub_arr = out_dic[key]
            pid = key[1:3]

            for sub_dic in sub_arr:
                porder = out_dic['z' + pid + '00']['order']

                for key2 in sub_dic:
                    uid = key2[1:]

                    cur_dic = sub_dic[key2]

                    sorder = cur_dic['order']
                    cat_dic = {
                        'uid': uid,
                        'slug': cur_dic['slug'],
                        'name': cur_dic['name'],
                        'count': 0,
                        'tmpl': 1,
                        'pid': pid + '00',
                        'order': porder * 100 + sorder,
                        'kind': '{0}'.format(sig),
                    }

                    MCategory.add_or_update(pid + uid, cat_dic)


def gen_yaml_category():
    '''
    find YAML.
    '''
    for wroot, _, wfiles in os.walk('./database/meta'):
        for wfile in wfiles:
            if wfile.endswith('.yaml'):
                gen_category(os.path.join(wroot, wfile), wfile[0])


def run_gen_category(*args):
    '''
    to run
    '''
    gen_yaml_category()
    gen_xlsx_category()
