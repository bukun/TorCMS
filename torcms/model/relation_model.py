# -*- coding:utf-8 -*-

import peewee

from torcms.core import tools
from torcms.model.core_tab import TabPost, TabPost2Tag, TabRel, TabCorrelation
from torcms.model.label_model import MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog as MInfor2Catalog


class MCorrelation():
    @staticmethod
    def add_relation(postid, relid, kind, order):
        '''
        Adding relation between two posts.
        '''
        uid = tools.get_uuid()
        entry = TabCorrelation.create(
            uid=uid,
            post_id=postid,
            rel_id=relid,
            kind=kind,
            order=order,
        )
        return entry.uid

        # recs = TabRel.select().where((TabRel.post_f_id == app_f)
        #                              & (TabRel.post_t_id == app_t))
        # if recs.count() > 1:
        #     for record in recs:
        #         MRelation.delete(record.uid)
        #
        # if recs.count() == 0:
        #     uid = tools.get_uuid()
        #     entry = TabRel.create(
        #         uid=uid,
        #         post_f_id=app_f,
        #         post_t_id=app_t,
        #         count=1,
        #     )
        #     return entry.uid
        # elif recs.count() == 1:
        #     MRelation.update_relation(app_f, app_t, weight)
        # else:
        #     return False

    @staticmethod
    def delete(uid):
        entry = TabRel.delete().where(TabRel.uid == uid)
        entry.execute()

    @staticmethod
    def update_relation(app_f, app_t, weight=1):
        try:
            postinfo = TabRel.get(
                (TabRel.post_f_id == app_f) & (TabRel.post_t_id == app_t)
            )
        except Exception as err:
            print(repr(err))
            return False
        entry = TabRel.update(
            count=postinfo.count + weight
        ).where(
            (TabRel.post_f_id == app_f) & (TabRel.post_t_id == app_t)
        )
        entry.execute()

    @staticmethod
    def get_app_relations(app_id, num=10, kind=1):
        '''
        The the related infors.
        '''

        recs = TabCorrelation.select().where(
            (TabCorrelation.post_id == app_id) &
            (TabCorrelation.kind == kind)
        ).distinct(TabCorrelation.rel_id).order_by(
            TabCorrelation.rel_id
        ).limit(num)
        return recs


class MRelation():
    @staticmethod
    def add_relation(app_f, app_t, weight=1):
        '''
        Adding relation between two posts.
        '''
        recs = TabRel.select().where((TabRel.post_f_id == app_f)
                                     & (TabRel.post_t_id == app_t))
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
        entry = TabRel.delete().where(TabRel.uid == uid)
        entry.execute()

    @staticmethod
    def update_relation(app_f, app_t, weight=1):
        try:
            postinfo = TabRel.get(
                (TabRel.post_f_id == app_f) & (TabRel.post_t_id == app_t)
            )
        except Exception as err:
            print(repr(err))
            return False
        entry = TabRel.update(
            count=postinfo.count + weight
        ).where(
            (TabRel.post_f_id == app_f) & (TabRel.post_t_id == app_t)
        )
        entry.execute()

    @staticmethod
    def get_app_relations(app_id, num=20, kind='1'):
        '''
        The the related infors.
        如有标签按标签推荐，如无标签按分类推荐
        '''

        tag_info = filter(lambda x: not x.tag_name.startswith('_'),
                          MPost2Label.get_by_uid(app_id).objects())

        info_tag = MInfor2Catalog.get_first_category(app_id)

        tag_arr = []
        for tag in tag_info:
            tag_arr.append(tag.tag_uid)

        if len(tag_arr) > 0:

            recs = TabPost2Tag.select(
                TabPost2Tag, TabPost.title.alias('post_title'),
                TabPost.valid.alias('post_valid')).join(
                TabPost,
                on=(TabPost2Tag.post_id == TabPost.uid
                    )).where((TabPost2Tag.tag_id << tag_arr)
                             & (TabPost.uid != app_id)
                             & (TabPost.kind == kind)
                             & (TabPost.valid == 1)).distinct(
                TabPost2Tag.post_id).order_by(
                TabPost2Tag.post_id).limit(num)
            if recs.count() == 0:
                recs = TabPost2Tag.select(
                    TabPost2Tag,
                    TabPost.title.alias('post_title'),
                    TabPost.valid.alias('post_valid')
                ).join(
                    TabPost, on=(TabPost2Tag.post_id == TabPost.uid)
                ).where(
                    (TabPost.uid != app_id) &
                    (TabPost2Tag.tag_id == info_tag.tag_id) &
                    (TabPost.kind == kind) &
                    (TabPost.valid == 1)
                ).order_by(
                    peewee.fn.Random()
                ).limit(num)

        else:
            if info_tag:
                recs = TabPost2Tag.select(
                    TabPost2Tag,
                    TabPost.title.alias('post_title'),
                    TabPost.valid.alias('post_valid')
                ).join(
                    TabPost, on=(TabPost2Tag.post_id == TabPost.uid)
                ).where(
                    (TabPost.uid != app_id) &
                    (TabPost2Tag.tag_id == info_tag.tag_id) &
                    (TabPost.kind == kind) &
                    (TabPost.valid == 1)
                ).order_by(
                    peewee.fn.Random()
                ).limit(num)
            else:
                recs = TabPost2Tag.select(
                    TabPost2Tag,
                    TabPost.title.alias('post_title'),
                    TabPost.valid.alias('post_valid')
                ).join(
                    TabPost, on=(TabPost2Tag.post_id == TabPost.uid)
                ).where(
                    (TabPost.uid != app_id) &
                    (TabPost.kind == kind) &
                    (TabPost.valid == 1)
                ).order_by(
                    peewee.fn.Random()
                ).limit(num)
        return recs
