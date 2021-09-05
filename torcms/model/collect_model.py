# -*- coding:utf-8 -*-
'''
Model for collection.
'''
import time

from config import CMS_CFG
from torcms.core import tools
from torcms.model.core_tab import TabCollect, TabPost


class MCollect():
    '''
    Model for collection.
    '''
    @staticmethod
    def query_recent(user_id, num=10):
        '''
        Collection of recent.
        '''
        return TabCollect.select(
            TabCollect, TabPost.uid.alias('post_uid'),
            TabPost.title.alias('post_title'),
            TabPost.view_count.alias('post_view_count')).where(
                TabCollect.user_id == user_id).join(
                    TabPost, on=(TabCollect.post_id == TabPost.uid)).order_by(
                        TabCollect.timestamp.desc()).limit(num)

    #
    # def query_most(self, num):
    #     return g_Collect.select().order_by(g_Collect.count.desc()).limit(num)

    @staticmethod
    def get_by_signature(user_id, app_id):
        '''
        Get the collection.
        '''
        try:
            return TabCollect.get((TabCollect.user_id == user_id)
                                  & (TabCollect.post_id == app_id))
        except Exception as err:
            print(repr(err))
            return None

    @staticmethod
    def count_of_user(user_id):
        '''
        Get the cound of views.
        '''
        return TabCollect.select(
            TabCollect, TabPost.uid.alias('post_uid'),
            TabPost.title.alias('post_title'),
            TabPost.view_count.alias('post_view_count')).where(
                TabCollect.user_id == user_id).join(
                    TabPost, on=(TabCollect.post_id == TabPost.uid)).count()

    @staticmethod
    def query_pager_by_all(user_id, current_page_num=1):

        recs = TabCollect.select(
            TabCollect, TabPost.uid.alias('post_uid'),
            TabPost.title.alias('post_title'), TabPost.kind.alias('post_kind'),
            TabPost.view_count.alias('post_view_count')).where(
                TabCollect.user_id == user_id).join(
                    TabPost, on=(TabCollect.post_id == TabPost.uid)).order_by(
                        TabCollect.timestamp.desc()).paginate(
                            current_page_num, CMS_CFG['list_num'])
        return recs

    @staticmethod
    def add_or_update(user_id, app_id):
        '''
        Add the collection or update.
        '''

        rec = MCollect.get_by_signature(user_id, app_id)

        if rec:
            entry = TabCollect.update(timestamp=int(time.time())).where(
                TabCollect.uid == rec.uid)
            entry.execute()
        else:
            TabCollect.create(
                uid=tools.get_uuid(),
                user_id=user_id,
                post_id=app_id,
                timestamp=int(time.time()),
            )

    @staticmethod
    def remove_collect(user_id, app_id):
        '''
        Cancel collection
        '''

        rec = MCollect.get_by_signature(user_id, app_id)

        if rec:
            entry = TabCollect.delete().where(
                TabCollect.uid == rec.uid)
            entry.execute()
        else:
            return None

    @staticmethod
    def query_pager_by_userid(user_id, kind, num=10):

        recs = TabCollect.select(
            TabCollect, TabPost.uid.alias('post_uid'),
            TabPost.title.alias('post_title'), TabPost.kind.alias('post_kind'),
            TabPost.view_count.alias('post_view_count')).where(
                (TabCollect.user_id == user_id) & (TabPost.kind == kind)).join(
                    TabPost, on=(TabCollect.post_id == TabPost.uid)).order_by(
                        TabCollect.timestamp.desc()).limit(num)
        return recs
