# -*- coding:utf-8 -*-

import datetime
import tornado.escape
from torcms.core import tools
from torcms.model.core_tab import TabWiki
from torcms.core.tools import logger
from torcms.model.abc_model import Mabc, MHelper
import peewee


class MWiki(Mabc):
    def __init__(self):

        super(MWiki, self).__init__()

    @staticmethod
    def get_counts():
        '''
        The count in table.
        :return:
        '''
        return TabWiki.select().count()

    @staticmethod
    def query_recent_edited(timstamp, kind='1'):
        return TabWiki.select().where(
            (TabWiki.kind == kind) & (TabWiki.time_update > timstamp)
        ).order_by(
            TabWiki.time_update.desc()
        )

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        :param uid:
        :return:
        '''
        return MHelper.delete(TabWiki, uid)

    @staticmethod
    def get_by_uid(uid):
        return MHelper.get_by_uid(TabWiki, uid)

    @staticmethod
    def update_cnt(uid, post_data):
        entry = TabWiki.update(
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp(),
        ).where(TabWiki.uid == uid)
        entry.execute()

    @staticmethod
    def update(uid, post_data):
        title = post_data['title'].strip()
        if len(title) < 2:
            return False

        cnt_html = tools.markdown2html(post_data['cnt_md'])

        entry = TabWiki.update(
            title=title,
            date=datetime.datetime.now(),
            cnt_html=cnt_html,
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp()
        ).where(TabWiki.uid == uid)
        entry.execute()

    @staticmethod
    def create_wiki(post_data):
        logger.info('Call create wiki')

        title = post_data['title'].strip()
        if len(title) < 2:
            logger.info(' ' * 4 + 'The title is too short.')
            return False

        the_wiki = MWiki.get_by_wiki(title)
        if the_wiki:
            logger.info(' ' * 4 + 'The title already exists.')
            MWiki.update(the_wiki.uid, post_data)
            return

        uid = '_' + tools.get_uu8d()

        return MWiki.__create_rec(uid, '1', post_data=post_data)

    @staticmethod
    def create_page(slug, post_data):
        '''
        The page would be created with slug.
        :param slug:
        :param post_data:
        :return:
        '''
        logger.info('Call create Page')
        if MWiki.get_by_uid(slug):
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
            TabWiki.create(
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
        return TabWiki.select().where(
            TabWiki.kind == kind
        ).order_by(
            TabWiki.time_update.desc()
        ).limit(num)

    @staticmethod
    def query_most(num=8, kind='1'):
        return TabWiki.select().where(
            TabWiki.kind == kind
        ).order_by(
            TabWiki.view_count.desc()
        ).limit(num)

    @staticmethod
    def update_view_count(citiao):
        entry = TabWiki.update(
            view_count=TabWiki.view_count + 1
        ).where(
            TabWiki.title == citiao
        )
        entry.execute()

    @staticmethod
    def update_view_count_by_uid(uid):
        entry = TabWiki.update(
            view_count=TabWiki.view_count + 1
        ).where(
            TabWiki.uid == uid
        )
        entry.execute()

    @staticmethod
    def get_by_wiki(citiao):
        q_res = TabWiki.select().where(TabWiki.title == citiao)
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
        entry = TabWiki.update(
            view_count=TabWiki.view_count + 1,
        ).where(TabWiki.uid == slug)
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
        return TabWiki.select().where(TabWiki.kind == kind).limit(limit)

    @staticmethod
    def query_random(num=6, kind='1'):
        return TabWiki.select().where(
            TabWiki.kind == kind
        ).order_by(
            peewee.fn.Random()
        ).limit(num)

    @staticmethod
    def query_recent(num=8, kind='1'):
        return TabWiki.select().where(
            TabWiki.kind == kind
        ).order_by(
            TabWiki.time_update
        ).limit(num)
