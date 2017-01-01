# -*- coding:utf-8 -*-

import datetime
import time

import tornado
import tornado.escape
from torcms.core import tools
from torcms.model.core_tab import g_Wiki
from torcms.model.supertable_model import MSuperTable
import peewee

class MPage(MSuperTable):
    def __init__(self):
        self.tab = g_Wiki
        self.kind = '2'
        try:
            g_Wiki.create_table()
        except:
            pass

    def update(self, slug, post_data):
        title = post_data['title'].strip()
        if len(title) < 2:
            return False

        entry = g_Wiki.update(
            title=title,
            date=datetime.datetime.now(),
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=time.time(),
            kind = '2',
        ).where(g_Wiki.uid == slug)
        entry.execute()

    def insert_data(self, post_data):
        title = post_data['title'].strip()
        if len(title) < 2:
            return False

        slug = post_data['slug']
        uu = self.get_by_uid(slug)
        if uu is None:
            pass
        else:
            return (False)

        try:
            g_Wiki.create(
                title=title,
                date=datetime.datetime.now(),
                uid=slug,
                cnt_html=tools.markdown2html(post_data['cnt_md']),
                time_create=time.time(),
                user_name=post_data['user_name'],
                cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
                time_update=time.time(),
                view_count=1,
                kind = '2', # 2 for page
            )
            return slug
        except:
            return ''


    def query_all(self, kind = '2'):
        return self.tab.select().where(self.tab.kind == kind)

    def view_count_plus(self, slug):
        entry = g_Wiki.update(
            view_count=g_Wiki.view_count + 1,
        ).where(g_Wiki.uid == slug)
        entry.execute()


    def query_random(self, num=6):
        return self.tab.select().where(self.tab.kind == self.kind).order_by(peewee.fn.Random()).limit(num)


    def query_recent(self, num=8):
        return self.tab.select().where(self.tab.kind == self.kind).order_by(self.tab.time_update).limit(num)