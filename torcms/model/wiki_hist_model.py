# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.core_tab import g_WikiHist
import tornado.escape
from torcms.model.abc_model import Mabc, MHelper

class MWikiHist(Mabc):
    def __init__(self):
        try:
            g_WikiHist.create_table()
        except:
            pass

    @staticmethod
    def get_last(postid):
        recs = g_WikiHist.select().where(
            g_WikiHist.wiki_id == postid
        ).order_by(g_WikiHist.time_update.desc())
        if recs.count() == 0:
            print('No old file: ', postid)
            return False
        else:
            print('Got old file.')
            return recs.get()

    @staticmethod
    def delete( uid):
        '''
        Delete by uid
        :param uid:
        :return:
        '''
        return MHelper.delete(g_WikiHist, uid)


    @staticmethod
    def get_by_uid(uid):
        return MHelper.get_by_uid(g_WikiHist, uid)

    @staticmethod
    def update_cnt(uid, post_data):
        entry = g_WikiHist.update(
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp(),
        ).where(g_WikiHist.uid == uid)
        entry.execute()

    @staticmethod
    def query_by_wikiid(postid, limit=5):
        recs = g_WikiHist.select().where(
            g_WikiHist.wiki_id == postid
        ).order_by(
            g_WikiHist.time_update.desc()
        ).limit(limit)
        return recs

    @staticmethod
    def create_wiki_history(raw_data):
        entry = g_WikiHist.create(
            uid=tools.get_uuid(),
            title=raw_data.title,
            wiki_id=raw_data.uid,
            user_name=raw_data.user_name,
            cnt_md=raw_data.cnt_md,
            time_update=raw_data.time_update,
        )
        return (entry.uid)
