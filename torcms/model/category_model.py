# -*- coding:utf-8 -*-

from torcms.model.core_tab import g_Tag, g_Post2Tag
from torcms.model.abc_model import Mabc, MHelper


class MCategory(Mabc):
    def __init__(self):
        try:
            g_Tag.create_table()
        except:
            pass

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        :param uid:
        :return:
        '''
        return MHelper.delete(g_Tag, uid)

    @staticmethod
    def get_by_uid(uid):
        return MHelper.get_by_uid(g_Tag, uid)

    # Deprived
    @staticmethod
    def get_qian2(qian2):

        '''
        用于首页。根据前两位，找到所有的大类与小类。
        :param qian2: 分类id的前两位
        :return: 数组，包含了找到的分类
        '''
        return g_Tag.select().where(
            g_Tag.uid.startswith(qian2)
        ).order_by(g_Tag.order)

    @staticmethod
    def get_parent_list(kind='1'):
        db_data = g_Tag.select().where((g_Tag.kind == kind) & (g_Tag.uid.endswith('00'))).order_by(
            g_Tag.uid)
        return db_data

    @staticmethod
    def query_kind_cat(kind_sig):
        return g_Tag.select().where(
            (g_Tag.kind == kind_sig) & (g_Tag.pid == '0000')
        ).order_by(g_Tag.order)

    @staticmethod
    def query_sub_cat(pid):
        return g_Tag.select().where(g_Tag.pid == pid).order_by(g_Tag.order)

    @staticmethod
    def query_pcat(kind='1'):
        return g_Tag.select().where(
            (g_Tag.kind == kind) & (g_Tag.uid.endswith('00'))
        ).order_by(g_Tag.order)

    @staticmethod
    def query_uid_starts_with(qian2):
        return MCategory.get_qian2(qian2)

    @staticmethod
    def query_all(by_count=False, by_order=True, kind='1'):
        if by_count:
            recs = g_Tag.select().where(g_Tag.kind == kind).order_by(g_Tag.count.desc())
        elif by_order:
            recs = g_Tag.select().where(g_Tag.kind == kind).order_by(g_Tag.order)
        else:
            recs = g_Tag.select().where(g_Tag.kind == kind).order_by(g_Tag.uid)
        return recs

    @staticmethod
    def query_field_count(limit_num, kind='1'):
        return g_Tag.select().where(g_Tag.kind == kind).order_by(g_Tag.count.desc()).limit(limit_num)

    @staticmethod
    def get_by_slug(slug):
        '''
        return the category record .
        :param slug:
        :return:
        '''
        uu = g_Tag.select().where(g_Tag.slug == slug)
        if uu.count() > 0:
            return uu.get()
        else:
            return None

    @staticmethod
    def update_count(cat_id):
        '''
        Update the count of certain category.
        :param cat_id:
        :return:
        '''
        entry2 = g_Tag.update(
            count=g_Post2Tag.select().where(
                g_Post2Tag.tag == cat_id
            ).count()
        ).where(g_Tag.uid == cat_id)
        entry2.execute()

    @staticmethod
    def update(uid, post_data):
        '''
        Update the category.
        :param uid:
        :param post_data:
        :return:
        '''
        raw_rec = g_Tag.get(g_Tag.uid == uid)
        entry = g_Tag.update(
            name=post_data['name'] if 'name' in post_data else raw_rec.name,
            slug=post_data['slug'] if 'slug' in post_data else raw_rec.slug,
            order=post_data['order'] if 'order' in post_data else raw_rec.order,
            kind=post_data['kind'] if 'kind' in post_data else raw_rec.kind,
            pid=post_data['pid'],
        ).where(g_Tag.uid == uid)
        entry.execute()

    @staticmethod
    def create_wiki_history(uid, post_data):
        catinfo = MCategory.get_by_uid(uid)
        if catinfo:
            MCategory.update(uid, post_data)
        else:
            g_Tag.create(
                uid=uid,
                name=post_data['name'],
                slug=post_data['slug'],
                order=post_data['order'],
                kind=post_data['kind'] if 'kind' in post_data else '1',
                pid=post_data['pid'],
            )
        return uid
