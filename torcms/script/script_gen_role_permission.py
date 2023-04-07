# -*- coding: utf-8
'''
Genereting catetory.
'''
import sys

from openpyxl.reader.excel import load_workbook

from torcms.script.autocrud.base_crud import FILTER_COLUMNS
from torcms.model.role2permission_model import MRole2Permission
from torcms.model.staff2role_model import MStaff2Role
from torcms.model.permission_model import MPermission
from torcms.model.role_model import MRole
from torcms.model.user_model import MUser
from pathlib import Path

XLSX_FILE = './database/role_perm.xlsx'
if Path(XLSX_FILE).exists():
    pass
else:
    XLSX_FILE = '../../database/role_perm.xlsx'


def gen_xlsx_role_permission():
    '''
    Genereting role,permission from xlsx file.
    '''

    for sheet_ranges in load_workbook(filename=XLSX_FILE):
        kind_sig = str(sheet_ranges['A1'].value).strip()
        # permission 入库
        for col_idx in FILTER_COLUMNS:
            cell_val = sheet_ranges['{0}1'.format(col_idx)].value
            if cell_val and cell_val != '':
                puid = kind_sig + cell_val.split(":")[0]

                ppdata = {'name': cell_val.split(":")[1]}

                MPermission.add_or_update(puid, ppdata)

        for row_num in range(3, 10000):

            # role入库
            a_cell_val = sheet_ranges['A{0}'.format(row_num)].value
            b_cell_val = sheet_ranges['B{0}'.format(row_num)].value
            c_cell_val = sheet_ranges['C{0}'.format(row_num)].value
            d_cell_val = sheet_ranges['D{0}'.format(row_num)].value

            if a_cell_val and a_cell_val != '':
                cell_arr = a_cell_val.strip()
                uid = kind_sig + cell_arr.split(":")[0]
                name = cell_arr.split(":")[1]
                pid = '0000'
                auid = uid
                aname = name

            elif b_cell_val and b_cell_val != '':
                cell_arr = b_cell_val
                uid = kind_sig + cell_arr.split(":")[0]
                pid = auid
                name = aname + cell_arr.split(":")[1]
                buid = uid
                bname = name

            elif c_cell_val and c_cell_val != '':
                cell_arr = c_cell_val
                uid = kind_sig + cell_arr.split(":")[0]
                pid = buid
                name = bname + cell_arr.split(":")[1]
                cuid = uid
                cname = name
            elif d_cell_val and d_cell_val != '':
                cell_arr = d_cell_val
                uid = kind_sig + cell_arr.split(":")[0]
                pid = cuid
                name = cname + cell_arr.split(":")[1]

            else:
                continue

            post_data = {'name': name, 'uid': uid, 'pid': pid}


            MRole.add_or_update(uid, post_data)
            user_data = {
                'user_name': f'user_{uid}',
                'user_pass': 'Gg123456',
                'user_email': f'user_{uid}@qq.com',
            }
            tt = MUser.create_user(user_data)
            if tt.get('uid'):
                role_permission_relation(uid, tt['uid'], sheet_ranges, row_num, kind_sig)


def role_permission_relation(role_uid, user_uid, work_sheet, row_num, kind_sig):
    for col_idx in FILTER_COLUMNS:

        cell_val = work_sheet['{0}{1}'.format(col_idx, row_num)].value

        if cell_val in [1, '1']:
            cel_val = work_sheet['{0}1'.format(col_idx)].value.strip()
            per_uid = kind_sig + cel_val.split(":")[0]

            MRole2Permission.add_or_update(role_uid, per_uid, kind_sig=kind_sig)
            MStaff2Role.add_or_update(user_uid, role_uid)


def run_gen_role_permission(*args):
    '''
    to run
    '''
    gen_xlsx_role_permission()


def test_script():
    gen_xlsx_role_permission()


if __name__ == '__main__':
    gen_xlsx_role_permission()
