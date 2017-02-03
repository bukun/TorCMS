# -*- coding:utf-8 -*-

import time
from torcms.core import tools
from torcms.model.core_tab import g_User2Reply
from torcms.model.core_tab import g_Reply
from torcms.model.abc_model import Mabc


class MReply2User(Mabc):
    def __init__(self):

        self.tab = g_User2Reply
        try:
            g_User2Reply.create_table()
        except:
            pass

    def update(self, uid, post_data, update_time=False):
        pass
        # cnt_html = tools.markdown2html(post_data['cnt_md'][0])
        #
        # entry = CabVoter2Reply.update(
        #     title=post_data['title'][0],
        #     date=datetime.datetime.now(),
        #     cnt_html=cnt_html,
        #     user_name=post_data['user_name'],
        #     cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
        #     time_update=time.time(),
        #     logo=post_data['logo'][0],
        #     keywords=post_data['keywords'][0],
        #     src_type=post_data['src_type'][0] if ('src_type' in post_data) else 0
        # ).where(CabVoter2Reply.uid == uid)
        #
        # entry.execute()

    def create_wiki_history(self, user_id, reply_id):

        record = g_User2Reply.select().where(
            (g_User2Reply.reply_id == reply_id) & (g_User2Reply.user_id == user_id))

        print('reply_voter_count', user_id, record.count())
        if record.count() > 0:
            # return g_Voter2Reply.select().where(g_Voter2Reply.reply_id == reply_id).count()
            # return (False)
            pass
        else:
            g_User2Reply.create(
                uid=tools.get_uuid(),
                reply_id=reply_id,
                user_id=user_id,
                timestamp=time.time(),
            )

    def get_voter_count(self, reply_id):
        return g_User2Reply.select().where(g_User2Reply.reply_id == reply_id).count()

    def delete(self, del_id):
        try:
            del_count2 = g_User2Reply.delete().where(g_User2Reply.reply_id == del_id)
            del_count2.execute()

            del_count = g_Reply.delete().where(g_Reply.uid == del_id)
            del_count.execute()

            return True
        except:

            return False

