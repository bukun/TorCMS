# -*- coding:utf-8 -*-
from torcms.model.core_tab import g_Link
from torcms.model.abc_model import Mabc, MHelper


class MLink(Mabc):
    def __init__(self):
        try:
            g_Link.create_table()
        except:
            pass

    @staticmethod
    def get_counts():
        '''
        The count in table.
        :return:
        '''
        return g_Link.select().count()

    @staticmethod
    def query_all(limit_num=50):
        '''
        Return some of the records. Not all.
        :param limit_num:
        :return:
        '''
        return g_Link.select().limit(limit_num)

    @staticmethod
    def get_by_uid(uid):
        return MHelper.get_by_uid(g_Link, uid)

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        :param uid:
        :return:
        '''
        return MHelper.delete(g_Link, uid)

    @staticmethod
    def update(uid, post_data):
        entry = g_Link.update(
            name=post_data['name'],
            link=post_data['link'],
            order=post_data['order'],
            logo=post_data['logo'] if 'logo' in post_data else '',
        ).where(g_Link.uid == uid)
        entry.execute()

    @staticmethod
    def create_wiki_history(id_link, post_data):
        uu = MLink.get_by_uid(id_link)
        if uu:
            return (False)
        g_Link.create(
            name=post_data['name'],
            link=post_data['link'],
            order=post_data['order'],
            logo=post_data['logo'] if 'logo' in post_data else '',
            uid=id_link,
        )
        return (id_link)

    @staticmethod
    def query_link(num):
        return g_Link.select().limit(num).order_by(g_Link.order)
