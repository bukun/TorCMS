# -*- coding:utf-8 -*-

import time
from torcms.core import tools
from torcms.model.core_tab import g_User2Reply
from torcms.model.core_tab import g_Reply
from torcms.model.abc_model import Mabc


class MReply2User(Mabc):
    def __init__(self):

        try:
            g_User2Reply.create_table()
        except:
            pass

    @staticmethod
    def update(uid, post_data, update_time=False):
        pass

    @staticmethod
    def create_wiki_history(user_id, reply_id):

        record = g_User2Reply.select().where(
            (g_User2Reply.reply_id == reply_id) & (g_User2Reply.user_id == user_id)
        )

        if record.count() > 0:
            pass
        else:
            g_User2Reply.create(
                uid=tools.get_uuid(),
                reply_id=reply_id,
                user_id=user_id,
                timestamp=time.time(),
            )

    @staticmethod
    def get_voter_count(reply_id):
        return g_User2Reply.select().where(g_User2Reply.reply_id == reply_id).count()

    @staticmethod
    def delete(uid):
        try:
            del_count2 = g_User2Reply.delete().where(g_User2Reply.reply_id == uid)
            del_count2.execute()

            del_count = g_Reply.delete().where(g_Reply.uid == uid)
            del_count.execute()

            return True
        except:

            return False
