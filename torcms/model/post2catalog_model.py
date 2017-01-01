# -*- coding:utf-8 -*-

import peewee

import config
from torcms.core import tools
from torcms.model.core_tab import g_Tag, g_Post, g_Post2Tag
from torcms.model.supertable_model import MSuperTable




class MPost2Catalog(MSuperTable):
    def __init__(self):
        self.tab_post2catalog = g_Post2Tag
        self.tab_catalog = g_Tag
        self.tab_post = g_Post
        self.kind = '1'
        try:
            g_Post2Tag.create_table()
        except:
            pass

    def remove_relation(self, post_id, tag_id):
        entry = self.tab_post2catalog.delete().where(
            (self.tab_post2catalog.post == post_id) & (self.tab_post2catalog.tag == tag_id))
        entry.execute()
    def remove_tag(self,  tag_id):
        entry = self.tab_post2catalog.delete().where(self.tab_post2catalog.tag == tag_id)
        entry.execute()


    def query_by_catid(self, catid):
        return self.tab_post2catalog.select().where(self.tab_post2catalog.tag == catid)

    def __get_by_info(self, post_id, catalog_id):
        recs = self.tab_post2catalog.select().where(
            (self.tab_post2catalog.post == post_id) & (self.tab_post2catalog.tag == catalog_id))
        if recs.count() > 1:
            idx = 0
            for rec in recs:
                if idx == 0:
                    out_rec = rec
                    pass
                else:
                    entry = self.tab_post2catalog.delete().where(self.tab_post2catalog.uid == rec.uid)
                    entry.execute()
                    # self.delete(rec.uid)
                idx = idx + 1
            return out_rec.get()
        elif recs.count() == 1:
            return self.tab_post2catalog.get(
                (self.tab_post2catalog.post == post_id) & (self.tab_post2catalog.tag == catalog_id))
        else:
            return False

    def query_count(self):
        recs = self.tab_post2catalog.select(self.tab_post2catalog.tag,
                                            peewee.fn.COUNT(self.tab_post2catalog.tag).alias('num')).group_by(
            self.tab_post2catalog.tag)
        return (recs)

    def add_record(self, post_id, catalog_id, order=0):
        tt = self.__get_by_info(post_id, catalog_id)
        if tt:
            entry = self.tab_post2catalog.update(
                order=order,
            ).where(self.tab_post2catalog.uid == tt.uid)
            entry.execute()
        else:
            self.tab_post2catalog.create(
                uid=tools.get_uuid(),
                post=post_id,
                tag =catalog_id,
                order=order,
            )

    def count_of_certain_category(self, cat_id):
        return self.tab_post2catalog.select().where(self.tab_post2catalog.tag == cat_id).count()

    def query_pager_by_slug(self, slug, current_page_num=1):
        recs = self.tab_post.select().join(self.tab_post2catalog).join(self.tab_catalog).where(
             self.tab_catalog.slug == slug ).order_by(
            self.tab_post.time_update.desc()).paginate(current_page_num, config.page_num)
        return recs


    def query_by_entity_uid(self, idd, kind=''):
        if kind == '':
            return self.tab_post2catalog.select().join(self.tab_catalog).where(
                 (self.tab_post2catalog.post == idd) & (self.tab_catalog.kind != 'z')).order_by(
                self.tab_post2catalog.order)
        else:
            return self.tab_post2catalog.select().join(self.tab_catalog).where(
            (self.tab_catalog.kind == kind) & (self.tab_post2catalog.post == idd)).order_by(
            self.tab_post2catalog.order)

    def query_by_id(self, idd):
        return self.query_by_entity_uid(idd)


    def get_entry_catalog(self, app_uid):
        '''
        Get the first, uniqe category of post.
        :param app_uid:
        :return:
        '''

        uu = self.query_by_entity_uid(app_uid)
        if uu.count() > 0:
            return uu.get()
        else:
            return None
