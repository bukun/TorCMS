# -*- coding:utf-8 -*-
'''
Database Model for post to catalog.
'''

import peewee

from config import CMS_CFG
from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.core_tab import TabPost, TabPost2Tag, TabTag


class MPost2Catalog():
    '''
    Database Model for post to catalog.
    '''
    @staticmethod
    def just_query_all():
        '''
        Just Query all the records from TabPost2Tag.
        '''
        recs = TabPost2Tag.select()
        return recs

    @staticmethod
    def del_by_uid(uid):
        '''
        Just Query all the records from TabPost2Tag.
        '''
        entry = TabPost2Tag.delete().where(TabPost2Tag.uid == uid)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def query_all():
        '''
        Query all the records from TabPost2Tag.
        '''
        recs = TabPost2Tag.select(
            TabPost2Tag,
            TabTag.kind.alias('tag_kind'),
        ).join(TabTag, on=(TabPost2Tag.tag_id == TabTag.uid))
        return recs

    @staticmethod
    def remove_relation(post_id, tag_id):
        '''
        Delete the record of post 2 tag.
        '''
        entry = TabPost2Tag.delete().where((TabPost2Tag.post_id == post_id)
                                           & (TabPost2Tag.tag_id == tag_id))
        entry.execute()
        MCategory.update_count(tag_id)

    @staticmethod
    def remove_tag(tag_id):
        '''
        Delete the records of certain tag.
        '''
        entry = TabPost2Tag.delete().where(TabPost2Tag.tag_id == tag_id)
        entry.execute()

    @staticmethod
    def query_by_catid(catid):
        '''
        Query the records by ID of catalog.
        '''
        return TabPost2Tag.select().where(TabPost2Tag.tag_id == catid)

    @staticmethod
    def query_postinfo_by_cat(catid):

        cat_con = TabPost2Tag.tag_id == catid
        recs = TabPost.select().join(TabPost2Tag,
                                     on=((TabPost.uid == TabPost2Tag.post_id) &
                                         (TabPost.valid == 1))).where(cat_con)
        return recs

    @staticmethod
    def query_by_post(postid):
        '''
        Query records by post.
        '''
        return TabPost2Tag.select().where(
            TabPost2Tag.post_id == postid).order_by(TabPost2Tag.order)

    @staticmethod
    def __get_by_info(post_id, catalog_id):
        '''
        Geo the record by post and catalog.
        '''
        recs = TabPost2Tag.select().where((TabPost2Tag.post_id == post_id)
                                          & (TabPost2Tag.tag_id == catalog_id))

        if recs.count() == 1:
            return recs.get()
        elif recs.count() > 1:
            # return the first one, and delete others.
            out_rec = None
            for rec in recs:
                if out_rec:
                    entry = TabPost2Tag.delete().where(
                        TabPost2Tag.uid == rec.uid)
                    entry.execute()
                else:
                    out_rec = rec
            return out_rec
        return None

    @staticmethod
    def query_count():
        '''
        The count of post2tag.
        '''
        recs = TabPost2Tag.select(
            TabPost2Tag.tag_id,
            peewee.fn.COUNT(TabPost2Tag.tag_id).alias('num')).group_by(
                TabPost2Tag.tag_id)
        return recs

    @staticmethod
    def update_field(uid, post_id=None, tag_id=None, par_id=None):
        '''
        Update the field of post2tag.
        '''
        if post_id:
            entry = TabPost2Tag.update(post_id=post_id).where(
                TabPost2Tag.uid == uid)
            entry.execute()

        if tag_id:
            entry2 = TabPost2Tag.update(
                par_id=tag_id[:2] + '00',
                tag_id=tag_id,
            ).where(TabPost2Tag.uid == uid)
            entry2.execute()
        if par_id:
            entry2 = TabPost2Tag.update(par_id=par_id).where(
                TabPost2Tag.uid == uid)
            entry2.execute()

    @staticmethod
    def add_record(post_id, catalog_id, order=0):
        '''
        Create the record of post 2 tag, and update the count in g_tag.
        '''

        rec = MPost2Catalog.__get_by_info(post_id, catalog_id)
        if rec:
            entry = TabPost2Tag.update(
                order=order,
                # For migration. the value should be added when created.
                par_id=rec.tag_id[:2] + '00',
            ).where(TabPost2Tag.uid == rec.uid)
            entry.execute()
        else:
            TabPost2Tag.create(
                uid=tools.get_uuid(),
                par_id=catalog_id[:2] + '00',
                post_id=post_id,
                tag_id=catalog_id,
                order=order,
            )

        MCategory.update_count(catalog_id)

    @staticmethod
    def count_of_certain_category(cat_id, tag=''):
        '''
        Get the count of certain category.
        '''

        if cat_id.endswith('00'):
            # The first level category, using the code bellow.
            cat_con = TabPost2Tag.par_id == cat_id
        else:
            cat_con = TabPost2Tag.tag_id == cat_id


        if tag:
            condition = {'def_tag_arr': [tag]}
            recs = TabPost2Tag.select().join(
                TabPost,
                on=((TabPost2Tag.post_id == TabPost.uid) & (TabPost.valid == 1)
                    )).where(cat_con & TabPost.extinfo.contains(condition))
        else:
            recs = TabPost2Tag.select().join(
                TabPost,
                on=((TabPost2Tag.post_id == TabPost.uid) &
                    (TabPost.valid == 1))).where(cat_con)

        return recs.count()

    @staticmethod
    def query_pager_by_slug(slug, current_page_num=1, tag='', order=False):
        '''
        Query pager via category slug.
        '''
        cat_rec = MCategory.get_by_slug(slug)
        if cat_rec:
            cat_id = cat_rec.uid
        else:
            return None

        # The flowing code is valid.
        if cat_id.endswith('00'):
            # The first level category, using the code bellow.
            cat_con = TabPost2Tag.par_id == cat_id
        else:
            cat_con = TabPost2Tag.tag_id == cat_id

        if tag:
            condition = {'def_tag_arr': [tag]}
            recs = TabPost.select().join(
                TabPost2Tag,
                on=((TabPost.uid == TabPost2Tag.post_id) & (TabPost.valid == 1)
                    )).where(cat_con
                             & TabPost.extinfo.contains(condition)).order_by(
                                 TabPost.time_update.desc()).paginate(
                                     current_page_num, CMS_CFG['list_num']).distinct()
        elif order:
            recs = TabPost.select().join(
                TabPost2Tag,
                on=((TabPost.uid == TabPost2Tag.post_id) &
                    (TabPost.valid == 1))).where(cat_con).order_by(
                        TabPost.order.asc()).distinct()
        else:
            recs = TabPost.select().join(
                TabPost2Tag,
                on=((TabPost.uid == TabPost2Tag.post_id) &
                    (TabPost.valid == 1))).where(cat_con).order_by(
                        TabPost.time_update.desc()).paginate(
                            current_page_num, CMS_CFG['list_num']).distinct()

        return recs

    @staticmethod
    def query_by_entity_uid(idd, kind=''):
        '''
        Query post2tag by certain post.
        '''

        if kind == '':
            return TabPost2Tag.select(
                TabPost2Tag, TabTag.slug.alias('tag_slug'),
                TabTag.name.alias('tag_name')).join(
                    TabTag, on=(TabPost2Tag.tag_id == TabTag.uid
                                )).where((TabPost2Tag.post_id == idd)
                                         & (TabTag.kind != 'z')).order_by(
                                             TabPost2Tag.order)
        return TabPost2Tag.select(
            TabPost2Tag, TabTag.slug.alias('tag_slug'),
            TabTag.name.alias('tag_name')).join(
                TabTag, on=(TabPost2Tag.tag_id == TabTag.uid
                            )).where((TabTag.kind == kind)
                                     & (TabPost2Tag.post_id == idd)).order_by(
                                         TabPost2Tag.order)

    @staticmethod
    def query_by_id(idd):
        '''
        Alias of `query_by_entity_uid`.
        '''
        return MPost2Catalog.query_by_entity_uid(idd)

    @staticmethod
    def get_first_category(app_uid):
        '''
        Get the first, as the uniqe category of post.
        '''
        recs = MPost2Catalog.query_by_entity_uid(app_uid).objects()
        if recs.count() > 0:
            return recs.get()

        return None
