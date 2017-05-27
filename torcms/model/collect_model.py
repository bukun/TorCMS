# -*- coding:utf-8 -*-

'''
Model for collection.
'''
import time

from torcms.core import tools
from torcms.model.core_tab import TabPost
from torcms.model.core_tab import TabCollect
from torcms.model.abc_model import Mabc
from config import CMS_CFG


class MCollect(Mabc):
    '''
    Model for collection.
    '''

    @staticmethod
    def query_recent(user_id, num=10):
        '''
        :param user_id:
        :param num:
        :return:
        '''
        return TabCollect.select(
            TabCollect, TabPost.uid.alias('post_uid'),
            TabPost.title.alias('post_title'),
            TabPost.view_count.alias('post_view_count')
        ).where(
            TabCollect.user_id == user_id
        ).join(
            TabPost, on=(TabCollect.post_id == TabPost.uid)
        ).order_by(
            TabCollect.timestamp.desc()
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
            return TabCollect.get(
                (TabCollect.user_id == user_id) &
                (TabCollect.post_id == app_id)
            )
        except:
            return None

    @staticmethod
    def count_of_user(user_id):
        return TabCollect.select(
            TabCollect, TabPost.uid.alias('post_uid'),
            TabPost.title.alias('post_title'),
            TabPost.view_count.alias('post_view_count')
        ).where(
            TabCollect.user_id == user_id
        ).join(
            TabPost, on=(TabCollect.post_id == TabPost.uid)
        ).count()

    @staticmethod
    def query_pager_by_all(user_id, current_page_num=1):

        recs = TabCollect.select(
            TabCollect, TabPost.uid.alias('post_uid'),
            TabPost.title.alias('post_title'),
            TabPost.view_count.alias('post_view_count')
        ).where(
            TabCollect.user_id == user_id
        ).join(
            TabPost, on=(TabCollect.post_id == TabPost.uid)
        ).order_by(
            TabCollect.timestamp.desc()
        ).paginate(current_page_num, CMS_CFG['list_num'])
        return recs

    @staticmethod
    def add_or_update(user_id, app_id):
        '''
        :param user_id:
        :param app_id:
        :return:
        '''

        rec = MCollect.get_by_signature(user_id, app_id)

        if rec:

            entry = TabCollect.update(
                timestamp=int(time.time())
            ).where(TabCollect.uid == rec.uid)
            entry.execute()
        else:
            TabCollect.create(
                uid=tools.get_uuid(),
                user_id=user_id,
                post_id=app_id,
                timestamp=int(time.time()),
            )
