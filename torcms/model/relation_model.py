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
        super(MRelation, self).__init__()

    @staticmethod
    def add_relation(app_f, app_t, weight=1):

        recs = g_Rel.select().where(
            (g_Rel.post_f_id == app_f) &
            (g_Rel.post_t_id == app_t)
        )
        if recs.count() > 1:
            for record in recs:
                MRelation.delete(record.uid)

        if recs.count() == 0:
            uid = tools.get_uuid()
            entry = g_Rel.create(
                uid=uid,
                post_f_id=app_f,
                post_t_id=app_t,
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
                (g_Rel.post_f_id == app_f) &
                (g_Rel.post_t_id == app_t)
            )
        except:
            return False
        entry = g_Rel.update(
            count=postinfo.count + weight
        ).where(
            (g_Rel.post_f_id == app_f) &
            (g_Rel.post_t_id == app_t)
        )
        entry.execute()

    @staticmethod
    def get_app_relations(app_id, num=20, kind='1'):
        '''
        The the related infors.
        '''
        info_tag = MInfor2Catalog.get_first_category(app_id)
        if info_tag:
            return g_Post2Tag.select(
                g_Post2Tag, g_Post.title.alias('post_title')
            ).join(
                g_Post, on=(g_Post2Tag.post_id == g_Post.uid)
            ).where(
                (g_Post2Tag.tag_id == info_tag.tag_id) &
                (g_Post.kind == kind)
            ).order_by(
                peewee.fn.Random()
            ).limit(num)
        else:
            return g_Post2Tag.select(
                g_Post2Tag, g_Post.title.alias('post_title')
            ).join(g_Post, on=(g_Post2Tag.post_id == g_Post.uid)).where(
                g_Post.kind == kind
            ).order_by(peewee.fn.Random()).limit(num)
