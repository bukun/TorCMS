# -*- coding:utf-8 -*-

import peewee

from config import CMS_CFG
from torcms.core import tools
from torcms.model.core_tab import g_Tag, g_Post, g_Post2Tag
from torcms.model.abc_model import Mabc
from torcms.model.category_model import MCategory


class MPost2Catalog(Mabc):
    def __init__(self):

        super(MPost2Catalog, self).__init__()

    @staticmethod
    def remove_relation(post_id, tag_id):
        '''
        Delete the record of post 2 tag.
        :param post_id:
        :param tag_id:
        :return:
        '''
        entry = g_Post2Tag.delete().where(
            (g_Post2Tag.post_id == post_id) &
            (g_Post2Tag.tag_id == tag_id)
        )
        entry.execute()
        MCategory.update_count(tag_id)

    @staticmethod
    def remove_tag(tag_id):
        '''
        Delete the records of certain tag.
        :param tag_id:
        :return:
        '''
        entry = g_Post2Tag.delete().where(
            g_Post2Tag.tag_id == tag_id
        )
        entry.execute()

    @staticmethod
    def query_by_catid(catid):
        return g_Post2Tag.select().where(
            g_Post2Tag.tag_id == catid
        )

    @staticmethod
    def query_by_post(postid):
        '''
        Query records by post.
        :param postid:
        :return:
        '''
        return g_Post2Tag.select().where(
            g_Post2Tag.post_id == postid
        ).order_by(g_Post2Tag.order)

    @staticmethod
    def __get_by_info(post_id, catalog_id):
        recs = g_Post2Tag.select().where(
            (g_Post2Tag.post_id == post_id) &
            (g_Post2Tag.tag_id == catalog_id)
        )
        if recs.count() == 1:
            return recs.get()
        elif recs.count() > 1:
            # return the first one, and delete others.
            idx = 0
            out_rec = None
            for rec in recs:
                if idx == 0:
                    out_rec = rec
                else:
                    entry = g_Post2Tag.delete().where(
                        g_Post2Tag.uid == rec.uid
                    )
                    entry.execute()
                idx += idx
            return out_rec.get()

        else:
            return None

    @staticmethod
    def query_count():
        recs = g_Post2Tag.select(
            g_Post2Tag.tag_id,
            peewee.fn.COUNT(g_Post2Tag.tag_id).alias('num')
        ).group_by(
            g_Post2Tag.tag_id
        )
        return recs

    @staticmethod
    def add_record(post_id, catalog_id, order=0):
        '''
        Create the record of post 2 tag, and update the count in g_tag.
        :param post_id:
        :param catalog_id:
        :param order:
        :return:
        '''
        rec = MPost2Catalog.__get_by_info(post_id, catalog_id)
        if rec:
            entry = g_Post2Tag.update(
                order=order,
            ).where(g_Post2Tag.uid == rec.uid)
            entry.execute()
        else:
            g_Post2Tag.create(
                uid=tools.get_uuid(),
                post=post_id,
                tag=catalog_id,
                order=order,
            )

        MCategory.update_count(catalog_id)

    @staticmethod
    def count_of_certain_category(cat_id):
        return g_Post2Tag.select().where(
            g_Post2Tag.tag_id == cat_id
        ).count()

    @staticmethod
    def query_pager_by_slug(slug, current_page_num=1, order=False):
        if order:
            recs = g_Post.select().join(g_Post2Tag, on=(g_Post.uid == g_Post2Tag.post_id)).join(
                g_Tag, on=(g_Tag.uid == g_Post2Tag.tag_id)
            ).where(g_Tag.slug == slug).order_by(g_Post.order.asc())
        else:
            recs = g_Post.select().join(g_Post2Tag, on=(g_Post.uid == g_Post2Tag.post_id)).join(
                g_Tag, on=(g_Tag.uid == g_Post2Tag.tag_id)
            ).where(
                g_Tag.slug == slug
            ).order_by(
                g_Post.time_update.desc()
            ).paginate(current_page_num, CMS_CFG['list_num'])
        return recs

    @staticmethod
    def query_by_entity_uid(idd, kind=''):
        if kind == '':
            return g_Post2Tag.select(
                g_Post2Tag,
                g_Tag.slug.alias('tag_slug'),
                g_Tag.name.alias('tag_name')
            ).join(
                g_Tag, on=(g_Post2Tag.tag_id == g_Tag.uid)
            ).where(
                (g_Post2Tag.post_id == idd) &
                (g_Tag.kind != 'z')
            ).order_by(
                g_Post2Tag.order
            )
        else:
            return g_Post2Tag.select(
                g_Post2Tag,
                g_Tag.slug.alias('tag_slug'),
                g_Tag.name.alias('tag_name')
            ).join(g_Tag, on=(g_Post2Tag.tag_id == g_Tag.uid)).where(
                (g_Tag.kind == kind) &
                (g_Post2Tag.post_id == idd)
            ).order_by(
                g_Post2Tag.order
            )

    @staticmethod
    def query_by_id(idd):
        return MPost2Catalog.query_by_entity_uid(idd)

    @staticmethod
    def get_first_category(app_uid):
        '''
        Get the first, as the uniqe category of post.
        :param app_uid:
        :return:
        '''

        recs = MPost2Catalog.query_by_entity_uid(app_uid).naive()
        if recs.count() > 0:
            return recs.get()
        else:
            return None
