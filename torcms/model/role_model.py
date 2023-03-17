# -*- coding:utf-8 -*-
'''
For Roles
'''
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabRole
from torcms.core import tools


class MRole():
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
    def query_all(limit_num=50):
        '''
        Return some of the records. Not all.
        '''
        return TabRole.select().limit(limit_num)

    @staticmethod
    def get_by_uid(uid):
        '''
        Get a link by ID.
        '''
        return MHelper.get_by_uid(TabRole, uid)

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''
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
                status=post_data[0],
                time_create=tools.timestamp(),
                time_update=tools.timestamp(),

            )
        return uid
