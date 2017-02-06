# -*- coding:utf-8 -*-

'''
For label, and label to post
'''

from torcms.core import tools
from torcms.model.core_tab import g_Tag
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Post2Tag as g_Post2Tag
from torcms.core.tools import logger

from config import CMS_CFG
from torcms.model.abc_model import Mabc, MHelper


class MLabel(Mabc):
    '''
    For Label
    '''

    @staticmethod
    def get_id_by_name(tag_name, kind='z'):
        recs = g_Tag.select().where(
            (g_Tag.name == tag_name) & (g_Tag.kind == kind)
        )
        logger.info('tag count of {0}: {1} '.format(tag_name, recs.count()))
        if recs.count() == 1:
            return recs.get().uid
        elif recs.count() > 1:
            idx = 0
            rec0 = None
            for rec in recs:
                rec0 = rec
                # Only keep one.
                if idx == 0:
                    pass
                else:
                    g_Post2Tag.delete().where(g_Post2Tag.tag == rec.uid).execute()
                    g_Tag.delete().where(g_Tag.uid == rec.uid).execute()
                idx += 1
            return rec0.uid
        else:
            return MLabel.create_tag(tag_name)

    @staticmethod
    def delete(uid):
        return MHelper.delete(g_Tag, uid)

    @staticmethod
    def get_by_slug(tag_slug):
        uu = g_Tag.select().where(g_Tag.slug == tag_slug)
        if uu:
            return uu.get()
        else:
            return False

    @staticmethod
    def create_tag(tag_name, kind='z'):

        cur_count = g_Tag.select().where(
            (g_Tag.name == tag_name) &
            (g_Tag.kind == kind)
        ).count()
        if cur_count > 0:
            g_Tag.delete().where(
                (g_Tag.name == tag_name) &
                (g_Tag.kind == kind)
            ).execute()

        uid = tools.get_uu4d_v2()
        while g_Tag.select().where(g_Tag.uid == uid).count() > 0:
            uid = tools.get_uu4d_v2()

        g_Tag.create(
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

        if g_Tag.select().where(g_Tag.uid == uid).count():
            return False

        g_Tag.create(
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
        try:
            g_Post2Tag.create_table()
        except:
            pass

    @staticmethod
    def query_count(uid):
        return g_Post2Tag.select().where(g_Post2Tag.tag == uid).count()

    @staticmethod
    def remove_relation(post_id, tag_id):
        entry = g_Post2Tag.delete().where(
            (g_Post2Tag.post == post_id) & (g_Post2Tag.tag == tag_id)
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
    def get_by_uid(idd, kind='z'):
        return g_Post2Tag.select().join(g_Tag).where(
            (g_Post2Tag.post == idd) & (g_Tag.kind == 'z')
        )

    @staticmethod
    def get_by_info(post_id, catalog_id):
        tmp_recs = g_Post2Tag.select().join(g_Tag).where(
            (g_Post2Tag.post == post_id) &
            (g_Post2Tag.tag == catalog_id) &
            (g_Tag.kind == 'z')
        )

        if tmp_recs.count() > 1:
            ''' 如果多于1个，则全部删除
            '''
            idx = 0
            out_rec = None
            for tmp_rec in tmp_recs:
                if idx == 0:
                    out_rec = tmp_rec
                else:
                    entry = g_Post2Tag.delete().where(g_Post2Tag.uid == tmp_rec.uid)
                    entry.execute()
                idx += 1
            return out_rec

        elif tmp_recs.count() == 1:
            return tmp_recs.get()
        else:
            return None

    @staticmethod
    def add_record(post_id, tag_name, order=1, kind='z'):
        logger.info('Add label kind: {0}'.format(kind))
        tag_id = MLabel.get_id_by_name(tag_name, 'z')
        labelinfo = MPost2Label.get_by_info(post_id, tag_id)
        if labelinfo:
            entry = g_Post2Tag.update(
                order=order,
            ).where(g_Post2Tag.uid == labelinfo.uid)
            entry.execute()
        else:
            entry = g_Post2Tag.create(
                uid=tools.get_uuid(),
                post=post_id,
                tag=tag_id,
                order=order,
                kind='z')
            return entry.uid

    @staticmethod
    def total_number(slug, kind='1'):
        return g_Post.select().join(g_Post2Tag).where(
            (g_Post2Tag.tag == slug) & (g_Post.kind == kind)
        ).count()

    @staticmethod
    def query_pager_by_slug(slug, kind='1', current_page_num=1):
        return g_Post.select().join(g_Post2Tag).where(
            (g_Post2Tag.tag == slug) &
            (g_Post.kind == kind)
        ).paginate(current_page_num, CMS_CFG['list_num'])
