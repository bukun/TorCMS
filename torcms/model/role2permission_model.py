# -*- coding:utf-8 -*-
'''
Reply of users.
'''
import time

from torcms.core import tools
from torcms.model.core_tab import TabRole, TabPermission,TabRole2Permission



class MRole2Permission():
    @staticmethod
    def query_all():
        '''
        Return some of the records. Not all.
        '''
        return TabRole2Permission.select()

    @staticmethod
    def add_or_update(role_uid, per_id,kind_sig='1'):

        record = TabRole2Permission.select().where(
            (TabRole2Permission.role == role_uid)
            & (TabRole2Permission.permission == per_id)
        )

        if record.count() > 0:
            pass
        else:
            TabRole2Permission.create(
                role=role_uid,
                permission=per_id,
                kind=kind_sig
            )


