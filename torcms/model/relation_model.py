# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Rel
from torcms.model.core_tab import g_Post2Tag
from torcms.model.infor2catalog_model import MInfor2Catalog
import peewee


class MRelation():
    def __init__(self):
        self.tab_relation = g_Rel
        self.tab_post = g_Post
        self.tab_post2tag = g_Post2Tag
        self.minfo2tag = MInfor2Catalog()

    def add_relation(self, app_f, app_t, weight=1):
        print('=' * 20)
        print(app_f)
        print(app_t)
        cur = self.tab_relation.select().where(
            (self.tab_relation.post_f == app_f) & (self.tab_relation.post_t == app_t))
        if cur.count() > 1:
            for x in cur:
                self.delete(x.uid)

        if cur.count() == 0:
            uid = tools.get_uuid()
            entry = self.tab_relation.create(
                uid=uid,
                post_f=app_f,
                post_t=app_t,
                count=1,
            )
            return entry.uid
        elif cur.count() == 1:
            self.update_relation(app_f, app_t, weight)
        else:
            return False

    def delete(self, uid_base, uid_rel):
        entry = self.tab_relation.delete().where(
            (self.tab_relation.app_f == uid_base) & (self.tab_relation.app_t == uid_rel))
        entry.execute()

    def update_relation(self, app_f, app_t, weight=1):
        try:
            uu = self.tab_relation.get((self.tab_relation.app_f == app_f) & (self.tab_relation.app_t == app_t))
        except:
            return False
        entry = self.tab_relation.update(
            count=uu.count + weight
        ).where((self.tab_relation.app_f == app_f) & (self.tab_relation.app_t == app_t))
        entry.execute()

    def get_app_relations(self, app_id, num=20, kind='1'):
        '''
        The the related infors.
        '''
        info_tag = self.minfo2tag.get_entry_catalog(app_id)
        if info_tag:
            return self.tab_post2tag.select().join(self.tab_post).where(
                (self.tab_post2tag.tag == info_tag.tag.uid) & (self.tab_post.kind == kind)).order_by(
                peewee.fn.Random()).limit(num)
        else:
            return self.tab_post2tag.select().join(self.tab_post).where(
                self.tab_post.kind == kind).order_by(
                peewee.fn.Random()).limit(num)
