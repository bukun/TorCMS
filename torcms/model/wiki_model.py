# -*- coding:utf-8 -*-
'''
The model for wiki.
``kind == '1'``
'''

import datetime

import peewee
import tornado.escape

from config import CMS_CFG
from torcms.core import tools
from torcms.core.tools import logger
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabWiki


class MWiki():
    '''
    Class for wiki.
    '''
    @staticmethod
    def get_counts():
        '''
        The count in table.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return TabWiki.select().count(None)

    @staticmethod
    def query_recent_edited(timstamp, kind='1'):
        return TabWiki.select().where((TabWiki.kind == kind) & (
            TabWiki.time_update > timstamp)).order_by(
                TabWiki.time_update.desc())

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''
        return MHelper.delete(TabWiki, uid)

    @staticmethod
    def get_by_uid(uid):
        '''
        Get the wiki object by the UID.
        '''
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
            # user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp()).where(TabWiki.uid == uid)
        entry.execute()

    @staticmethod
    def create_wiki(post_data):
        '''
        Create the wiki.
        '''
        logger.info('Call create wiki')

        title = post_data['title'].strip()
        # if len(title) < 2:
        #     logger.info(' ' * 4 + 'The title is too short.')
        #     return False

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
        '''
        logger.info('Call create Page')
        if MWiki.get_by_uid(slug):
            return False

        # title = post_data['title'].strip()
        # if len(title) < 2:
        #     return False
        return MWiki.__create_rec(slug, '2', post_data=post_data)

    @staticmethod
    def __create_rec(*args, **kwargs):
        '''
        Create the record.
        '''
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
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def query_dated(num=10, kind='1'):
        '''
        List the wiki of dated.
        '''
        return TabWiki.select().where(TabWiki.kind == kind).order_by(
            TabWiki.time_update.desc()).limit(num)

    @staticmethod
    def query_most(num=8, kind='1'):
        '''
        List the most viewed wiki.
        '''
        return TabWiki.select().where(TabWiki.kind == kind).order_by(
            TabWiki.view_count.desc()).limit(num)

    @staticmethod
    def update_view_count(citiao):
        '''
        view count of the wiki, plus 1. By wiki
        '''
        entry = TabWiki.update(view_count=TabWiki.view_count +
                               1).where(TabWiki.title == citiao)
        entry.execute()

    @staticmethod
    def update_view_count_by_uid(uid):
        '''
        update the count of wiki, by uid.
        '''
        entry = TabWiki.update(view_count=TabWiki.view_count +
                               1).where(TabWiki.uid == uid)
        entry.execute()

    @staticmethod
    def get_by_wiki(citiao):
        '''
        Get the wiki record by title.
        '''
        q_res = TabWiki.select().where((TabWiki.title == citiao)
                                       & (TabWiki.kind == '1'))
        the_count = q_res.count()
        if the_count == 0 or the_count > 1:
            return None
        else:
            MWiki.update_view_count(citiao)
            return q_res.get()

    @staticmethod
    def get_by_title(in_title):
        '''
        Aka get_by_wiki
        '''
        return MWiki.get_by_wiki(in_title)

    @staticmethod
    def view_count_plus(slug):
        '''
        View count plus one.
        '''
        entry = TabWiki.update(view_count=TabWiki.view_count +
                               1, ).where(TabWiki.uid == slug)
        entry.execute()

    @staticmethod
    def query_all(**kwargs):
        '''
        Qeury recent wiki.
        '''
        kind = kwargs.get('kind', '1')
        limit = kwargs.get('limit', 50)

        return TabWiki.select().where(TabWiki.kind == kind).limit(limit)

    @staticmethod
    def query_random(num=6, kind='1'):
        '''
        Query wikis randomly.
        '''
        return TabWiki.select().where(TabWiki.kind == kind).order_by(
            peewee.fn.Random()).limit(num)

    @staticmethod
    def query_recent(num=8, kind='1'):
        return TabWiki.select().where(TabWiki.kind == kind).order_by(
            TabWiki.time_update.desc()).limit(num)

    @staticmethod
    def total_number(kind):
        '''
        Return the number of certian slug.
        '''
        return TabWiki.select().where(TabWiki.kind == kind).count()

    @staticmethod
    def query_pager_by_kind(kind, current_page_num=1):
        '''
        Query pager
        '''
        return TabWiki.select().where(TabWiki.kind == kind).order_by(
            TabWiki.time_update.desc()).paginate(current_page_num,
                                                 CMS_CFG['list_num'])

    @staticmethod
    def count_of_certain_kind(kind):
        '''
        Get the count of certain kind.
        '''

        recs = TabWiki.select().where(TabWiki.kind == kind)

        return recs.count()
