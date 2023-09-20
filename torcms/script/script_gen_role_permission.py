# -*- coding: utf-8
'''
Genereting catetory.
'''
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

        # permission 入库
        for col_idx in FILTER_COLUMNS:
            cell_val = sheet_ranges['{0}1'.format(col_idx)].value
            if cell_val and cell_val != '':
                puid = cell_val.split(":")[0]

                ppdata = {'name': cell_val.split(":")[1]}

                MPermission.add_or_update(puid, ppdata)
        role_arr = []
        for row_num in range(3, 10000):

            # role入库
            a_cell_val = sheet_ranges['A{0}'.format(row_num)].value
            b_cell_val = sheet_ranges['B{0}'.format(row_num)].value
            c_cell_val = sheet_ranges['C{0}'.format(row_num)].value
            d_cell_val = sheet_ranges['D{0}'.format(row_num)].value

            if a_cell_val and a_cell_val != '':
                cell_arr = a_cell_val.strip()
                uid = cell_arr.split(":")[0]
                name = cell_arr.split(":")[1]
                pid = '0000'
                auid = uid
                aname = name

            elif b_cell_val and b_cell_val != '':
                cell_arr = b_cell_val
                uid = cell_arr.split(":")[0]
                pid = auid
                name = aname + cell_arr.split(":")[1]
                buid = uid
                bname = name

            elif c_cell_val and c_cell_val != '':
                cell_arr = c_cell_val
                uid = cell_arr.split(":")[0]
                pid = buid
                name = bname + cell_arr.split(":")[1]
                cuid = uid
                cname = name
            elif d_cell_val and d_cell_val != '':
                cell_arr = d_cell_val
                uid = cell_arr.split(":")[0]
                pid = cuid
                name = cname + cell_arr.split(":")[1]

            else:
                continue

            post_data = {'name': name, 'uid': uid, 'pid': pid}
            role_arr.append(uid)
            MRole.add_or_update(uid, post_data)

            user_data = {
                'user_name': f'user_{uid}',
                'user_pass': 'Gg123456',
                'user_email': f'user_{uid}@qq.com',
                'role': '3333',
            }
            tt = MUser.create_user(user_data)
            if tt.get('uid'):

                role_permission_relation(uid, tt['uid'], sheet_ranges, row_num)

                # 编辑者添加权限
                create_editor_role(uid)

                cur_per = MRole2Permission.query_permission_by_role(uid)
                extinfo = {}
                extinfo['roles'] = role_arr
                for per in cur_per:
                    extinfo[f'_per_{per["uid"]}'] = 0

                MUser.update_extinfo(tt['uid'], extinfo)


def role_permission_relation(role_uid, user_uid, work_sheet, row_num):
    for col_idx in FILTER_COLUMNS:

        cell_val = work_sheet['{0}{1}'.format(col_idx, row_num)].value

        if cell_val in [1, '1']:
            cel_val = work_sheet['{0}1'.format(col_idx)].value.strip()
            per_uid = cel_val.split(":")[0]

            MRole2Permission.add_or_update(role_uid, per_uid)
            MStaff2Role.add_or_update(user_uid, role_uid)


def run_gen_role_permission(*args):
    '''
    to run
    '''
    gen_xlsx_role_permission()


def test_script():
    gen_xlsx_role_permission()


def create_editor_role(role_uid):
    per_editor = []
    per_admin = []

    per_dic_v = {
        "uid": "can_view",

        "per_data": {
            "name": "查看",
            "controller": 0,
            "action": 0
        },

    }
    per_dic_a = {
        "uid": "can_add",

        "per_data": {
            "name": "添加",
            "controller": 0,
            "action": 0
        },

    }
    per_dic_e = {
        "uid": "can_edit",

        "per_data": {
            "name": "编辑",
            "controller": 0,
            "action": 0
        },

    }
    per_dic_d = {
        "uid": "can_delete",

        "per_data": {
            "name": "删除",
            "controller": 0,
            "action": 0
        },

    }
    per_editor.append(per_dic_v)
    per_editor.append(per_dic_a)
    per_editor.append(per_dic_e)
    per_editor.append(per_dic_d)

    per_ad_r = {
        "uid": "can_review",

        "per_data": {
            "name": "复查",
            "controller": 0,
            "action": 0
        },

    }
    per_ad_v = {
        "uid": "can_verify",

        "per_data": {
            "name": "审核",
            "controller": 0,
            "action": 0
        },

    }
    per_ad_a = {
        "uid": "assign_role",

        "per_data": {
            "name": "权限",
            "controller": 0,
            "action": 0
        },

    }
    per_ad_g = {
        "uid": "assign_group",

        "per_data": {
            "name": "分组",
            "controller": 0,
            "action": 0
        },

    }
    per_admin.append(per_ad_r)
    per_admin.append(per_ad_v)
    per_admin.append(per_ad_a)
    per_admin.append(per_ad_g)

    if role_uid.endswith('editor'):
        for per_edit in per_editor:
            MPermission.add_or_update(per_edit['uid'], per_edit['per_data'])
            MRole2Permission.add_or_update('editor', per_edit['uid'])
    else:

        for per_ad in per_admin:
            MPermission.add_or_update(per_ad['uid'], per_ad['per_data'])
            MRole2Permission.add_or_update('administrators', per_ad['uid'])

if __name__ == '__main__':
    gen_xlsx_role_permission()
