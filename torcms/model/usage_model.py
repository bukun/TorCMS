# -*- coding:utf-8 -*-

'''
Handle the usage of the info.
'''

import time

import peewee
from torcms.model.infor2catalog_model import MInfor2Catalog
from torcms.model.core_tab import g_Member,  g_Usage, g_Post
from torcms.core import tools
from torcms.model.user_model import MUser


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
        return (self.tab.select().order_by('view_count'))

    def query_random(self):
        fn = peewee.fn
        return self.tab.select().order_by(fn.Random()).limit(6)

    def query_recent(self, user_id, kind, num, ):
        return self.tab.select().where((self.tab.user_id == user_id) & (self.tab.kind == kind )).order_by(
            self.tab.timestamp.desc()).limit(num)

    def query_recent_by_cat(self, user_id, cat_id, num):
        return self.tab.select().where(
            (self.tab.tag_id == cat_id) & (self.tab.user_id == user_id)).order_by(self.tab.timestamp.desc()).limit(
            num)

    def query_most(self, user_id, kind, num):
        return self.tab.select().where((self.tab.user_id == user_id) & (self.tab.kind == kind)).order_by(
            self.tab.count.desc()).limit(num)

    def get_by_signature(self, user_id, sig):
        return self.tab.select().where((self.tab.post_id == sig) & (self.tab.user_id == user_id))

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

        tt = self.get_by_signature(user_id, post_id)
        uu = self.mapp2catalog.get_entry_catalog(post_id)
        if uu:
            pass
        else:
            return False
        cat_id = uu.tag.uid
        if tt.count() > 0:
            rec = tt.get()
            self.count_increate(rec.uid, cat_id, rec.count)
        else:
            self.tab.create(
                uid=tools.get_uuid(),
                post=post_id,
                user_id=user_id,
                count=1,
                tag_id=cat_id,
                timestamp=int(time.time()),
                kind = kind,
            )


