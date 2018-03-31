# -*- coding:utf-8 -*-

'''
Model for category
'''

from torcms.model.core_tab import TabTag, TabPost2Tag
from torcms.model.abc_model import Mabc, MHelper


class MCategory(Mabc):
    '''
    Model for category
    '''

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''
        return MHelper.delete(TabTag, uid)

    @staticmethod
    def get_by_uid(uid):
        return MHelper.get_by_uid(TabTag, uid)

    # Deprived
    @staticmethod
    def get_qian2(qian2):
        '''
        用于首页。根据前两位，找到所有的大类与小类。
        :param qian2: 分类id的前两位
        :return: 数组，包含了找到的分类
        '''
        return TabTag.select().where(
            TabTag.uid.startswith(qian2)
        ).order_by(TabTag.order)

    @staticmethod
    def get_parent_list(kind='1'):
        return TabTag.select().where(
            (TabTag.kind == kind) & (TabTag.uid.endswith('00'))
        ).order_by(
            TabTag.uid
        )

    @staticmethod
    def query_kind_cat(kind_sig):
        return TabTag.select().where(
            (TabTag.kind == kind_sig) & (TabTag.pid == '0000')
        ).order_by(TabTag.order)

    @staticmethod
    def query_sub_cat(pid):
        return TabTag.select().where(TabTag.pid == pid).order_by(TabTag.order)

    @staticmethod
    def query_pcat(**kwargs):
        _ = kwargs
        return TabTag.select().where(TabTag.pid == '0000').order_by(TabTag.order)

    @staticmethod
    def query_uid_starts_with(qian2):
        return MCategory.get_qian2(qian2)

    @staticmethod
    def query_all(kind='1', by_count=False, by_order=True):
        '''
        Qeury all the categories, order by count or defined order.
        '''
        if by_count:
            recs = TabTag.select().where(TabTag.kind == kind).order_by(TabTag.count.desc())
        elif by_order:
            recs = TabTag.select().where(TabTag.kind == kind).order_by(TabTag.order)
        else:
            recs = TabTag.select().where(TabTag.kind == kind).order_by(TabTag.uid)
        return recs

    @staticmethod
    def query_field_count(limit_num, kind='1'):
        '''
        Query the posts count of certain category.
        '''
        return TabTag.select().where(
            TabTag.kind == kind
        ).order_by(
            TabTag.count.desc()
        ).limit(limit_num)

    @staticmethod
    def get_by_slug(slug):
        '''
        return the category record .
        '''
        rec = TabTag.select().where(TabTag.slug == slug)
        if rec.count() > 0:
            return rec.get()
        return None

    @staticmethod
    def update_count(cat_id):
        '''
        Update the count of certain category.
        '''
        # Todo: the record not valid should not be counted.
        entry2 = TabTag.update(
            count=TabPost2Tag.select().where(
                TabPost2Tag.tag_id == cat_id
            ).count()
        ).where(TabTag.uid == cat_id)
        entry2.execute()

    @staticmethod
    def update(uid, post_data):
        '''
        Update the category.
        '''
        raw_rec = TabTag.get(TabTag.uid == uid)
        entry = TabTag.update(
            name=post_data['name'] if 'name' in post_data else raw_rec.name,
            slug=post_data['slug'] if 'slug' in post_data else raw_rec.slug,
            order=post_data['order'] if 'order' in post_data else raw_rec.order,
            kind=post_data['kind'] if 'kind' in post_data else raw_rec.kind,
            pid=post_data['pid'],
        ).where(TabTag.uid == uid)
        entry.execute()

    @staticmethod
    def add_or_update(uid, post_data):
        '''
        Add or update the data by the given ID of post.
        '''
        catinfo = MCategory.get_by_uid(uid)
        if catinfo:
            MCategory.update(uid, post_data)
        else:
            TabTag.create(
                uid=uid,
                name=post_data['name'],
                slug=post_data['slug'],
                order=post_data['order'],
                kind=post_data['kind'] if 'kind' in post_data else '1',
                pid=post_data['pid'],
            )
        return uid
