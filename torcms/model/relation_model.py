# -*- coding:utf-8 -*-

import peewee
from torcms.core import tools
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Rel
from torcms.model.core_tab import g_Post2Tag
from torcms.model.post2catalog_model import MPost2Catalog as MInfor2Catalog
from torcms.model.abc_model import Mabc


class MRelation(Mabc):
    def __init__(self):
        try:
            g_Rel.create_table()
        except:
            pass

    @staticmethod
    def add_relation(app_f, app_t, weight=1):

        recs = g_Rel.select().where(
            (g_Rel.post_f == app_f) &
            (g_Rel.post_t == app_t)
        )
        if recs.count() > 1:
            for record in recs:
                MRelation.delete(record.uid)

        if recs.count() == 0:
            uid = tools.get_uuid()
            entry = g_Rel.create(
                uid=uid,
                post_f=app_f,
                post_t=app_t,
                count=1,
            )
            return entry.uid
        elif recs.count() == 1:
            MRelation.update_relation(app_f, app_t, weight)
        else:
            return False

    @staticmethod
    def delete(uid):
        entry = g_Rel.delete().where(
            g_Rel.uid == uid

        )
        entry.execute()

    @staticmethod
    def update_relation(app_f, app_t, weight=1):
        try:
            postinfo = g_Rel.get(
                (g_Rel.post_f == app_f) &
                (g_Rel.post_t == app_t)
            )
        except:
            return False
        entry = g_Rel.update(
            count=postinfo.count + weight
        ).where(
            (g_Rel.post_f == app_f) &
            (g_Rel.post_t == app_t)
        )
        entry.execute()

    @staticmethod
    def get_app_relations(app_id, num=20, kind='1'):
        '''
        The the related infors.
        '''
        info_tag = MInfor2Catalog.get_entry_catalog(app_id)
        if info_tag:
            return g_Post2Tag.select().join(
                g_Post
            ).where(
                (g_Post2Tag.tag == info_tag.tag.uid) &
                (g_Post.kind == kind)
            ).order_by(
                peewee.fn.Random()
            ).limit(num)
        else:
            return g_Post2Tag.select().join(g_Post).where(
                g_Post.kind == kind
            ).order_by(peewee.fn.Random()).limit(num)
