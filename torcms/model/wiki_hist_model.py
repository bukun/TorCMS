# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.core_tab import g_WikiHist
from torcms.model.supertable_model import MSuperTable
import tornado.escape


class MWikiHist(MSuperTable):
    def __init__(self):
        self.tab = g_WikiHist
        try:
            g_WikiHist.create_table()
        except:
            pass

    def get_last(self, postid):
        recs = self.tab.select().where(self.tab.wiki_id == postid).order_by(self.tab.time_update.desc())
        if recs.count() == 0:
            print('No old file: ', postid)
            return False
        else:
            print('Got old file.')
            return recs.get()

    def update_cnt(self, uid, post_data):
        entry = self.tab.update(
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp(),
        ).where(self.tab.uid == uid)
        entry.execute()

    def query_by_wikiid(self, postid, limit = 5):
        recs = self.tab.select().where(self.tab.wiki_id == postid).order_by(self.tab.time_update.desc()).limit(limit)
        return recs

    def insert_data(self, raw_data):
        entry = g_WikiHist.create(
            uid=tools.get_uuid(),
            title=raw_data.title,
            wiki_id=raw_data.uid,
            user_name=raw_data.user_name,
            cnt_md=raw_data.cnt_md,
            time_update=raw_data.time_update,
        )
        return (entry.uid)


