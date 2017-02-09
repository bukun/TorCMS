# -*- coding:utf-8 -*-

'''
Model for collection.
'''
import time

from torcms.core import tools
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Collect
from torcms.model.abc_model import Mabc


class MCollect(Mabc):
    '''
    Model for collection.
    '''

    def __init__(self):
        try:
            g_Collect.create_table()
        except:
            pass

    @staticmethod
    def query_recent(user_id, num=10):
        '''
        :param user_id:
        :param num:
        :return:
        '''
        return g_Collect.select().where(
            g_Collect.user == user_id
        ).join(g_Post).order_by(
            g_Collect.timestamp.desc()
        ).limit(num)

    #
    # def query_most(self, num):
    #     return g_Collect.select().order_by(g_Collect.count.desc()).limit(num)

    @staticmethod
    def get_by_signature(user_id, app_id):
        '''
        :param user_id:
        :param app_id:
        :return:
        '''
        try:
            return g_Collect.get(
                (g_Collect.user == user_id) &
                (g_Collect.post == app_id)
            )
        except:
            return None

    @staticmethod
    def add_or_update(user_id, app_id):
        '''
        :param user_id:
        :param app_id:
        :return:
        '''

        rec = MCollect.get_by_signature(user_id, app_id)

        if rec:

            entry = g_Collect.update(
                timestamp=int(time.time())
            ).where(g_Collect.uid == rec.uid)
            entry.execute()
        else:
            g_Collect.create(
                uid=tools.get_uuid(),
                user=user_id,
                post=app_id,
                timestamp=int(time.time()),
            )
