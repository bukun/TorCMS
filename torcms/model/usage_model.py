# -*- coding:utf-8 -*-

'''
Handle the usage of the info.
'''

import time

import peewee
# from torcms.model.infor2catalog_model import MInfor2Catalog
from torcms.model.post2catalog_model import MPost2Catalog as MInfor2Catalog
from torcms.model.core_tab import g_Usage
from torcms.core import tools
from torcms.model.user_model import MUser
from torcms.core.tools import logger

class MUsage(object):
    '''
    Handle the usage of the info.
    '''

    def __init__(self):
        self.tab = g_Usage
        try:
            g_Usage.create_table()
        except:
            pass
        self.mapp2catalog = MInfor2Catalog()
        self.muser = MUser()

    def get_all(self):
        return self.tab.select().order_by('view_count')

    def query_random(self):
        return self.tab.select().order_by(peewee.fn.Random()).limit(6)

    def query_recent(self, user_id, kind, num = 10 ):
        return self.tab.select().where(
            (self.tab.user_id == user_id) &
            (self.tab.kind == kind)
        ).order_by(
            self.tab.timestamp.desc()
        ).limit(num)

    def query_recent_by_cat(self, user_id, cat_id, num):
        return self.tab.select().where(
            (self.tab.tag_id == cat_id) &
            (self.tab.user_id == user_id)
        ).order_by(
            self.tab.timestamp.desc()
        ).limit(num)

    def query_most(self, user_id, kind, num):
        return self.tab.select().where(
            (self.tab.user_id == user_id) &
            (self.tab.kind == kind)
        ).order_by(
            self.tab.count.desc()
        ).limit(num)

    def query_by_signature(self, user_id, sig):
        return self.tab.select().where(
            (self.tab.post == sig) &
            (self.tab.user_id == user_id)
        )

    def count_increate(self, rec, cat_id, num):
        entry = self.tab.update(
            timestamp=int(time.time()),
            count=num + 1,
            tag_id=cat_id,
        ).where(self.tab.uid == rec)
        entry.execute()

    def add_or_update(self, user_id, post_id, kind):
        '''
        Create the record if new, else update it.
        :param user_id:
        :param post_id:
        :param kind:
        :return:
        '''

        rec = self.query_by_signature(user_id, post_id)
        print('=xx' * 20)
        for x in rec:
            print(x.uid, x.kind)

        cate_rec = self.mapp2catalog.get_entry_catalog(post_id)
        if cate_rec:
            pass
        else:
            return False
        cat_id = cate_rec.tag.uid
        if rec.count() > 0:
            logger.info('Usage update: {uid}'.format(uid = post_id))
            rec = rec.get()
            query = self.tab.update(kind = kind).where(self.tab.uid == rec.uid)
            query.execute()
            self.count_increate(rec.uid, cat_id, rec.count)
        else:
            logger.info('Usage create: {uid}'.format(uid = post_id))
            self.tab.create(
                uid=tools.get_uuid(),
                post=post_id,
                user_id=user_id,
                count=1,
                tag_id=cat_id,
                timestamp=int(time.time()),
                kind=kind,
            )
