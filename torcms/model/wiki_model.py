# -*- coding:utf-8 -*-

import datetime
import tornado.escape
from torcms.core import tools
from torcms.model.core_tab import g_Wiki
from torcms.core.tools import logger
from torcms.model.abc_model import Mabc, MHelper
import peewee


class MWiki(Mabc):
    def __init__(self):

        try:
            g_Wiki.create_table()
        except:
            pass

    @staticmethod
    def get_counts():
        '''
        The count in table.
        :return:
        '''
        return g_Wiki.select().count()

    @staticmethod
    def query_recent_edited(timstamp, kind='1'):
        return g_Wiki.select().where(
            (g_Wiki.kind == kind) & (g_Wiki.time_update > timstamp)
        ).order_by(
            g_Wiki.time_update.desc()
        )

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        :param uid:
        :return:
        '''
        return MHelper.delete(g_Wiki, uid)

    @staticmethod
    def get_by_uid(uid):
        return  MHelper.get_by_uid(g_Wiki, uid)

    @staticmethod
    def update_cnt(uid, post_data):
        entry = g_Wiki.update(
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp(),
        ).where(g_Wiki.uid == uid)
        entry.execute()

    @staticmethod
    def update(uid, post_data):
        title = post_data['title'].strip()
        if len(title) < 2:
            return False

        cnt_html = tools.markdown2html(post_data['cnt_md'])

        entry = g_Wiki.update(
            title=title,
            date=datetime.datetime.now(),
            cnt_html=cnt_html,
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp()
        ).where(g_Wiki.uid == uid)
        entry.execute()

    @staticmethod
    def create_wiki(post_data):
        logger.info('Call create wiki')

        title = post_data['title'].strip()
        if len(title) < 2:
            logger.info(' ' * 4 + 'The title is too short.')
            return False

        uu = MWiki.get_by_wiki(title)
        if uu:
            logger.info(' ' * 4 + 'The title already exists.')
            MWiki.update(uu.uid, post_data)
            return

        uid = '_' + tools.get_uu8d()

        return MWiki.__create_rec(uid, '1', post_data=post_data)

    @staticmethod
    def create_wiki_history(slug, post_data):
        logger.info('Call create Page')
        uu = MWiki.get_by_uid(slug)
        if uu is None:
            pass
        else:
            return False

        title = post_data['title'].strip()
        if len(title) < 2:
            return False
        return MWiki.__create_rec(slug, '2', post_data=post_data)

    @staticmethod
    def __create_rec(*args, **kwargs):
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

    @staticmethod
    def query_dated(num=10, kind='1'):
        return g_Wiki.select().where(
            g_Wiki.kind == kind
        ).order_by(
            g_Wiki.time_update.desc()
        ).limit(num)

    @staticmethod
    def query_most(num=8, kind='1'):
        return g_Wiki.select().where(
            g_Wiki.kind == kind
        ).order_by(
            g_Wiki.view_count.desc()
        ).limit(num)

    @staticmethod
    def update_view_count(citiao):
        entry = g_Wiki.update(
            view_count=g_Wiki.view_count + 1
        ).where(
            g_Wiki.title == citiao
        )
        entry.execute()

    @staticmethod
    def update_view_count_by_uid(uid):
        entry = g_Wiki.update(
            view_count=g_Wiki.view_count + 1
        ).where(
            g_Wiki.uid == uid
        )
        entry.execute()

    @staticmethod
    def get_by_wiki(citiao):
        q_res = g_Wiki.select().where(g_Wiki.title == citiao)
        tt = q_res.count()
        if tt == 0 or tt > 1:
            return None
        else:
            MWiki.update_view_count(citiao)
            return q_res.get()

    @staticmethod
    def get_by_title(in_title):
        # Aka get_by_wiki
        return MWiki.get_by_wiki(in_title)

    @staticmethod
    def view_count_plus(slug):
        entry = g_Wiki.update(
            view_count=g_Wiki.view_count + 1,
        ).where(g_Wiki.uid == slug)
        entry.execute()

    @staticmethod
    def query_all(**kwargs):
        if 'kind' in kwargs:
            kind = kwargs['kind']
        else:
            kind = '1'
        if 'limit' in kwargs:
            limit = kwargs['limit']
        else:
            limit = 999999
        return g_Wiki.select().where(g_Wiki.kind == kind).limit(limit)

    @staticmethod
    def query_random(num=6, kind='1'):
        return g_Wiki.select().where(
            g_Wiki.kind == kind
        ).order_by(
            peewee.fn.Random()
        ).limit(num)

    @staticmethod
    def query_recent(num=8, kind='1'):
        return g_Wiki.select().where(
            g_Wiki.kind == kind
        ).order_by(
            g_Wiki.time_update
        ).limit(num)
