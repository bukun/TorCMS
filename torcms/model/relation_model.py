# -*- coding:utf-8 -*-

import peewee
from torcms.core import tools
from torcms.model.core_tab import TabPost
from torcms.model.core_tab import TabRel
from torcms.model.core_tab import TabPost2Tag
from torcms.model.post2catalog_model import MPost2Catalog as MInfor2Catalog
from torcms.model.abc_model import Mabc


class MRelation(Mabc):
    def __init__(self):
        super(MRelation, self).__init__()

    @staticmethod
    def add_relation(app_f, app_t, weight=1):

        recs = TabRel.select().where(
            (TabRel.post_f_id == app_f) &
            (TabRel.post_t_id == app_t)
        )
        if recs.count() > 1:
            for record in recs:
                MRelation.delete(record.uid)

        if recs.count() == 0:
            uid = tools.get_uuid()
            entry = TabRel.create(
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
        entry = TabRel.delete().where(
            TabRel.uid == uid

        )
        entry.execute()

    @staticmethod
    def update_relation(app_f, app_t, weight=1):
        try:
            postinfo = TabRel.get(
                (TabRel.post_f_id == app_f) &
                (TabRel.post_t_id == app_t)
            )
        except:
            return False
        entry = TabRel.update(
            count=postinfo.count + weight
        ).where(
            (TabRel.post_f_id == app_f) &
            (TabRel.post_t_id == app_t)
        )
        entry.execute()

    @staticmethod
    def get_app_relations(app_id, num=20, kind='1'):
        '''
        The the related infors.
        '''
        info_tag = MInfor2Catalog.get_first_category(app_id)
        if info_tag:
            return TabPost2Tag.select(
                TabPost2Tag, TabPost.title.alias('post_title'), TabPost.valid.alias('post_valid')
            ).join(
                TabPost, on=(TabPost2Tag.post_id == TabPost.uid)
            ).where(
                (TabPost2Tag.tag_id == info_tag.tag_id) &
                (TabPost.kind == kind)
            ).order_by(
                peewee.fn.Random()
            ).limit(num)
        else:
            return TabPost2Tag.select(
                TabPost2Tag, TabPost.title.alias('post_title'), TabPost.valid.alias('post_valid')
            ).join(TabPost, on=(TabPost2Tag.post_id == TabPost.uid)).where(
                TabPost.kind == kind
            ).order_by(peewee.fn.Random()).limit(num)
