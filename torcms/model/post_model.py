# -*- coding:utf-8 -*-

import datetime
import time
import peewee
import tornado.escape
import config
from torcms.core import tools
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Post2Tag
from torcms.model.supertable_model import MSuperTable


class MPost(MSuperTable):
    def __init__(self):
        self.tab = g_Post


    def update_rating(self, uid, rating):
        entry = g_Post.update(
            rating = rating
        ).where(g_Post.uid == uid)
        entry.execute()

    def update_kind(self, uid, kind):
        entry = g_Post.update(
            kind = kind
        ).where(g_Post.uid == uid)
        entry.execute()

    def update_cnt(self, uid, post_data):

        entry = g_Post.update(
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update = tools.timestamp(),
        ).where(g_Post.uid == uid)
        entry.execute()

    def update(self, uid, post_data, update_time=False):
        title = post_data['title'].strip()
        if len(title) < 2:
            return False
        cnt_html = tools.markdown2html(post_data['cnt_md'])
        try:
            if update_time:
                entry2 = g_Post.update(
                    date=datetime.datetime.now(),
                    time_create  = tools.timestamp(),
                ).where(g_Post.uid == uid)
                entry2.execute()
        except:
            pass
        cur_rec = self.get_by_id(uid)

        entry = g_Post.update(
            title=title,
            cnt_html=cnt_html,
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'].strip()),
            logo=post_data['logo'],
            keywords=post_data['keywords'] if 'keywords' in post_data else '',
            kind=post_data['kind'] if 'kind' in post_data else 1,
            extinfo=post_data['extinfo'] if 'extinfo' in post_data else cur_rec.extinfo,
            time_update= tools.timestamp(),
            valid=1,
        ).where(g_Post.uid == uid)
        entry.execute()


    def add_or_update(self, uid, post_data):

        cur_rec = self.get_by_id(uid)
        if cur_rec:
            self.update(uid, post_data)
        else:
            self.insert_data(uid, post_data)

    def insert_data(self, id_post, post_data):
        title = post_data['title'].strip()
        if len(title) < 2:
            return False

        cur_rec = self.get_by_id(id_post)
        if cur_rec:
            return (False)

        entry = g_Post.create(
            title=title,
            date=datetime.datetime.now(),
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            uid=id_post,
            time_create=post_data['time_create'] if 'time_create' in post_data else tools.timestamp(),
            time_update=post_data['time_update'] if 'time_update' in post_data else tools.timestamp(),
            user_name=post_data['user_name'],
            view_count=post_data['view_count'] if 'view_count' in post_data else 1,
            logo=post_data['logo'],
            keywords=post_data['keywords'] if 'keywords' in post_data else '',
            extinfo=post_data['extinfo'] if 'extinfo' in post_data else {},
            kind=post_data['kind'] if 'kind' in post_data else '1',
            valid=1,
        )
        return (entry.uid)

    def query_cat_random(self, cat_id, num=6):
        if cat_id == '':
            return self.query_random(num)

        return g_Post.select().join(g_Post2Tag).where(g_Post2Tag.tag == cat_id).order_by(
            peewee.fn.Random()).limit(num)


    def query_recent(self, num=8, kind='1'):
        return self.tab.select().where(self.tab.kind == kind).order_by(g_Post.time_create.desc()).limit(num)

    def query_all(self, kind='1'):
        return self.tab.select().where(self.tab.kind == kind).order_by(g_Post.time_update.desc())

    def get_num_by_cat(self, cat_str, kind='1'):
        return g_Post.select().where(
            (self.tab.kind == kind) & (g_Post.id_cats.contains(',{0},'.format(cat_str)))).count()

    def query_keywords_empty(self, kind='1'):
        return g_Post.select().where((self.tab.kind == kind) & (g_Post.keywords == ''))

    def query_recent_edited(self, timstamp, kind='1'):
        return self.tab.select().where((self.tab.kind == kind) & (g_Post.time_update > timstamp)).order_by(
            g_Post.time_update.desc())

    def query_dated(self, num=8, kind='1'):
        return g_Post.select().where(self.tab.kind == kind).order_by(g_Post.time_update.asc()).limit(num)

    def query_most_pic(self, num, kind='1'):
        return g_Post.select().where((self.tab.kind == kind) & (g_Post.logo != "")).order_by(
            g_Post.view_count.desc()).limit(num)

    def query_cat_recent(self, cat_id, num=8, kind='1'):
        return g_Post.select().join(g_Post2Tag).where((self.tab.kind == kind) & (g_Post2Tag.tag == cat_id)).order_by(
            g_Post.time_create.desc()).limit(num)

    def query_most(self, num=8, kind='1'):
        return g_Post.select().where(self.tab.kind == kind).order_by(g_Post.view_count.desc()).limit(num)

    def query_cat_by_pager(self, cat_str, cureent, kind='1'):
        tt = g_Post.select().where((self.tab.kind == kind) & (g_Post.id_cats.contains(str(cat_str)))).order_by(
            g_Post.time_create.desc()).paginate(cureent, config.page_num)
        return tt

    def update_view_count_by_uid(self, uid):
        entry = g_Post.update(view_count=g_Post.view_count + 1).where(g_Post.uid == uid)
        try:
            entry.execute()
            return True
        except:
            return False

    def update_keywords(self, uid, inkeywords):
        entry = g_Post.update(keywords=inkeywords).where(g_Post.uid == uid)
        entry.execute()

    def get_next_record(self, in_uid, kind='1'):
        current_rec = self.get_by_id(in_uid)
        query = g_Post.select().where(
            (self.tab.kind == kind) & (g_Post.time_create < current_rec.time_create)).order_by(
            g_Post.time_create.desc())
        if query.count() == 0:
            return None
        else:
            return query.get()

    def get_previous_record(self, in_uid, kind='1'):
        current_rec = self.get_by_id(in_uid)
        query = g_Post.select().where(
            (self.tab.kind == kind) & (g_Post.time_create > current_rec.time_create)).order_by(g_Post.time_create)
        if query.count() == 0:
            return None
        else:
            return query.get()
