# -*- coding:utf-8 -*-

'''
Handle the usage of the info.
'''

import time

import peewee
from torcms.model.post2catalog_model import MPost2Catalog as MInfor2Catalog
from torcms.model.core_tab import TabUsage, TabPost
from torcms.core import tools
from torcms.core.tools import logger
from torcms.model.abc_model import Mabc



class MUsage(Mabc):
    '''
    Handle the usage of the info.
    '''

    def __init__(self):
        super(MUsage, self).__init__()

    @staticmethod
    def query_by_post(postid):
        '''
        Query records by post.
        :param postid:
        :return:
        '''
        return TabUsage.select().where(
            TabUsage.post_id == postid
        )

    @staticmethod
    def get_all():
        return TabUsage.select().order_by('view_count')

    @staticmethod
    def query_random():
        return TabUsage.select().order_by(peewee.fn.Random()).limit(6)

    @staticmethod
    def query_recent(user_id, kind, num=10):
        return TabUsage.select(
            TabUsage, TabPost.title.alias('post_title')
        ).join(
            TabPost, on=(TabUsage.post_id == TabPost.uid)
        ).where(
            (TabUsage.user_id == user_id) &
            (TabUsage.kind == kind)
        ).order_by(
            TabUsage.timestamp.desc()
        ).limit(num)

    @staticmethod
    def query_recent_by_cat(user_id, cat_id, num):
        return TabUsage.select().where(
            (TabUsage.tag_id == cat_id) &
            (TabUsage.user_id == user_id)
        ).order_by(
            TabUsage.timestamp.desc()
        ).limit(num)

    @staticmethod
    def query_most(user_id, kind, num):
        return TabUsage.select(
            TabUsage, TabPost.title.alias('post_title')
        ).join(
            TabPost, on=(TabUsage.post_id == TabPost.uid)
        ).where(
            (TabUsage.user_id == user_id) &
            (TabUsage.kind == kind)
        ).order_by(
            TabUsage.count.desc()
        ).limit(num)

    @staticmethod
    def query_by_signature(user_id, sig):
        return TabUsage.select().where(
            (TabUsage.post_id == sig) &
            (TabUsage.user_id == user_id)
        )

    @staticmethod
    def count_increate(rec, cat_id, num):
        entry = TabUsage.update(
            timestamp=int(time.time()),
            count=num + 1,
            tag_id=cat_id,
        ).where(TabUsage.uid == rec)
        entry.execute()

    @staticmethod
    def add_or_update(user_id, post_id, kind):
        '''
        Create the record if new, else update it.
        :param user_id:
        :param post_id:
        :param kind:
        :return:
        '''

        rec = MUsage.query_by_signature(user_id, post_id)
        cate_rec = MInfor2Catalog.get_first_category(post_id)
        if cate_rec:
            cat_id = cate_rec.tag_id
        else:
            return False

        if rec.count() > 0:
            logger.info('Usage update: {uid}'.format(uid=post_id))
            rec = rec.get()
            query = TabUsage.update(kind=kind).where(TabUsage.uid == rec.uid)
            query.execute()
            MUsage.count_increate(rec.uid, cat_id, rec.count)
        else:
            logger.info('Usage create: {uid}'.format(uid=post_id))
            TabUsage.create(
                uid=tools.get_uuid(),
                post_id=post_id,
                user_id=user_id,
                count=1,
                tag_id=cat_id,
                timestamp=int(time.time()),
                kind=kind,
            )

    @staticmethod
    def update_field(uid, post_id=None):
        if post_id:
            entry = TabUsage.update(
                post_id=post_id
            ).where(TabUsage.uid == uid)
            entry.execute()

