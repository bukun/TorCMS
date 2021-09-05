# -*- coding:utf-8 -*-

import tornado.escape

from torcms.core import tools
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabWikiHist


class MWikiHist():
    @staticmethod
    def get_last(postid):
        '''
        Get the last wiki in history.
        '''
        recs = TabWikiHist.select().where(
            TabWikiHist.wiki_id == postid).order_by(
                TabWikiHist.time_update.desc())

        return None if recs.count() == 0 else recs.get()

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''
        return MHelper.delete(TabWikiHist, uid)

    @staticmethod
    def get_by_uid(uid):
        return MHelper.get_by_uid(TabWikiHist, uid)

    @staticmethod
    def update_cnt(uid, post_data):
        entry = TabWikiHist.update(
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp(),
        ).where(TabWikiHist.uid == uid)
        entry.execute()

    @staticmethod
    def query_by_wikiid(postid, limit=5):
        recs = TabWikiHist.select().where(
            TabWikiHist.wiki_id == postid).order_by(
                TabWikiHist.time_update.desc()).limit(limit)
        return recs

    @staticmethod
    def create_wiki_history(raw_data, user_info):
        entry = TabWikiHist.create(
            uid=tools.get_uuid(),
            title=raw_data.title,
            wiki_id=raw_data.uid,
            user_name=user_info.user_name,
            cnt_md=raw_data.cnt_md,
            time_update=tools.timestamp()
        )
        return entry.uid
