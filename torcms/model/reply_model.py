# -*- coding:utf-8 -*-


import datetime

import tornado.escape

from torcms.core import tools
from torcms.model.core_tab import g_Reply
from torcms.model.core_tab import g_User2Reply
from torcms.model.supertable_model import MSuperTable


class MReply(MSuperTable):
    def __init__(self):
        self.tab = g_Reply
        try:
            g_Reply.create_table()
        except:
            pass

    def update_vote(self, reply_id, count):
        entry = g_Reply.update(
            vote=count
        ).where(g_Reply.uid == reply_id)
        entry.execute()

    def insert_data(self, post_data):
        uid = tools.get_uuid()

        g_Reply.create(
            uid=uid,
            post_id = post_data['post_id'],
            user_name=post_data['user_name'],
            user_id=post_data['user_id'],
            timestamp=tools.timestamp(),
            date=datetime.datetime.now(),
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_reply']),
            cnt_html=tools.markdown2html(post_data['cnt_reply']),
            vote=0,
        )
        return (uid)
    def query_by_post(self, postid):
        return g_Reply.select().where(g_Reply.post_id == postid).order_by(g_Reply.timestamp.desc())
    def get_by_zan(self, reply_id):
        return g_User2Reply.select().where(g_User2Reply.reply_id == reply_id).count()
    def query_all(self):
        return self.tab.select().order_by(g_Reply.timestamp.desc())
