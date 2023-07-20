# -*- coding: utf-8
'''
Genereting role.
'''
import sys
from config import post_cfg
from openpyxl.reader.excel import load_workbook
from torcms.script.autocrud.base_crud import FILTER_COLUMNS
from torcms.model.role2permission_model import MRole2Permission
from torcms.model.staff2role_model import MStaff2Role
from torcms.model.permission_model import MPermission
from torcms.model.role_model import MRole
from torcms.model.user_model import MUser
from pathlib import Path

XLSX_FILE = '../../database/hlj_role.xlsx'
if Path(XLSX_FILE).exists():
    pass
else:
    XLSX_FILE = Path(__file__).parent /'hlj_role.xlsx'


def test_gen_role():
    '''
    Genereting role from xlsx file.
    '''

    for sheet_ranges in load_workbook(filename=XLSX_FILE):

        # role 入库

        cell_val = sheet_ranges['A1'].value
        if cell_val and cell_val != '':
            puid = cell_val.split(":")[0]

            ppdata = {'name': cell_val.split(":")[1], 'pid': '0000'}
            try:
                MRole.add_or_update(puid, ppdata)
            except:
                pass
            try:
                MPermission.add_or_update(puid, ppdata)
            except:
                pass
            try:
                MRole2Permission.add_or_update(puid, puid, kind_sig='z')
            except:
                pass

        role_arr = []
        for row_num in range(3, 10000):

            # role入库
            a_cell_val = sheet_ranges['A{0}'.format(row_num)].value
            b_cell_val = sheet_ranges['B{0}'.format(row_num)].value

            if a_cell_val and a_cell_val != '':
                cell_arr = a_cell_val.strip()
                uid = cell_arr.split(":")[0]
                name = cell_arr.split(":")[1]
                pid = puid
                shi_uid = uid


            elif b_cell_val and b_cell_val != '':
                cell_arr = b_cell_val
                uid = cell_arr.split(":")[0]
                pid = shi_uid
                name = cell_arr.split(":")[1]

            else:
                continue

            post_data = {'name': name, 'uid': uid, 'pid': pid}
            role_arr.append(uid)
            try:
                MRole.add_or_update(uid, post_data)
            except:
                pass
            try:
                MPermission.add_or_update(uid, post_data)
            except:
                pass
            try:
                MRole2Permission.add_or_update(uid, uid, kind_sig='z')
            except:
                pass


def select_role():
    recs = MRole.query_all()
    print("*" * 50)
    for x in recs:
        print(x.name)


if __name__ == '__main__':
    test_gen_role()
    # select_role()
