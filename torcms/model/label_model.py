# -*- coding:utf-8 -*-

import config
from torcms.core import tools
from torcms.model.core_tab import g_Tag
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Post2Tag as g_Post2Tag
from torcms.model.supertable_model import MSuperTable


class MLabel(MSuperTable):
    def __init__(self):
        self.tab = g_Tag


    def get_id_by_name(self, tag_name, kind = 'z'):
        uu = self.tab.select().where((self.tab.name == tag_name) & (self.tab.kind == kind))
        print('tag count of name:', tag_name, uu.count())
        if uu.count() == 1:
            return uu.get().uid
        elif uu.count() > 1:
            idx = 0
            for x in uu:
                tx = x
                # Only keep one.
                if idx == 0:
                    pass
                else:
                    print('Delete tag,', x.uid )
                    g_Post2Tag.delete().where(g_Post2Tag.tag == x.uid ).execute()
                    self.tab.delete().where( self.tab.uid  == x.uid ).execute()
                idx = idx + 1
            return tx.get().uid
        else:
            return self.create_tag(tag_name)

    def get_by_slug(self, tag_slug):
        uu = self.tab.select().where(self.tab.slug == tag_slug)
        if uu:
            return uu.get()
        else:
            return False

    def create_tag(self, tag_name, kind='z'):

        cur_count = self.tab.select().where((self.tab.name == tag_name) & (self.tab.kind == kind)).count()
        if cur_count > 0:
            return False

        uid = tools.get_uu4d_v2()
        while self.tab.select().where(self.tab.uid == uid).count() > 0:
            uid = tools.get_uu4d_v2()

        self.tab.create(
            uid=uid,
            slug = uid,
            name=tag_name,
            order = 1,
            count=0,
            kind = 'z',
            tmpl = 9,
            pid = 'zzzz',
        )
        return uid

    def create_tag_with_uid(self, uid, tag_name):

        if self.tab.select().where(self.tab.uid == uid).count():
            return False

        self.tab.create(
            uid=uid,
            slug = uid,
            name=tag_name,
            order = 1,
            count=0,
            kind = 'z',
            tmpl=9,
            pid='zzzz',
        )
        return uid

class MPost2Label(MSuperTable):
    def __init__(self):
        self.tab = g_Post2Tag
        self.tab_label = g_Tag
        self.tab_post = g_Post
        self.mtag = MLabel()
        try:
            g_Post2Tag.create_table()
        except:
            pass
    def remove_relation(self, post_id, tag_id):
        entry = self.tab.delete().where((self.tab.post == post_id) & (self.tab.tag == tag_id))
        entry.execute()

    def generate_catalog_list(self, signature):
        tag_infos = self.get_by_id(signature)
        out_str = ''
        for tag_info in tag_infos:
            tmp_str = '<li><a href="/tag/{0}" >{1}</a></li>'.format(tag_info.tag, tag_info.catalog_name)
            out_str += tmp_str
        return out_str

    def get_by_id(self, idd, kind = 'z'):
        return self.tab.select().join(self.tab_label).where((self.tab.post == idd) & (self.tab_label.kind == 'z') )



    def get_by_info(self, post_id, catalog_id):
        tmp_recs = self.tab.select().join(self.tab_label).where((self.tab.post == post_id) & (self.tab.tag == catalog_id) & (self.tab_label.kind == 'z'))

        if tmp_recs.count() > 1:
            ''' 如果多于1个，则全部删除
            '''
            idx = 0
            for tmp_rec in tmp_recs:
                if idx == 0:
                    out_rec = tmp_rec
                else:
                    self.delete(tmp_rec.uid)
                idx = idx + 1
            return out_rec.get()

        elif tmp_recs.count() == 1:
            return tmp_recs.get()
        else:
            return False

    def add_record(self, post_id, tag_name, order=1, kind = 'z'):
        print('Add label kind: {0}'.format(kind))
        tag_id = self.mtag.get_id_by_name(tag_name, 'z')
        print('tag_id:', tag_id)
        tt = self.get_by_info(post_id, tag_id)
        if tt:
            entry = self.tab.update(
                order=order,
            ).where(self.tab.uid == tt.uid)
            entry.execute()
        else:
            entry = self.tab.create(
                uid=tools.get_uuid(),
                post=post_id,
                tag=tag_id,
                order=order,
                kind = 'z',
            )
            return entry.uid


    def total_number(self, slug,kind = '1'):
        return self.tab_post.select().join(self.tab).where((self.tab.tag == slug) & (self.tab_post.kind == kind)).count()

    def query_pager_by_slug(self, slug, kind = '1', current_page_num=1):
        return self.tab_post.select().join(self.tab).where((self.tab.tag == slug) & (self.tab_post.kind == kind)).paginate(current_page_num,
                                                                                          config.page_num)
