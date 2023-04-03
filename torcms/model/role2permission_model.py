# -*- coding:utf-8 -*-
'''
Reply of users.
'''
import time
from peewee import JOIN
from torcms.core import tools
from torcms.model.core_tab import TabRole, TabPermission, TabRole2Permission


class MRole2Permission:
    @staticmethod
    def query_all():
        '''
        Return some of the records. Not all.
        '''
        return TabRole2Permission.select()

    @staticmethod
    def query_by_permission(per_id):
        '''
        Query records by permission.
        '''
        return TabRole2Permission.select().where(
            TabRole2Permission.permission == per_id
        )

    @staticmethod
    def query_permission_by_role(role_id):
        query = (
            TabRole2Permission.select(
                TabPermission.uid, TabPermission.name, TabPermission.action, TabPermission.controller
            )
            .join(TabPermission, JOIN.INNER)
            .switch(TabRole2Permission)
            .join(TabRole, JOIN.INNER)
            .where(TabRole2Permission.role == role_id)
        )
        return query.dicts()

    @staticmethod
    def query_by_role(role_id):
        '''
        Query records by role.
        '''
        return TabRole2Permission.select().where(TabRole2Permission.role == role_id)

    @staticmethod
    def remove_relation(role_id, per_id):
        '''
        Delete the record of Role 2 Permission.
        '''
        entry = TabRole2Permission.delete().where(
            (TabRole2Permission.role == role_id)
            & (TabRole2Permission.permission == per_id)
        )
        entry.execute()

    @staticmethod
    def add_or_update(role_uid, per_id, kind_sig='1'):

        record = TabRole2Permission.select().where(
            (TabRole2Permission.role == role_uid)
            & (TabRole2Permission.permission == per_id)
        )

        if record.count() > 0:
            pass
        else:
            TabRole2Permission.create(role=role_uid, permission=per_id, kind=kind_sig)
