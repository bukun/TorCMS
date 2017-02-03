# -*- coding: utf-8

import os
import yaml
# import json

# from torcms.model.category_model import MCategory
from openpyxl.reader.excel import load_workbook
from torcms.model.category_model import MCategory


def gen_xlsx_category():
    xlsx_file = './database/meta/info_tags.xlsx'
    if os.path.exists(xlsx_file):
        print('Got it')
        pass
    else:
        print('The xlsx file does not exists.')
        return
    wb = load_workbook(filename=xlsx_file)
    mappcat = MCategory()
    # 在分类中排序
    order_index = 1

    for sheet_ranges in wb:
        print(dir(sheet_ranges))
        print(sheet_ranges.title)
        kind_sig = str(sheet_ranges['A1'].value).strip()

        for row_num in range(3, 10000):

            # 父类
            A_cell_val = sheet_ranges['A{0}'.format(row_num)].value
            B_cell_val = sheet_ranges['B{0}'.format(row_num)].value
            C_cell_val = sheet_ranges['C{0}'.format(row_num)].value

            if A_cell_val or B_cell_val or C_cell_val:
                pass
            else:
                break

            if A_cell_val and A_cell_val != '':
                cell_arr = A_cell_val.strip()
                p_uid = cell_arr[1:]  # 所有以 t 开头
                t_slug = sheet_ranges['C{0}'.format(row_num)].value.strip()
                t_title = sheet_ranges['D{0}'.format(row_num)].value.strip()
                u_uid = '{0}00'.format(p_uid)
                pp_uid = '0000'
            elif B_cell_val and B_cell_val != '':
                cell_arr = B_cell_val
                c_iud = cell_arr[1:]
                t_slug = sheet_ranges['C{0}'.format(row_num)].value.strip()
                t_title = sheet_ranges['D{0}'.format(row_num)].value.strip()
                u_uid = '{0}{1}'.format(p_uid, c_iud)
                pp_uid = '{0}00'.format(p_uid)
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
            print(post_data)
            mappcat.create_wiki_history(u_uid, post_data)
            order_index += 1


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
                'tmpl': 1,
                'pid': '0000',
                'order': porder * 100,
                'kind': '{0}'.format(sig),
            }

            mcat.create_wiki_history(uid, cat_dic)
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

                    mcat.create_wiki_history(pid + uid, cat_dic)


def gen_yaml_category():
    for wroot, wdirs, wfiles in os.walk('./database/meta'):
        for wfile in wfiles:
            if wfile.endswith('.yaml'):
                gen_category(os.path.join(wroot, wfile), wfile[0])


def run_gen_category():
    print('run gen category')
    gen_yaml_category()
    gen_xlsx_category()
