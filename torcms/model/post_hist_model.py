# -*- coding:utf-8 -*-

'''
For Post history
'''
import tornado.escape
from torcms.core import tools
from torcms.model.core_tab import TabPostHist
from torcms.model.abc_model import Mabc, MHelper


class MPostHist(Mabc):
    '''
    For Post history
    '''

    def __init__(self):
        super(MPostHist, self).__init__()

    @staticmethod
    def get_by_uid(uid):
        '''
        return the record by uid
        :param uid:
        :return:
        '''
        return MHelper.get_by_uid(TabPostHist, uid)

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        :param uid:
        :return:
        '''

        del_count = TabPostHist.delete().where(TabPostHist.uid == uid)
        try:
            del_count.execute()
            return False
        except:
            return True

    @staticmethod
    def update_cnt(uid, post_data):
        entry = TabPostHist.update(
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp(),
        ).where(TabPostHist.uid == uid)
        entry.execute()

    @staticmethod
    def query_by_postid(postid, limit=5):
        recs = TabPostHist.select().where(
            TabPostHist.post_id == postid
        ).order_by(
            TabPostHist.time_update.desc()
        ).limit(limit)
        return recs

    @staticmethod
    def get_last(postid, limit=10):
        recs = TabPostHist.select().where(
            TabPostHist.post_id == postid
        ).order_by(TabPostHist.time_update.desc()).limit(limit)
        if recs.count() == 0:
            return None
        else:
            return recs.get()

    @staticmethod
    def create_post_history(raw_data):
        uid = tools.get_uuid()
        TabPostHist.create(
            uid=uid,
            title=raw_data.title,
            post_id=raw_data.uid,
            user_name=raw_data.user_name,
            cnt_md=raw_data.cnt_md,
            time_update=raw_data.time_update,
            logo=raw_data.logo,
        )

        return True
