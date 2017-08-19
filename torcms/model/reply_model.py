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


class MReply(Mabc):
    def __init__(self):
        super(MReply, self).__init__()

    @staticmethod
    def get_by_uid(uid):
        recs = TabReply.select().where(TabReply.uid == uid)
        if recs.count() == 0:
            return None
        else:
            return recs.get()

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
        :param post_data:
        :return:
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
            vote=0,
        )
        return uid

    @staticmethod
    def query_by_post(postid):
        '''
        Get reply list of certain post.
        :param postid:
        :return:
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
