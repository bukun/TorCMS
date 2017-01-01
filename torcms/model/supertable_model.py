# -*- coding:utf-8 -*-

import time
import config
import peewee

from torcms.model.core_tab import g_Tag


class MSuperTable():
    def __init__(self):
        self.tab = g_Tag
        try:
            self.tab.create_table()
        except:
            pass

    def get_counts(self):
        return self.tab.select().count()

    def update(self, uid, post_data, update_time=False):
        pass

    def insert_data(self, id_post, post_data):
        pass

    def query_old(self):
        return self.tab.select().order_by('time_update').limit(10)



    def get_parent_list(self, kind='1'):
        db_data = self.tab.select().where((self.tab.kind == kind) & (self.tab.uid.endswith('00'))).order_by(
            self.tab.uid)
        return (db_data)

    def get_by_id(self, in_uid):
        return self.get_by_uid(in_uid)

    def get_by_uid(self, in_uid):
        recs = self.tab.select().where(self.tab.uid == in_uid)
        if recs.count() == 0:
            return None
        else:
            return recs.get()

    def query_all(self, limit_num=50, by_uid='False', kind=None):
        if kind:
            if by_uid:
                return self.tab.select().where(self.tab.kind == kind).order_by(self.tab.uid).limit(limit_num)
            else:
                return self.tab.select().where(self.tab.kind == kind).limit(limit_num)
        else:

            if by_uid:
                return self.tab.select().order_by(self.tab.uid).limit(limit_num)
            else:
                return self.tab.select().limit(limit_num)

    def query_random(self, num=6, kind = '1'):
        return self.tab.select().where(self.tab.kind == kind).order_by(peewee.fn.Random()).limit(num)
    def query_recent(self, num=8, kind = '1'):
        return self.tab.select().where(self.tab.kind == kind).limit(num)

    def delete(self, del_id):

        del_count = self.tab.delete().where(self.tab.uid == del_id)
        del_count.execute()

    def query_recent_most(self, num=8, recent=30):
        time_that = int(time.time()) - recent * 24 * 3600
        return self.tab.select().where(self.tab.time_update > time_that).order_by(self.tab.view_count.desc()).limit(num)

    def query_cat_by_pager(self, cat_str, cureent):
        tt = self.tab.select().where(self.tab.id_cats.contains(str(cat_str))).order_by(
            self.tab.time_update.desc()).paginate(cureent, config.page_num)
        return tt

    def query_by_spec(self, spec_id):
        return self.tab.select().where(self.tab.id_spec == spec_id).order_by(self.tab.time_update.desc())

    def get_by_keyword(self, par2):
        return self.tab.select().where(self.tab.title.contains(par2)).order_by(self.tab.time_update.desc()).limit(20)
