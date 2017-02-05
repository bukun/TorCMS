# -*- coding:utf-8 -*-

'''
Handle the usage of the info.
'''

import time

import peewee
from torcms.model.post2catalog_model import MPost2Catalog as MInfor2Catalog
from torcms.model.core_tab import g_Usage
from torcms.core import tools
from torcms.core.tools import logger
from torcms.model.abc_model import Mabc

class MUsage(Mabc):
    '''
    Handle the usage of the info.
    '''

    def __init__(self):
        try:
            g_Usage.create_table()
        except:
            pass

    @staticmethod
    def get_all():
        return g_Usage.select().order_by('view_count')

    @staticmethod
    def query_random():
        return g_Usage.select().order_by(peewee.fn.Random()).limit(6)

    @staticmethod
    def query_recent( user_id, kind, num = 10 ):
        return g_Usage.select().where(
            (g_Usage.user_id == user_id) &
            (g_Usage.kind == kind)
        ).order_by(
            g_Usage.timestamp.desc()
        ).limit(num)

    @staticmethod
    def query_recent_by_cat( user_id, cat_id, num):
        return g_Usage.select().where(
            (g_Usage.tag_id == cat_id) &
            (g_Usage.user_id == user_id)
        ).order_by(
            g_Usage.timestamp.desc()
        ).limit(num)

    @staticmethod
    def query_most( user_id, kind, num):
        return g_Usage.select().where(
            (g_Usage.user_id == user_id) &
            (g_Usage.kind == kind)
        ).order_by(
            g_Usage.count.desc()
        ).limit(num)

    @staticmethod
    def query_by_signature( user_id, sig):
        return g_Usage.select().where(
            (g_Usage.post == sig) &
            (g_Usage.user_id == user_id)
        )

    @staticmethod
    def count_increate( rec, cat_id, num):
        entry = g_Usage.update(
            timestamp=int(time.time()),
            count=num + 1,
            tag_id=cat_id,
        ).where(g_Usage.uid == rec)
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
        print('=xx' * 20)
        for x in rec:
            print(x.uid, x.kind)

        cate_rec = MInfor2Catalog.get_entry_catalog(post_id)
        if cate_rec:
            pass
        else:
            return False
        cat_id = cate_rec.tag.uid
        if rec.count() > 0:
            logger.info('Usage update: {uid}'.format(uid = post_id))
            rec = rec.get()
            query = g_Usage.update(kind = kind).where(g_Usage.uid == rec.uid)
            query.execute()
            MUsage.count_increate(rec.uid, cat_id, rec.count)
        else:
            logger.info('Usage create: {uid}'.format(uid = post_id))
            g_Usage.create(
                uid=tools.get_uuid(),
                post=post_id,
                user_id=user_id,
                count=1,
                tag_id=cat_id,
                timestamp=int(time.time()),
                kind=kind,
            )
