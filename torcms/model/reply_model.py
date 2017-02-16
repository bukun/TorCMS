# -*- coding:utf-8 -*-


import datetime
import tornado.escape
from torcms.core import tools
from torcms.model.core_tab import g_Reply
from torcms.model.core_tab import g_User2Reply

from torcms.model.abc_model import Mabc


class MReply(Mabc):
    def __init__(self):
        super(MReply, self).__init__()

    @staticmethod
    def get_by_uid(uid):
        recs = g_Reply.select().where(g_Reply.uid == uid)
        if recs.count() == 0:
            return None
        else:
            return recs.get()

    @staticmethod
    def update_vote(reply_id, count):
        entry = g_Reply.update(
            vote=count
        ).where(g_Reply.uid == reply_id)
        entry.execute()

    @staticmethod
    def create_wiki_history(post_data):
        uid = tools.get_uuid()

        g_Reply.create(
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
        return g_Reply.select().where(
            g_Reply.post_id == postid
        ).order_by(g_Reply.timestamp.desc())

    @staticmethod
    def get_by_zan(reply_id):
        return g_User2Reply.select().where(g_User2Reply.reply_id == reply_id).count()

    @staticmethod
    def query_all():
        return g_Reply.select().order_by(g_Reply.timestamp.desc())
