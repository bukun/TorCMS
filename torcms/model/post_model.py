# -*- coding:utf-8 -*-

'''
Model for Posts.
'''
import time
import datetime
import peewee
import tornado.escape
from torcms.core import tools
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Post2Tag
from torcms.model.abc_model import Mabc, MHelper


class MPost(Mabc):
    '''
    Model for Posts.
    '''

    def __init__(self):
        try:
            g_Post.create_table()
        except:
            pass

    @staticmethod
    def query_recent_most(num=8, recent=30):
        '''
        Query the records from database that recently updated.
        :param num: the number that will returned.
        :param recent: the number of days recent.
        :return:
        '''
        time_that = int(time.time()) - recent * 24 * 3600
        return g_Post.select().where(g_Post.time_update > time_that).order_by(
            g_Post.view_count.desc()
        ).limit(num)

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        :param uid:
        :return:
        '''
        return MHelper.delete(g_Post, uid)

    @staticmethod
    def get_by_uid(uid):
        '''
        return the record by uid
        :param uid:
        :return:
        '''
        return MHelper.get_by_uid(g_Post, uid)

    @staticmethod
    def get_counts():
        '''
        The count in table.
        :return:
        '''
        return g_Post.select().count()

    @staticmethod
    def update_rating(uid, rating):
        '''
        :param uid:
        :param rating:
        :return:
        '''
        entry = g_Post.update(
            rating=rating
        ).where(g_Post.uid == uid)
        entry.execute()

    @staticmethod
    def update_kind(uid, kind):
        '''
        :param uid:
        :param kind:
        :return:
        '''
        entry = g_Post.update(
            kind=kind
        ).where(g_Post.uid == uid)
        entry.execute()

    @staticmethod
    def update_cnt(uid, post_data):
        '''
        :param uid:
        :param post_data:
        :return:
        '''

        entry = g_Post.update(
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'].strip()),
            time_update=tools.timestamp(),
        ).where(g_Post.uid == uid)
        entry.execute()

    @staticmethod
    def update(uid, post_data, update_time=False):
        '''
        :param uid:
        :param post_data:
        :param update_time:
        :return:
        '''

        title = post_data['title'].strip()
        if len(title) < 2:
            return False
        cnt_html = tools.markdown2html(post_data['cnt_md'])
        try:
            if update_time:
                entry2 = g_Post.update(
                    date=datetime.datetime.now(),
                    time_create=tools.timestamp(),
                ).where(g_Post.uid == uid)
                entry2.execute()
        except:
            pass
        cur_rec = MPost.get_by_uid(uid)

        entry = g_Post.update(
            title=title,
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'].strip()),
            cnt_html=cnt_html,
            logo=post_data['logo'],
            keywords=post_data['keywords'] if 'keywords' in post_data else '',
            kind=post_data['kind'] if 'kind' in post_data else 1,
            extinfo=post_data['extinfo'] if 'extinfo' in post_data else cur_rec.extinfo,
            time_update=tools.timestamp(),
            valid=1,
        ).where(g_Post.uid == uid)
        entry.execute()

    @staticmethod
    def add_or_update(uid, post_data):
        '''
        :param uid:
        :param post_data:
        :return:
        '''

        cur_rec = MPost.get_by_uid(uid)
        if cur_rec:
            MPost.update(uid, post_data)
        else:
            MPost.create_wiki_history(uid, post_data)

    @staticmethod
    def create_wiki_history(post_uid, post_data):
        '''
        :param post_uid:
        :param post_data:
        :return:
        '''
        title = post_data['title'].strip()
        if len(title) < 2:
            return False

        cur_rec = MPost.get_by_uid(post_uid)
        if cur_rec:
            return False

        entry = g_Post.create(
            title=title,
            date=datetime.datetime.now(),
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'].strip()),
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            uid=post_uid,
            time_create=(post_data['time_create'] if 'time_create' in post_data
                         else tools.timestamp()),
            time_update=(post_data['time_update'] if 'time_update' in post_data
                         else tools.timestamp()),
            user_name=post_data['user_name'],
            view_count=post_data['view_count'] if 'view_count' in post_data else 1,
            logo=post_data['logo'],
            keywords=post_data['keywords'] if 'keywords' in post_data else '',
            extinfo=post_data['extinfo'] if 'extinfo' in post_data else {},
            kind=post_data['kind'] if 'kind' in post_data else '1',
            valid=1,
        )
        return entry.uid

    @staticmethod
    def query_cat_random(cat_id, num=6):
        '''
        :param cat_id:
        :param num:
        :return:
        '''
        if cat_id == '':
            return g_Post.select().order_by(peewee.fn.Random()).limit(num)
            # return self.query_random(num)
        else:
            return g_Post.select().join(g_Post2Tag).where(
                g_Post2Tag.tag == cat_id
            ).order_by(
                peewee.fn.Random()
            ).limit(num)

    @staticmethod
    def query_random(num=6, kind='1'):
        '''
        Return the random records of centain kind.
        :param num:
        :param kind:
        :return:
        '''
        return g_Post.select().where(g_Post.kind == kind).order_by(peewee.fn.Random()).limit(num)

    @staticmethod
    def query_recent(num=8, kind='1'):
        '''
        :param num:
        :param kind:
        :return:
        '''
        return g_Post.select().where(
            g_Post.kind == kind
        ).order_by(
            g_Post.time_create.desc()
        ).limit(num)

    @staticmethod
    def query_all(**kwargs):
        '''
        :param kwargs:
        :return:
        '''
        if 'kind' in kwargs:
            kind = kwargs['kind']
        else:
            kind = '1'
        return g_Post.select().where(
            g_Post.kind == kind
        ).order_by(
            g_Post.time_update.desc()
        )

    @staticmethod
    def query_keywords_empty(kind='1'):
        '''
        :param kind:
        :return:
        '''
        return g_Post.select().where((g_Post.kind == kind) & (g_Post.keywords == ''))

    @staticmethod
    def query_recent_edited(timstamp, kind='1'):
        '''
        :param timstamp:
        :param kind:
        :return:
        '''
        return g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.time_update > timstamp)
        ).order_by(g_Post.time_update.desc())

    @staticmethod
    def query_dated(num=8, kind='1'):
        '''
        :param num:
        :param kind:
        :return:
        '''
        return g_Post.select().where(
            g_Post.kind == kind
        ).order_by(
            g_Post.time_update.asc()
        ).limit(num)

    @staticmethod
    def query_most_pic(num, kind='1'):
        '''
        :param num:
        :param kind:
        :return:
        '''
        return g_Post.select().where(
            (g_Post.kind == kind) & (g_Post.logo != "")
        ).order_by(g_Post.view_count.desc()).limit(num)

    @staticmethod
    def query_cat_recent(cat_id, num=8, kind='1'):
        '''
        :param cat_id:
        :param num:
        :param kind:
        :return:
        '''
        return g_Post.select().join(g_Post2Tag).where(
            (g_Post.kind == kind) &
            (g_Post2Tag.tag == cat_id)
        ).order_by(
            g_Post.time_create.desc()
        ).limit(num)

    @staticmethod
    def query_most(num=8, kind='1'):
        '''
        :param num:
        :param kind:
        :return:
        '''
        return g_Post.select().where(
            g_Post.kind == kind
        ).order_by(
            g_Post.view_count.desc()
        ).limit(num)

    @staticmethod
    def update_view_count_by_uid(uid):
        '''
        :param uid:
        :return:
        '''
        entry = g_Post.update(view_count=g_Post.view_count + 1).where(g_Post.uid == uid)
        try:
            entry.execute()
            return True
        except:
            return False

    @staticmethod
    def update_keywords(uid, inkeywords):
        '''
        :param uid:
        :param inkeywords:
        :return:
        '''
        entry = g_Post.update(keywords=inkeywords).where(g_Post.uid == uid)
        entry.execute()

    @staticmethod
    def get_next_record(in_uid, kind='1'):
        '''
        :param in_uid:
        :param kind:
        :return:
        '''
        current_rec = MPost.get_by_uid(in_uid)
        query = g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.time_create < current_rec.time_create)
        ).order_by(g_Post.time_create.desc())
        if query.count() == 0:
            return None
        else:
            return query.get()

    @staticmethod
    def get_previous_record(in_uid, kind='1'):
        '''
        :param in_uid:
        :param kind:
        :return:
        '''
        current_rec = MPost.get_by_uid(in_uid)
        query = g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.time_create > current_rec.time_create)
        ).order_by(g_Post.time_create)
        if query.count() == 0:
            return None
        else:
            return query.get()
