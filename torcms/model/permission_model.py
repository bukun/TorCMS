# -*- coding:utf-8 -*-
'''
For friends links.
'''
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabPermission


class MPermission():
    '''
    For friends links.
    '''

    @staticmethod
    def get_counts():
        '''
        The count in table.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return TabPermission.select().count(None)

    @staticmethod
    def query_all(current_page_num, perPage):
        '''
        Return some of the records. Not all.
        '''
        return TabPermission.select().paginate(current_page_num, perPage)

    @staticmethod
    def get_by_uid(uid):
        '''
        Get a link by ID.
        '''
        return MHelper.get_by_uid(TabPermission, uid)

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''
        return MHelper.delete(TabPermission, uid)

    @staticmethod
    def update(uid, post_data):
        '''
        Updat the link.
        '''
        raw_rec = TabPermission.get(TabPermission.uid == uid)
        entry = TabPermission.update(
            name=post_data['name'],
            controller=post_data.get('controller', raw_rec.controller),
            action=post_data.get('action', raw_rec.action)

        ).where(TabPermission.uid == uid)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def add_or_update(uid, post_data):
        '''
        Add record in permission.
        '''
        perinfo = MPermission.get_by_uid(uid)
        if perinfo:
            MPermission.update(uid, post_data)
        else:
            TabPermission.create(
                uid=uid,
                name=post_data['name'],
                controller=post_data.get('controller', '0'),
                action=post_data.get('action', '0')
            )
        return uid
