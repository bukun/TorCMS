# -*- coding:utf-8 -*-

'''
For friends links.
'''
from torcms.model.core_tab import TabLink
from torcms.model.abc_model import Mabc, MHelper


class MLink(Mabc):
    '''
    For friends links.
    '''

    def __init__(self):
        super(MLink, self).__init__()

    @staticmethod
    def get_counts():
        '''
        The count in table.
        :return:
        '''
        return TabLink.select().count()

    @staticmethod
    def query_all(limit_num=50):
        '''
        Return some of the records. Not all.
        :param limit_num:
        :return:
        '''
        return TabLink.select().limit(limit_num)

    @staticmethod
    def get_by_uid(uid):
        return MHelper.get_by_uid(TabLink, uid)

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        :param uid:
        :return:
        '''
        return MHelper.delete(TabLink, uid)

    @staticmethod
    def update(uid, post_data):
        '''
        Updat the link.
        :param uid:
        :param post_data:
        :return:
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
        except:
            return False

    @staticmethod
    def create_link(id_link, post_data):
        '''
        Add record in link.
        :param id_link:
        :param post_data:
        :return:
        '''
        if MLink.get_by_uid(id_link):
            return False
        TabLink.create(name=post_data['name'],
                       link=post_data['link'],
                       order=post_data['order'],
                       logo=post_data['logo'] if 'logo' in post_data else '',
                       uid=id_link)
        return id_link

    @staticmethod
    def query_link(num):
        return TabLink.select().limit(num).order_by(TabLink.order)
