# -*- coding:utf-8 -*-

import datetime

import tornado.escape

from torcms.core import tools
from torcms.model.core_tab import g_Wiki
from torcms.model.abc_model import Mabc
from torcms.core.tools import logger
import peewee


class MWiki(Mabc):
    def __init__(self):
        self.tab = g_Wiki
        self.kind = '1'
        try:
            self.tab.create_table()
        except:
            pass

    def query_recent_edited(self, timstamp, kind='1'):
        return self.tab.select().where(
            (self.tab.kind == kind) & (self.tab.time_update > timstamp)
        ).order_by(
            self.tab.time_update.desc()
        )

    def update_cnt(self, uid, post_data):

        entry = g_Wiki.update(
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp(),
        ).where(g_Wiki.uid == uid)
        entry.execute()

    def update(self, uid, post_data):
        title = post_data['title'].strip()
        if len(title) < 2:
            return False

        cnt_html = tools.markdown2html(post_data['cnt_md'])

        entry = self.tab.update(
            title=title,
            date=datetime.datetime.now(),
            cnt_html=cnt_html,
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp()
        ).where(self.tab.uid == uid)
        entry.execute()

    def create_wiki(self, post_data):
        logger.info('Call create wiki')

        title = post_data['title'].strip()
        if len(title) < 2:
            logger.info(' ' * 4 + 'The title is too short.')
            return False

        uu = self.get_by_wiki(title)
        if uu:
            logger.info(' ' * 4 + 'The title already exists.')
            self.update(uu.uid, post_data)
            return

        uid = '_' + tools.get_uu8d()

        return self.__create_rec(uid, '1', post_data=post_data)

    def create_wiki_history(self, slug, post_data):
        logger.info('Call create Page')
        uu = self.get_by_uid(slug)
        if uu is None:
            pass
        else:
            return False

        title = post_data['title'].strip()
        if len(title) < 2:
            return False
        return self.__create_rec(slug, '2', post_data=post_data)

    def __create_rec(self, *args, **kwargs):
        uid = args[0]
        kind = args[1]
        post_data = kwargs['post_data']

        try:
            g_Wiki.create(
                uid=uid,
                title=post_data['title'].strip(),
                date=datetime.datetime.now(),
                cnt_html=tools.markdown2html(post_data['cnt_md']),
                time_create=tools.timestamp(),
                user_name=post_data['user_name'],
                cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
                time_update=tools.timestamp(),
                view_count=1,
                kind=kind,  # 1 for wiki,  2 for page
            )
            return True
        except:
            return False

    def query_dated(self, num=10, kind='1'):
        return self.tab.select().where(
            self.tab.kind == kind
        ).order_by(
            self.tab.time_update.desc()
        ).limit(num)

    def query_most(self, num=8, kind='1'):
        return self.tab.select().where(
            self.tab.kind == kind
        ).order_by(
            self.tab.view_count.desc()
        ).limit(num)

    def update_view_count(self, citiao):
        entry = self.tab.update(
            view_count=self.tab.view_count + 1
        ).where(
            self.tab.title == citiao
        )
        entry.execute()

    def update_view_count_by_uid(self, uid):
        entry = self.tab.update(
            view_count=self.tab.view_count + 1
        ).where(
            self.tab.uid == uid
        )
        entry.execute()

    def get_by_wiki(self, citiao):
        q_res = self.tab.select().where(self.tab.title == citiao)
        tt = q_res.count()
        if tt == 0 or tt > 1:
            return None
        else:
            self.update_view_count(citiao)
            return q_res.get()

    def get_by_title(self, in_title):
        # Aka get_by_wiki
        return self.get_by_wiki(in_title)

    def view_count_plus(self, slug):
        entry = g_Wiki.update(
            view_count=g_Wiki.view_count + 1,
        ).where(g_Wiki.uid == slug)
        entry.execute()

    def query_all(self, **kwargs):
        if 'kind' in kwargs:
            kind = kwargs['kind']
        else:
            kind = '1'
        if 'limit' in kwargs:
            limit = kwargs['limit']
        else:
            limit = 999999
        return self.tab.select().where(self.tab.kind == kind).limit(limit)

    def query_random(self, num=6):
        return self.tab.select().where(
            self.tab.kind == self.kind
        ).order_by(
            peewee.fn.Random()
        ).limit(num)

    def query_recent(self, num=8):
        return self.tab.select().where(
            self.tab.kind == self.kind
        ).order_by(
            self.tab.time_update
        ).limit(num)
