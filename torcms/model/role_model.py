# -*- coding:utf-8 -*-
'''
For Roles
'''
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabRole


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
        return False