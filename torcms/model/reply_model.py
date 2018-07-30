# -*- coding:utf-8 -*-

'''
Data model for reply.
'''

import datetime
import tornado.escape
from torcms.core import tools
from torcms.model.core_tab import TabReply
from torcms.model.core_tab import TabUser2Reply
from torcms.model.abc_model import Mabc
from config import CMS_CFG


class MReply(Mabc):
    # def __init__(self):
    #     super(MReply, self).__init__()

    @staticmethod
    def get_by_uid(uid):
        recs = TabReply.select().where(TabReply.uid == uid)
        if recs.count():
            return recs.get()
        return None

    @staticmethod
    def update_vote(reply_id, count):
        entry = TabReply.update(
            vote=count
        ).where(TabReply.uid == reply_id)
        entry.execute()

    @staticmethod
    def create_reply(post_data):
        '''
        Create the reply.
        '''
        uid = tools.get_uuid()
        TabReply.create(
            uid=uid,
            post_id=post_data['post_id'],
            user_name=post_data['user_name'],
            user_id=post_data['user_id'],
            timestamp=tools.timestamp(),
            date=datetime.datetime.now(),
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_reply']),
            cnt_html=tools.markdown2html(post_data['cnt_reply']),
            vote=0
        )
        return uid

    @staticmethod
    def query_by_post(postid):
        '''
        Get reply list of certain post.
        '''
        return TabReply.select().where(
            TabReply.post_id == postid
        ).order_by(TabReply.timestamp.desc())

    @staticmethod
    def get_by_zan(reply_id):
        return TabUser2Reply.select().where(TabUser2Reply.reply_id == reply_id).count()

    @staticmethod
    def query_all():
        return TabReply.select().order_by(TabReply.timestamp.desc())

    @staticmethod
    def delete(del_id):
        return TabReply.delete().where(TabReply.post_id == del_id)

    @staticmethod
    def count_of_certain():
        '''
        Get the count of certain kind.
        '''

        recs = TabReply.select()

        return recs.count()

    @staticmethod
    def total_number():
        '''
        Return the number.
        '''
        return TabReply.select().count()

    @staticmethod
    def query_pager(current_page_num=1):
        '''
        Query pager
        '''
        return TabReply.select().paginate(current_page_num, CMS_CFG['list_num'])
