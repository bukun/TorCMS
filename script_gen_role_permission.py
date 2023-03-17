# -*- coding: utf-8
'''
Genereting catetory.
'''

from openpyxl.reader.excel import load_workbook

from torcms.script.autocrud.base_crud import FILTER_COLUMNS
from torcms.model.role2permission_model import MRole2Permission
from torcms.model.permission_model import MPermission
from torcms.model.role_model import MRole
from torcms.model.user_model import MUser
from torcms.model.role2permission_model import MRole2Permission
from torcms.model.staff2role_model import MStaff2Role


def run_gen_category(*args):
    '''
    to run
    '''
    # recs=MPermission.query_all()
    # for rec in recs:
    #     print("*" * 50)
    #     print(rec.uid)
    #     print(rec.name)
    #     print(rec.controller)
    #     print(rec.action)
    # rec2=MRole.query_all()
    # for rec in rec2:
    #     print("*" * 50)
    #     print(rec.uid)
    #     print(rec.name)
    #     print(rec.status)
    #     print(rec.pid)
    #     print(rec.time_create)
    #     print(rec.time_update)
    # rec3 = MRole2Permission.query_all()
    # for rec in rec3:
    #     print("*" * 50)
    #     print(rec.role)
    #     print(rec.permission)
    #     print(rec.kind)

    user = MUser.query_all()

    for x in user:
        MStaff2Role.add_or_update(x.uid, '1role1')
    aa = MStaff2Role.query_all()

    for x in aa:
        print(x.staff, x.role)

    # role=MRole.query_all()
    # for r in role:
    #     print(r.uid,r.name)


if __name__ == '__main__':
    run_gen_category()
