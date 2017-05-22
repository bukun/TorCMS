# -*- coding:utf-8 -*-

import peewee

from config import CMS_CFG
from torcms.core import tools
from torcms.model.core_tab import TabTag, TabPost, TabPost2Tag
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
        entry = TabPost2Tag.delete().where(
            (TabPost2Tag.post_id == post_id) &
            (TabPost2Tag.tag_id == tag_id)
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
        entry = TabPost2Tag.delete().where(
            TabPost2Tag.tag_id == tag_id
        )
        entry.execute()

    @staticmethod
    def query_by_catid(catid):
        return TabPost2Tag.select().where(
            TabPost2Tag.tag_id == catid
        )

    @staticmethod
    def query_by_post(postid):
        '''
        Query records by post.
        :param postid:
        :return:
        '''
        return TabPost2Tag.select().where(
            TabPost2Tag.post_id == postid
        ).order_by(TabPost2Tag.order)

    @staticmethod
    def __get_by_info(post_id, catalog_id):
        recs = TabPost2Tag.select().where(
            (TabPost2Tag.post_id == post_id) &
            (TabPost2Tag.tag_id == catalog_id)
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
                    entry = TabPost2Tag.delete().where(
                        TabPost2Tag.uid == rec.uid
                    )
                    entry.execute()
                idx += idx
            return out_rec.get()

        else:
            return None

    @staticmethod
    def query_count():
        recs = TabPost2Tag.select(
            TabPost2Tag.tag_id,
            peewee.fn.COUNT(TabPost2Tag.tag_id).alias('num')
        ).group_by(
            TabPost2Tag.tag_id
        )
        return recs

    @staticmethod
    def update_field(uid, post_id=None, tag_id=None):
        if post_id:
            entry = TabPost2Tag.update(
                post_id=post_id
            ).where(TabPost2Tag.uid == uid)
            entry.execute()

        if tag_id:
            entry2 = TabPost2Tag.update(
                tag_id=tag_id
            ).where(TabPost2Tag.uid == uid)
            entry2.execute()

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
            entry = TabPost2Tag.update(
                order=order,
            ).where(TabPost2Tag.uid == rec.uid)
            entry.execute()
        else:
            TabPost2Tag.create(
                uid=tools.get_uuid(),
                post_id=post_id,
                tag_id=catalog_id,
                order=order,
            )

        MCategory.update_count(catalog_id)

    @staticmethod
    def count_of_certain_category(cat_id):
        return TabPost2Tag.select().where(
            TabPost2Tag.tag_id == cat_id
        ).count()

    @staticmethod
    def query_pager_by_slug(slug, current_page_num=1, order=False):
        if order:
            recs = TabPost.select().join(TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)).join(
                TabTag, on=(TabTag.uid == TabPost2Tag.tag_id)
            ).where(TabTag.slug == slug).order_by(TabPost.order.asc()).paginate(current_page_num, CMS_CFG['list_num'])
        else:
            recs = TabPost.select().join(TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)).join(
                TabTag, on=(TabTag.uid == TabPost2Tag.tag_id)
            ).where(
                TabTag.slug == slug
            ).order_by(
                TabPost.time_update.desc()
            ).paginate(current_page_num, CMS_CFG['list_num'])
        return recs

    @staticmethod
    def query_by_entity_uid(idd, kind=''):
        if kind == '':
            return TabPost2Tag.select(
                TabPost2Tag,
                TabTag.slug.alias('tag_slug'),
                TabTag.name.alias('tag_name')
            ).join(
                TabTag, on=(TabPost2Tag.tag_id == TabTag.uid)
            ).where(
                (TabPost2Tag.post_id == idd) &
                (TabTag.kind != 'z')
            ).order_by(
                TabPost2Tag.order
            )
        else:
            return TabPost2Tag.select(
                TabPost2Tag,
                TabTag.slug.alias('tag_slug'),
                TabTag.name.alias('tag_name')
            ).join(TabTag, on=(TabPost2Tag.tag_id == TabTag.uid)).where(
                (TabTag.kind == kind) &
                (TabPost2Tag.post_id == idd)
            ).order_by(
                TabPost2Tag.order
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
