# -*- coding:utf-8 -*-
'''
For Post history
'''
import tornado.escape

from torcms.core import tools
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabPostHist


class MPostHist():
    '''
    For Post history
    '''
    @staticmethod
    def get_by_uid(uid):
        '''
        return the record by uid
        '''
        return MHelper.get_by_uid(TabPostHist, uid)

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''

        del_count = TabPostHist.delete().where(TabPostHist.uid == uid)
        try:
            del_count.execute()
            return False
        except Exception as err:
            print(repr(err))
            return True

    @staticmethod
    def update_cnt(uid, post_data):
        '''
        Update the content by ID.
        '''
        entry = TabPostHist.update(
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp(),
        ).where(TabPostHist.uid == uid)
        entry.execute()

    @staticmethod
    def query_by_postid(postid, limit=5):
        '''
        Query history of certian records.
        '''
        recs = TabPostHist.select().where(
            TabPostHist.post_id == postid).order_by(
                TabPostHist.time_update.desc()).limit(limit)
        return recs

    @staticmethod
    def get_last(postid, limit=10):
        '''
        Get the last one of the records.
        '''
        recs = TabPostHist.select().where(
            TabPostHist.post_id == postid).order_by(
                TabPostHist.time_update.desc()).limit(limit)
        if recs.count():
            return recs.get()
        return None

    @staticmethod
    def create_post_history(raw_data, user_info):
        '''
        Create the history of certain post.
        '''
        uid = tools.get_uuid()
        TabPostHist.create(
            uid=uid,
            title=raw_data.title,
            post_id=raw_data.uid,
            user_name=user_info.user_name,
            cnt_md=raw_data.cnt_md,
            time_update=tools.timestamp(),
            logo=raw_data.logo,
        )
        return True
