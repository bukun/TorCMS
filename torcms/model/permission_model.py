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
    def query_all(limit_num=50):
        '''
        Return some of the records. Not all.
        '''
        return TabPermission.select().limit(limit_num)

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
        entry = TabPermission.update(
            name=post_data['name'],
            controller=post_data['controller'],
            action=post_data['action'],
            pid=post_data['pid'],
            status=post_data['status'],

        ).where(TabPermission.uid == uid)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def create_link(id, post_data):
        '''
        Add record in link.
        '''
        if MPermission.get_by_uid(id):
            return False
     
        TabPermission.create(name=post_data['name'],
                       controller=post_data['controller'],
                       action=post_data['action'],
                       pid=post_data['pid'],
                       status=post_data['status'],
                       uid=id)
        return id

    @staticmethod
    def query_link():
        return TabPermission.select()
