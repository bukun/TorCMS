# -*- coding:utf-8 -*-

'''
For label, and label to post
'''

from torcms.core import tools
from torcms.core.tools import logger
from torcms.model.core_tab import TabTag
from torcms.model.core_tab import TabPost
from torcms.model.core_tab import TabPost2Tag
from torcms.model.abc_model import Mabc, MHelper
from config import CMS_CFG


class MLabel(Mabc):
    '''
    For Label
    '''

    @staticmethod
    def get_id_by_name(tag_name, kind='z'):
        '''
        Get ID by tag_name of the label.
        '''
        recs = TabTag.select().where(
            (TabTag.name == tag_name) & (TabTag.kind == kind)
        )
        logger.info('tag count of {0}: {1} '.format(tag_name, recs.count()))
        # the_id = ''
        if recs.count() == 1:
            the_id = recs.get().uid
        elif recs.count() > 1:
            rec0 = None
            for rec in recs:
                # Only keep one.
                if rec0:
                    TabPost2Tag.delete().where(TabPost2Tag.tag_id == rec.uid).execute()
                    TabTag.delete().where(TabTag.uid == rec.uid).execute()
                else:
                    rec0 = rec

            the_id = rec0.uid
        else:
            the_id = MLabel.create_tag(tag_name)
        return the_id

    @staticmethod
    def delete(uid):
        return MHelper.delete(TabTag, uid)

    @staticmethod
    def get_by_slug(tag_slug):
        '''
        Get label by slug.
        '''
        label_recs = TabTag.select().where(TabTag.slug == tag_slug)
        return label_recs.get() if label_recs else False

    @staticmethod
    def create_tag(tag_name, kind='z'):
        '''
        Create tag record by tag_name
        '''
        cur_recs = TabTag.select().where(
            (TabTag.name == tag_name) &
            (TabTag.kind == kind)
        )
        if cur_recs.count():
            uid = cur_recs.get().uid

            # TabTag.delete().where(
            #     (TabTag.name == tag_name) &
            #     (TabTag.kind == kind)
            # ).execute()
        else:
            uid = tools.get_uu4d_v2()  # Label with the ID of v2.
            while TabTag.select().where(TabTag.uid == uid).count() > 0:
                uid = tools.get_uu4d_v2()

            TabTag.create(
                uid=uid,
                slug=uid,
                name=tag_name,
                order=1,
                count=0,
                kind='z',
                tmpl=9,
                pid='zzzz',
            )
        return uid

    @staticmethod
    def create_tag_with_uid(uid, tag_name):

        if TabTag.select().where(TabTag.uid == uid).count():
            return False

        TabTag.create(
            uid=uid,
            slug=uid,
            name=tag_name,
            order=1,
            count=0,
            kind='z',
            tmpl=9,
            pid='zzzz',
        )
        return uid


class MPost2Label(Mabc):
    '''
    For post 2 label
    '''

    def __init__(self):
        super(MPost2Label, self).__init__()

    @staticmethod
    def query_count(uid):
        return TabPost2Tag.select().where(TabPost2Tag.tag_id == uid).count()

    @staticmethod
    def remove_relation(post_id, tag_id):
        '''
        Remove the relation of post and label.
        '''
        entry = TabPost2Tag.delete().where(
            (TabPost2Tag.post_id == post_id) & (TabPost2Tag.tag_id == tag_id)
        )
        entry.execute()

    @staticmethod
    def generate_catalog_list(signature):
        tag_infos = MPost2Label.get_by_uid(signature)
        out_str = ''
        for tag_info in tag_infos:
            tmp_str = '<li><a href="/tag/{0}" >{1}</a></li>'.format(
                tag_info.tag,
                tag_info.catalog_name
            )
            out_str += tmp_str
        return out_str

    @staticmethod
    def get_by_uid(post_id):
        '''
        Get records by post id.
        '''
        return TabPost2Tag.select(
            TabPost2Tag,
            TabTag.name.alias('tag_name'),
            TabTag.uid.alias('tag_uid')
        ).join(
            TabTag, on=(TabPost2Tag.tag_id == TabTag.uid)
        ).where(
            (TabPost2Tag.post_id == post_id) & (TabTag.kind == 'z')
        )

    @staticmethod
    def get_by_info(post_id, catalog_id):
        tmp_recs = TabPost2Tag.select().join(
            TabTag, on=(TabPost2Tag.tag_id == TabTag.uid)
        ).where(
            (TabPost2Tag.post_id == post_id) &
            (TabPost2Tag.tag_id == catalog_id) &
            (TabTag.kind == 'z')
        )

        if tmp_recs.count() > 1:
            '''
            Remove the rests if the count greater than 1.
            '''
            out_rec = None
            for tmp_rec in tmp_recs:
                if out_rec:
                    entry = TabPost2Tag.delete().where(TabPost2Tag.uid == tmp_rec.uid)
                    entry.execute()
                else:
                    out_rec = tmp_rec

        elif tmp_recs.count() == 1:
            out_rec = tmp_recs.get()
        else:
            out_rec = None
        return out_rec

    @staticmethod
    def add_record(post_id, tag_name, order=1, kind='z'):
        '''
        Add the record.
        '''
        logger.info('Add label kind: {0}'.format(kind))
        tag_id = MLabel.get_id_by_name(tag_name, 'z')
        labelinfo = MPost2Label.get_by_info(post_id, tag_id)
        if labelinfo:
            entry = TabPost2Tag.update(
                order=order,
            ).where(TabPost2Tag.uid == labelinfo.uid)
            entry.execute()
        else:
            entry = TabPost2Tag.create(
                uid=tools.get_uuid(),
                post_id=post_id,
                tag_id=tag_id,
                order=order,
                kind='z')
            return entry.uid

    @staticmethod
    def total_number(slug, kind='1'):
        '''
        Return the number of certian slug.
        '''
        return TabPost.select().join(
            TabPost2Tag,
            on=(TabPost.uid == TabPost2Tag.post_id)
        ).where(
            (TabPost2Tag.tag_id == slug) & (TabPost.kind == kind)
        ).count()

    @staticmethod
    def query_pager_by_slug(slug, kind='1', current_page_num=1):
        '''
        Query pager
        '''
        return TabPost.select().join(
            TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)
        ).where(
            (TabPost2Tag.tag_id == slug) &
            (TabPost.kind == kind)
        ).paginate(current_page_num, CMS_CFG['list_num'])
