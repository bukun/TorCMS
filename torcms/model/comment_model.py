# -*- coding:utf-8 -*-

'''
Model for Posts.
'''
from torcms.model.core_tab import TabPost
from torcms.model.core_tab import TabReply
from torcms.model.abc_model import Mabc
from config import CMS_CFG


class MComment(Mabc):
    '''
    Model for Posts.
    '''

    def __init__(self):
        super(MComment, self).__init__()

    @staticmethod
    def query_pager_by_comment(current_page_num=1):
        recs = TabPost.select().join(
            TabReply,
            on=(TabPost.uid == TabReply.post_id)
        ).distinct(TabPost.uid).paginate(current_page_num, CMS_CFG['list_num'])

        return recs

    @staticmethod
    def count_of_certain():
        recs = TabPost.select().join(
            TabReply,
            on=(TabPost.uid == TabReply.post_id)
        ).distinct(TabPost.uid)
        return recs.count()

    @staticmethod
    def count_of_comment(postid):
        recs = TabReply.select().join(
            TabPost,
            on=(TabReply.post_id == TabPost.uid)
        ).where(TabPost.uid == postid)
        return recs.count()

    @staticmethod
    def query_recent_edited(timstamp):
        '''
        获取最近有评论的Post，以时间戳为条件
        '''
        return TabPost.select().join(
            TabReply,
            on=(TabPost.uid == TabReply.post_id)
        ).where(
            (TabReply.timestamp > timstamp)
        ).distinct(TabPost.uid)
