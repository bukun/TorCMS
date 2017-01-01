# -*- coding:utf-8 -*-

import config
from torcms.model.core_tab import g_Tag
from torcms.model.supertable_model import MSuperTable


class MCategory(MSuperTable):
    def __init__(self):
        self.tab = g_Tag
        self.kind = '1'
        try:
            g_Tag.create_table()
        except:
            pass
    # Deprived
    def get_qian2(self, qian2):

        '''
        用于首页。根据前两位，找到所有的大类与小类。
        :param qian2: 分类id的前两位
        :return: 数组，包含了找到的分类
        '''
        return self.tab.select().where( self.tab.uid.startswith(qian2)).order_by(
            self.tab.order)
    def query_kind_cat(self, kind_sig):
        return self.tab.select().where((self.tab.kind == kind_sig) & (self.tab.pid == '0000') ).order_by(   self.tab.order)

    def query_sub_cat(self, pid):
        return self.tab.select().where(self.tab.pid == pid ).order_by(   self.tab.order)
    def query_pcat(self, kind='1'):
        return self.tab.select().where((self.tab.kind == kind) & (self.tab.uid.endswith('00'))).order_by(self.tab.order)

    def query_uid_starts_with(self, qian2):
        return self.get_qian2(qian2)

    def query_all(self, by_count=False, by_order=True, kind='1'):
        if by_count:
            recs = self.tab.select().where(self.tab.kind == kind).order_by(self.tab.count.desc())
        elif by_order:
            recs = self.tab.select().where(self.tab.kind == kind).order_by(self.tab.order)
        else:
            recs = self.tab.select().where(self.tab.kind == kind).order_by(self.tab.uid)
        return (recs)

    def query_field_count(self, limit_num, kind='1'):
        return self.tab.select().where(self.tab.kind == kind).order_by(self.tab.count.desc()).limit(limit_num)

    def get_by_slug(self, slug):
        uu = self.tab.select().where(self.tab.slug == slug)
        if uu.count() > 0:
            return uu.get()
        else:
            return False

    def update_count(self, cat_id, num):
        entry = self.tab.update(
            count=num,
        ).where(self.tab.uid == cat_id)
        entry.execute()

    def update(self, uid, post_data):
        raw_rec = self.get_by_id(uid)
        entry = self.tab.update(
            name=post_data['name'] if 'name' in post_data else raw_rec.name,
            slug=post_data['slug'] if 'slug' in post_data else raw_rec.slug,
            order=post_data['order'] if 'order' in post_data else raw_rec.order,
            kind=post_data['kind'] if 'kind' in post_data else raw_rec.kind,
            tmpl=post_data['tmpl'],
            pid=post_data['pid'],
            # role_mask = post_data['role_mask'] if 'role_mask' in post_data else '00100',
        ).where(self.tab.uid == uid)
        entry.execute()

    def insert_data(self, uid, post_data):
        uu = self.get_by_id(uid)
        if uu:
            self.update(uid, post_data)
        else:
            entry = self.tab.create(
                uid=uid,
                name=post_data['name'],
                slug=post_data['slug'],
                order=post_data['order'],
                kind=post_data['kind'] if 'kind' in post_data else '1',
                tmpl = post_data['tmpl'],
                pid = post_data['pid'],
                # role_mask=post_data['role_mask'] if 'role_mask' in post_data else '00100',
            )
            return (entry.uid)
