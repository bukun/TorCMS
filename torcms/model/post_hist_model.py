# -*- coding:utf-8 -*-


from torcms.core import tools
from torcms.model.core_tab import g_PostHist
from torcms.model.supertable_model import MSuperTable
import tornado.escape

class MPostHist(MSuperTable):
    def __init__(self):
        self.tab = g_PostHist
        try:
            g_PostHist.create_table()
        except:
            pass

    def update_cnt(self, uid, post_data):
        entry = self.tab.update(
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp(),
        ).where(self.tab.uid == uid)
        entry.execute()


    def query_by_postid(self, postid, limit = 5):
        recs = self.tab.select().where(self.tab.post_id == postid).order_by(self.tab.time_update.desc()).limit(limit)
        return recs

    def get_last(self, postid):
        recs = self.tab.select().where(self.tab.post_id == postid).order_by(self.tab.time_update.desc())
        if recs.count() == 0:
            return False
        else:
            return recs.get()

    def insert_data(self, raw_data):

        uid = tools.get_uuid()
        g_PostHist.create(
            uid=uid,
            title=raw_data.title,
            post_id=raw_data.uid,
            user_name=raw_data.user_name,
            cnt_md=raw_data.cnt_md,
            time_update=raw_data.time_update,
            logo=raw_data.logo,
        )

        return True
