# -*- coding: utf-8

import os
import yaml
import json

from torcms.model.category_model import MCategory
from openpyxl.reader.excel import load_workbook
from torcms.model.category_model import MCategory


def gen_xlsx_category():
    xlsx_file = './database/meta/info_tags.xlsx'
    if os.path.exists(xlsx_file):
        pass
    else:
        return
    wb = load_workbook(filename=xlsx_file)
    mappcat = MCategory()
    # 在分类中排序
    order_index = 1
    # 父类索引
    papa_index = 1
    # 子类索引
    c_index = 1
    papa_id = 0
    uid = ''
    p_dic = {}
    # 逐行遍历
    for sheet_ranges in wb:
        # sheet_ranges = wb[st_rag_name]
        kind_sig = str(sheet_ranges['A1'].value).strip()

        # index = 2
        # for xx_row in wb.iter_cols(min_row  = 3):
        #     row_num = row_num + 1
        for row_num in range(3, 10000):
            # 父类
            p_cell_val = sheet_ranges['A{0}'.format(row_num)].value
            b_cell_val = sheet_ranges['B{0}'.format(row_num)].value
            c_cell_val = sheet_ranges['C{0}'.format(row_num)].value

            if p_cell_val or b_cell_val or c_cell_val:
                pass
            else:
                break

            if p_cell_val and p_cell_val != '':
                cell_arr = p_cell_val.split(',')
                p_uid = cell_arr[0].strip().strip('t')
                t_name_arr = sheet_ranges['B{0}'.format(row_num)].value.strip().split(',')
                u_uid = '{0}00'.format(p_uid)
                pp_uid = '0000'


            if c_cell_val and c_cell_val != '':
                cell_arr = b_cell_val.split(',')
                c_iud = cell_arr[0].strip().strip('t')
                t_name_arr = c_cell_val.strip().split(',')
                u_uid = '{0}{1}'.format(p_uid, c_iud)
                pp_uid = '{0}00'.format(p_uid)

            post_data = {
                'name': t_name_arr[0],
                'slug': t_name_arr[1],
                'order': order_index,
                'uid': u_uid,
                'tmpl': 1,
                'pid': pp_uid,
                'kind': kind_sig,
            }
            print(post_data)
            mappcat.create_page(u_uid, post_data)
            order_index = order_index + 1

def gen_category(yaml_file, sig):
    mcat = MCategory()
    f = open(yaml_file)
    out_dic = yaml.load(f)

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
                'tmpl':1,
                'pid': '0000',
                'order': porder * 100,
                'kind': '{0}'.format(sig),
            }

            mcat.create_page(uid, cat_dic)
        else:
            sub_arr = out_dic[key]
            pid = key[1:3]

            for sub_dic in sub_arr:
                porder = out_dic['z' + pid + '00']['order']

                for key in sub_dic:
                    uid = key[1:]

                    cur_dic = sub_dic[key]

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

                    mcat.create_page(pid + uid, cat_dic)


def gen_yaml_category():
    for wroot, wdirs, wfiles in os.walk('./database/meta'):
        for wfile in wfiles:
            if wfile.endswith('.yaml'):
                gen_category(os.path.join(wroot, wfile), wfile[0])


def run_gen_category():
    gen_yaml_category()
    gen_xlsx_category()
