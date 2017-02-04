# -*- coding:utf-8 -*-

import config
from torcms.model.core_tab import g_Tag
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

        #
        # del_count = g_Tag.delete().where(g_Tag.uid == uid)
        # del_count.execute()
        # return True

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
        return (recs)

    @staticmethod
    def query_field_count(limit_num, kind='1'):
        return g_Tag.select().where(g_Tag.kind == kind).order_by(g_Tag.count.desc()).limit(limit_num)

    @staticmethod
    def get_by_slug(slug):
        uu = g_Tag.select().where(g_Tag.slug == slug)
        if uu.count() > 0:
            return uu.get()
        else:
            return None

    @staticmethod
    def update_count(cat_id, num):
        entry = g_Tag.update(
            count=num,
        ).where(g_Tag.uid == cat_id)
        entry.execute()

    @staticmethod
    def update(uid, post_data):
        raw_rec = g_Tag.get(g_Tag.uid == uid)
        entry = g_Tag.update(
            name=post_data['name'] if 'name' in post_data else raw_rec.name,
            slug=post_data['slug'] if 'slug' in post_data else raw_rec.slug,
            order=post_data['order'] if 'order' in post_data else raw_rec.order,
            kind=post_data['kind'] if 'kind' in post_data else raw_rec.kind,

            pid=post_data['pid'],
            # role_mask = post_data['role_mask'] if 'role_mask' in post_data else '00100',
        ).where(g_Tag.uid == uid)
        entry.execute()

    @staticmethod
    def create_wiki_history(uid, post_data):
        uu = MCategory.get_by_uid(uid)
        # uu = g_Tag.get(uid = uid)
        if uu:
            MCategory.update(uid, post_data)
        else:
            entry = g_Tag.create(
                uid=uid,
                name=post_data['name'],
                slug=post_data['slug'],
                order=post_data['order'],
                kind=post_data['kind'] if 'kind' in post_data else '1',
                # tmpl = post_data['tmpl'],
                pid=post_data['pid'],
                # role_mask=post_data['role_mask'] if 'role_mask' in post_data else '00100',
            )
        return uid
