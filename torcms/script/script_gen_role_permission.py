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


def create_test_role():
    per_arr = []
    aa = {'1': {'router': 'post',
                'html': '<span style="color:green;" class="glyphicon glyphicon-list-alt">[Document]</span>',
                'checker': '1', 'show': 'Document'}, '3': {'router': 'info',
                                                           'html': '<span style="color:blue;" class="glyphicon glyphicon-list-alt">[Info]</span>',
                                                           'checker': '0', 'show': 'Info'}, 'v': {'router': 'map-show',
                                                                                                  'html': '<span style="color:red;" class="glyphicon glyphicon-globe">[Map visualization]</span>',
                                                                                                  'checker': '0',
                                                                                                  'show': 'Map visualization'},
          'k': {'router': 'tutorial',
                'html': '<span style="color:blue;" class="glyphicon glyphicon-list-alt">[Tutorial]</span>',
                'checker': '0', 'show': 'Tutorial'}, 'q': {'router': 'topic',
                                                           'html': '<span style="color:blue;" class="glyphicon glyphicon-list-alt">[Topics]</span>',
                                                           'checker': '0', 'show': 'Topics'},
          's': {'router': 'app', 'html': '<span style="color:green;" class="glyphicon glyphicon-list-alt">[App]</span>',
                'checker': '0', 'show': 'App'}, 'd': {'router': 'directory',
                                                      'html': '<span style="color:blue;" class="glyphicon glyphicon-list-alt">[Directory]</span>',
                                                      'checker': '0', 'show': 'Directory'}, '9': {'router': 'data',
                                                                                                  'html': '<span style="color:blue;" class="glyphicon glyphicon-list-alt">[Data]</span>',
                                                                                                  'checker': '10',
                                                                                                  'show': 'Data'},
          'g': {'router': 'postgis',
                'html': '<span style="color:blue;" class="glyphicon glyphicon-list-alt">[postgis]</span>',
                'checker': '10', 'show': 'postgis'}, 't': {'router': 'dataset',
                                                           'html': '<span style="color:blue;" class="glyphicon glyphicon-list-alt">[Taginfo]</span>',
                                                           'checker': '10', 'show': 'Taginfo'},
          'm': {'router': 'map', 'html': '<span style="color:green;" class="glyphicon glyphicon-list-alt">[Map]</span>',
                'checker': '0', 'show': 'Map'}, '7': {'router': 'datayml',
                                                      'html': '<span style="color:blue;" class="glyphicon glyphicon-list-alt">[Datayml]</span>',
                                                      'checker': '10', 'show': 'Datayml'}}
    for kind in aa.keys():
        print("*" * 50)
        print(kind)
        per_dic_v = {
            "uid": "{0}can_view".format(kind),
            "kind": kind,
            "per_data": {
                "name": "{0}查看".format(kind),
                "controller": 1,
                "action": 1
            },

        }
        per_dic_a = {
            "uid": "{0}can_add".format(kind),
            "kind": kind,
            "per_data": {
                "name": "{0}添加".format(kind),
                "controller": 1,
                "action": 1
            },

        }
        per_dic_e = {
            "uid": "{0}can_edit".format(kind),
            "kind": kind,
            "per_data": {
                "name": "{0}编辑".format(kind),
                "controller": 1,
                "action": 1
            },

        }
        per_dic_d = {
            "uid": "{0}can_delete".format(kind),
            "kind": kind,
            "per_data": {
                "name": "{0}删除".format(kind),
                "controller": 1,
                "action": 1
            },

        }
        per_arr.append(per_dic_v)
        per_arr.append(per_dic_a)
        per_arr.append(per_dic_e)
        per_arr.append(per_dic_d)

    for per in per_arr:

        MPermission.add_or_update(per['uid'], per['per_data'])
        MRole2Permission.add_or_update('1editor', per['uid'], kind_sig=per['kind'])


if __name__ == '__main__':
    gen_xlsx_role_permission()
    create_test_role()
