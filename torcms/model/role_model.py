# -*- coding:utf-8 -*-
'''
For Roles
'''
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabRole
from torcms.core import tools
from torcms.model.role2permission_model import MRole2Permission
from torcms.model.staff2role_model import MStaff2Role


class MRole:
    '''
    For friends links.
    '''

    @staticmethod
    def get_counts():
        '''
        The count in table.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return TabRole.select().count(None)

    @staticmethod
    def query_all_pager(current_page_num, perPage):
        '''
        Return some of the records. Not all.
        '''
        return (
            TabRole.select()
            .where(TabRole.pid == '0000')
            .order_by(TabRole.time_create.desc())
            .paginate(current_page_num, perPage)
        )

    @staticmethod
    def query_all():
        '''
        Return some of the records. Not all.
        '''
        return TabRole.select()

    @staticmethod
    def get_by_uid(uid):
        '''
        Get a link by ID.
        '''
        return MHelper.get_by_uid(TabRole, uid)

    @staticmethod
    def get_by_pid(pid):

        recs = TabRole.select().where(TabRole.pid == pid)

        return recs

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''
        per_recs = MRole2Permission.query_by_role(uid)
        for role_rec in per_recs:
            MRole2Permission.remove_relation(uid, role_rec.permission)

        staff_recs = MStaff2Role.query_by_role(uid)
        for staff_rec in staff_recs:
            MStaff2Role.remove_relation(staff_rec.staff, uid)

        return MHelper.delete(TabRole, uid)

    @staticmethod
    def update(uid, post_data):
        '''
        Updat the link.
        '''
        raw_rec = TabRole.get(TabRole.uid == uid)
        entry = TabRole.update(
            name=post_data.get('name', raw_rec.name),
            pid=post_data.get('pid', raw_rec.pid),
            status=post_data.get('status', 0),
            time_create=tools.timestamp(),
            time_update=tools.timestamp(),
        ).where(TabRole.uid == uid)
        entry.execute()
        return uid

    @staticmethod
    def add_or_update(uid, post_data):
        '''
        Add or update the data by the given ID of post.
        '''
        catinfo = MRole.get_by_uid(uid)
        if catinfo:
            MRole.update(uid, post_data)
        else:
            TabRole.create(
                uid=uid,
                name=post_data['name'],
                pid=post_data['pid'],
                status=post_data.get('status', 0),
                time_create=tools.timestamp(),
                time_update=tools.timestamp(),
            )
        return uid
