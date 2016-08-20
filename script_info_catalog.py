# -*- coding: utf-8
from openpyxl.reader.excel import load_workbook
from torcms.model.minforcatalog import MInforCatalog

wb = load_workbook(filename='./database/meta/info_tags.xlsx')
sheet_ranges_arr = [wb['Sheet1'], wb['Sheet2']]
class_arr = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
sig_name_arr = []
mappcat = MInforCatalog()


def uu():
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
    for sheet_ranges in sheet_ranges_arr:

        for row_num in range(3, 48):
            # 父类
            p_cell_val = sheet_ranges['A{0}'.format(row_num)].value
            if p_cell_val and p_cell_val != '':
                cell_arr = p_cell_val.split(',')
                p_uid = cell_arr[0].strip().strip('t')
                priv_mask = cell_arr[1].strip().strip('t')
                t_name_arr = sheet_ranges['B{0}'.format(row_num)].value.strip().split(',')
                u_uid = '{0}00'.format(p_uid)

            # 子类
            b_cell_val = sheet_ranges['B{0}'.format(row_num)].value
            c_cell_val = sheet_ranges['C{0}'.format(row_num)].value
            if c_cell_val and c_cell_val != '':
                cell_arr = b_cell_val.split(',')
                c_iud = cell_arr[0].strip().strip('t')
                priv_mask = cell_arr[1].strip().strip('t')
                t_name_arr = c_cell_val.strip().split(',')
                u_uid = '{0}{1}'.format(p_uid, c_iud)
            post_data = {
                'name': [t_name_arr[0]],
                'slug': [t_name_arr[1]],
                'order': [order_index],
                'uid': [u_uid],
                'priv_mask': [priv_mask],
            }
            print(post_data)
            mappcat.insert_data(u_uid, post_data)
            order_index = order_index + 1


if __name__ == '__main__':
    uu()
