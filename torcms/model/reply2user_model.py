# -*- coding:utf-8 -*-
'''
Reply of users.
'''
import time

from torcms.core import tools
from torcms.model.core_tab import TabReply, TabUser2Reply
from torcms.model.replyid_model import TabReplyid


class MReply2User():
    @staticmethod
    def update(uid, post_data, update_time=False):
        pass

    @staticmethod
    def create_reply(user_id, reply_id):

        record = TabUser2Reply.select().where(
            (TabUser2Reply.reply_id == reply_id)
            & (TabUser2Reply.user_id == user_id))

        if record.count() > 0:
            pass
        else:
            TabUser2Reply.create(
                uid=tools.get_uuid(),
                reply_id=reply_id,
                user_id=user_id,
                timestamp=time.time(),
            )

    @staticmethod
    def get_voter_count(reply_id):
        return TabUser2Reply.select().where(
            TabUser2Reply.reply_id == reply_id).count()

    @staticmethod
    def delete(uid):
        try:

            del_count2 = TabUser2Reply.delete().where(
                TabUser2Reply.reply_id == uid)
            del_count2.execute()

            del_count = TabReply.delete().where(TabReply.uid == uid)
            del_count.execute()

            rec = TabReplyid.select().where(TabReplyid.reply0 == uid)
            for x in rec:
                del_count3 = TabReply.delete().where(TabReply.uid == x.reply1)
                del_count3.execute()

            del_count4 = TabReplyid.delete().where(TabReplyid.reply0 == uid)
            del_count4.execute()

            return True
        except Exception as err:
            print(repr(err))
            return False
