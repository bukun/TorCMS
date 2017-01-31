# -*- coding:utf-8 -*-

'''
The Base of Model
'''
import time
import peewee
from torcms.model.core_tab import g_Post


class Mabc():
    '''
    The Base of Model
    '''
    def __init__(self):
        self.tab = g_Post
        try:
            self.tab.create_table()
        except:
            pass

    def get_counts(self):
        '''
        The count in table.
        :return:
        '''
        return self.tab.select().count()

    def update(self, uid, post_data, update_time=False):
        pass

    def create_page(self, id_post, post_data):
        pass

    def query_old(self):
        return self.tab.select().order_by('time_update').limit(10)

    def get_parent_list(self, kind='1'):
        db_data = self.tab.select().where((self.tab.kind == kind) & (self.tab.uid.endswith('00'))).order_by(
            self.tab.uid)
        return (db_data)

    def get_by_id(self, uid):
        '''
        return the record by uid
        :param uid:
        :return:
        '''
        return self.get_by_uid(uid)

    def get_by_uid(self, uid):
        recs = self.tab.select().where(self.tab.uid == uid)
        if recs.count() == 0:
            return None
        else:
            return recs.get()

    def query_all(self, limit_num=50, by_uid='False', kind=None):
        '''
        Return some of the records. Not all.
        :param limit_num:
        :param by_uid:
        :param kind:
        :return:
        '''
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

    def query_random(self, num=6, kind='1'):
        '''
        Return the random records of centain kind.
        :param num:
        :param kind:
        :return:
        '''
        return self.tab.select().where(self.tab.kind == kind).order_by(peewee.fn.Random()).limit(num)

    def query_recent(self, num=8, kind='1'):
        return self.tab.select().where(self.tab.kind == kind).limit(num)

    def delete(self, uid):
        '''
        Delete by uid
        :param uid:
        :return:
        '''

        del_count = self.tab.delete().where(self.tab.uid == uid)
        del_count.execute()

    def query_recent_most(self, num=8, recent=30):
        '''
        Query the records from database that recently updated.
        :param num: the number that will returned.
        :param recent: the number of days recent.
        :return:
        '''
        time_that = int(time.time()) - recent * 24 * 3600
        return self.tab.select().where(self.tab.time_update > time_that).order_by(self.tab.view_count.desc()).limit(num)

    # def query_cat_by_pager(self, cat_str, cureent):
    #     tt = self.tab.select().where(self.tab.id_cats.contains(str(cat_str))).order_by(
    #         self.tab.time_update.desc()).paginate(cureent, config.page_num)
    #     return tt

    # def query_by_spec(self, spec_id):
    #     return self.tab.select().where(self.tab.id_spec == spec_id).order_by(self.tab.time_update.desc())

    def get_by_keyword(self, par2):
        return self.tab.select().where(self.tab.title.contains(par2)).order_by(self.tab.time_update.desc()).limit(20)
