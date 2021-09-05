# -*- coding:utf-8 -*-
'''
For friends links.
'''
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabLink


class MLink():
    '''
    For friends links.
    '''
    @staticmethod
    def get_counts():
        '''
        The count in table.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return TabLink.select().count(None)

    @staticmethod
    def query_all(limit_num=50):
        '''
        Return some of the records. Not all.
        '''
        return TabLink.select().limit(limit_num)

    @staticmethod
    def get_by_uid(uid):
        '''
        Get a link by ID.
        '''
        return MHelper.get_by_uid(TabLink, uid)

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''
        return MHelper.delete(TabLink, uid)

    @staticmethod
    def update(uid, post_data):
        '''
        Updat the link.
        '''
        entry = TabLink.update(
            name=post_data['name'],
            link=post_data['link'],
            order=post_data['order'],
            logo=post_data['logo'] if 'logo' in post_data else '',
        ).where(TabLink.uid == uid)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def create_link(id_link, post_data):
        '''
        Add record in link.
        '''
        if MLink.get_by_uid(id_link):
            return False
        try:
            the_order = int(post_data['order'])
        except Exception as err:
            print(repr(err))
            the_order = 999
        TabLink.create(name=post_data['name'],
                       link=post_data['link'],
                       order=the_order,
                       logo=post_data['logo'] if 'logo' in post_data else '',
                       uid=id_link)
        return id_link

    @staticmethod
    def query_link(num):
        return TabLink.select().limit(num).order_by(TabLink.order)
