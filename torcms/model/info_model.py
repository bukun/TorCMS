# -*- coding:utf-8 -*-

'''
Model for infor.
'''

import time
from datetime import datetime

import peewee
from torcms.core import tools
from torcms.model.abc_model import Mabc
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Post2Tag
# from torcms.model.core_tab import g_Post2Tag as CabPost2Label
from torcms.model.core_tab import g_Usage
from torcms.model.core_tab import g_Rel
from torcms.model.core_tab import g_Reply

import config
from config import cfg_render


#
# class MInforBase(Mabc):
#     '''
#     The base model of Infor.
#     '''
#
#     def __init__(self):
#         self.kind = '2'
#         self.tab_app = g_Post
#         self.tab_app2label = g_Post2Tag
#         self.tab_relation = g_Rel
#         self.tab_app2label = CabPost2Label
#         self.tab_usage = g_Usage
#         self.cab_reply = g_Reply



class MInfor(Mabc):
    def __init__(self):
        self.kind = '2'
        self.tab = g_Post
        # self.tab_app = g_Post
        # self.tab_app2label = g_Post2Tag
        self.tab_relation = g_Rel
        self.tab_app2label = g_Post2Tag
        self.tab_usage = g_Usage
        self.cab_reply = g_Reply
        try:
            g_Post.create_table()
        except:
            pass

    def get_all(self, kind='2'):
        return self.tab.select().where(
            (self.tab.kind == kind) &
            (self.tab.valid == 1)
        ).order_by(
            self.tab.time_update.desc()
        )

    def update_kind(self, uid, kind):
        entry = self.tab.update(
            kind=kind,
        ).where(self.tab.uid == uid)
        entry.execute()
        return True

    def update_jsonb(self, uid, extinfo):
        cur_extinfo = self.get_by_uid(uid).extinfo
        for key in extinfo:
            cur_extinfo[key] = extinfo[key]
        entry = self.tab.update(
            extinfo=cur_extinfo,
        ).where(self.tab.uid == uid)
        entry.execute()
        return uid

    def delete(self, del_id):
        # todo:
        # u1 = self.tab_app2label.delete().where(self.tab_app2label.post == del_id)
        # u1.execute()
        # u2 = self.tab_relation.delete().where(self.tab_relation.post_f == del_id)
        # u2.execute()
        # u3 = self.tab_relation.delete().where(self.tab_relation.post_t == del_id)
        # u3.execute()
        # u4 = self.tab_app2label.delete().where(self.tab_app2label.post == del_id)
        # u4.execute()
        # u5 = self.tab_usage.delete().where(self.tab_usage.post == del_id)
        # u5.execute()
        #
        # reply_arr = []
        # for reply in self.tab_app2reply.select().where(self.tab_app2reply.post_id == del_id):
        #     reply_arr.append(reply.reply_id.uid)
        #
        # u6 = self.tab_app2reply.delete().where(self.tab_app2reply.post_id == del_id)
        # u6.execute()
        #
        # for replyid in reply_arr:
        #     self.cab_reply.delete().where(self.cab_reply.uid == replyid).execute()
        #
        # uu = self.tab.delete().where(self.tab.uid == del_id)
        # uu.execute()
        return False

    def modify_meta(self, uid, data_dic, extinfo={}):
        '''
        手工修改的。
        :param uid:
        :param data_dic:
        :return:
        '''
        title = data_dic['title'].strip()
        if len(title) < 2:
            return False

        cur_info = self.get_by_uid(uid)
        if cur_info:
            cur_extinfo = cur_info.extinfo
            # Update the extinfo, Not replace
            for key in extinfo:
                cur_extinfo[key] = extinfo[key]
            entry = self.tab.update(
                title=title,
                user_name=data_dic['user_name'],
                keywords=','.join(
                    [x.strip() for x in data_dic['keywords'].strip().strip(',').split(',')]
                ),
                time_create=tools.timestamp(),
                time_update=tools.timestamp(),
                date=datetime.now(),
                cnt_md=data_dic['cnt_md'],
                logo=data_dic['logo'],
                cnt_html=tools.markdown2html(data_dic['cnt_md']),
                extinfo=cur_extinfo,
                valid=data_dic['valid'],

            ).where(self.tab.uid == uid)
            entry.execute()
        else:

            entry = self.add_meta(uid, data_dic, extinfo)
            return entry
        return uid

    # def modify_init(self, uid, data_dic):
    #     '''
    #     命令行更新的
    #     :param uid:
    #     :param data_dic:
    #     :return:
    #     '''
    #     entry = self.tab.update(
    #         time_update=int(time.time()),
    #         date=datetime.now(),
    #         keywords=data_dic['keywords'],
    #         kind=data_dic['kind'],
    #     ).where(self.tab.uid == uid)
    #     entry.execute()
    #     return uid

    def modify_init(self, uid, data_dic):
        '''
        命令行更新的
        :param uid:
        :param data_dic:
        :return:
        '''
        postinfo = self.get_by_uid(uid)
        entry = self.tab.update(
            time_update=tools.timestamp(),
            date=datetime.now(),
            kind=data_dic['kind'] if 'kind' in data_dic else postinfo.kind,
            keywords=data_dic['keywords'] if 'keywords' in data_dic else postinfo.keywords,
        ).where(self.tab.uid == uid)
        entry.execute()
        return uid

    def get_view_count(self, sig):
        try:
            return self.tab.get(uid=sig).view_count
        except:
            return False

    def view_count_increase(self, uid):
        infor = self.get_by_uid(uid)
        entry = self.tab.update(
            view_count=infor.view_count + 1,
        ).where(self.tab.uid == uid)
        entry.execute()

    def get_run_count(self, sig):
        try:
            return self.tab.get(uid=sig).run_count
        except:
            return False

    def run_count_increase(self, uid):

        entry = self.tab.update(
            run_count=self.get_run_count(uid) + 1,
        ).where(self.tab.uid == uid)
        entry.execute()

    def query_random(self, num=8, kind='2'):

        return self.tab.select().where(
            (self.tab.kind == kind) &
            (self.tab.valid == 1)
        ).order_by(
            peewee.fn.Random()
        ).limit(num)

    def query_cat_random(self, catid, num=8, kind='2'):
        return self.tab.select().join(self.tab_app2label).where(
            (self.tab.kind == kind) &
            (self.tab.valid == 1) &
            (self.tab_app2label.tag == catid)
        ).order_by(
            peewee.fn.Random()
        ).limit(num)

    def query_most(self, kind='2', num=8, ):
        return self.tab.select().where(
            (self.tab.kind == kind) &
            (self.tab.valid == 1)
        ).order_by(
            self.tab.view_count.desc()
        ).limit(num)

    def query_most_by_cat(self, num=8, catid=None, kind='2'):
        if catid:
            return self.tab.select().join(self.tab_app2label).where(
                (self.tab.kind == kind) &
                (self.tab.valid == 1) &
                (self.tab_app2label.tag == catid)
            ).order_by(
                self.tab.view_count.desc()
            ).limit(num)
        else:
            return False

    def query_least_by_cat(self, num=8, cat_str=1, kind='2'):
        return self.tab.select().join(self.tab_app2label).where(
            (self.tab.kind == kind) &
            (self.tab.valid == 1) &
            (self.tab_app2label.tag == cat_str)
        ).order_by(
            self.tab.view_count
        ).limit(num)

    def get_by_keyword(self, par2, kind='2'):
        return self.tab.select().where(
            (self.tab.kind == kind) &
            (self.tab.valid == 1) &
            (self.tab.title.contains(par2))
        ).order_by(
            self.tab.time_update.desc()
        ).limit(20)

    def query_recent(self, num=8, kind='2'):
        return self.tab.select().where(
            (self.tab.kind == kind) &
            (self.tab.valid == 1)
        ).order_by(
            self.tab.time_update.desc()
        ).limit(num)

    def get_by_uid(self, sig):
        cur_recs = self.tab.select().where(self.tab.uid == sig)
        if cur_recs.count() > 0:
            return cur_recs.get()
        else:
            return None
            # return self.tab.get(uid=sig)
            # try:
            #     return self.tab.get(uid=sig)
            # except:
            #     return False

    def query_extinfo_by_cat(self, cat_id, kind='2'):
        return self.tab.select().where(
            (self.tab.kind == kind) &
            (self.tab.valid == 1) &
            (self.tab.extinfo['def_cat_uid'] == cat_id)
        ).order_by(
            self.tab.time_update.desc()
        )

    def query_by_tagname(self, tag_name, kind='2'):
        return self.tab.select().where(
            (self.tab.kind == kind) &
            (self.tab.valid == 1) &
            (self.tab.extinfo['def_tag_arr'].contains(tag_name))
        ).order_by(
            self.tab.time_update.desc()
        )

    # def count_of_certain_category(self, cat_id):
    #     return self.tab.select().where(self.tab.tag == cat_id).count()

    def get_label_fenye(self, tag_slug, idx):
        all_list = self.query_by_tagname(tag_slug)

        # 当前分页的记录
        # Todo
        current_list = all_list[(idx - 1) * cfg_render['info_per_page']: idx * cfg_render['info_per_page']]
        return all_list

    def query_pager_by_tag(self, tag, current_page_num=1, kind='2'):
        recs = self.query_by_tagname(tag, kind).paginate(current_page_num, config.page_num)
        return recs

    def add_meta(self, uid, data_dic, extinfo={}):
        if len(uid) < 4:
            return False
        title = data_dic['title'].strip()
        if len(title) < 2:
            return False
        self.tab.create(
            uid=uid,
            title=title,
            keywords=','.join([x.strip() for x in data_dic['keywords'].split(',')]),
            time_create=tools.timestamp(),
            time_update=tools.timestamp(),
            create_time=tools.timestamp(),
            date=datetime.now(),
            cnt_md=data_dic['cnt_md'].strip(),
            logo=data_dic['logo'].strip(),
            cnt_html=tools.markdown2html(data_dic['cnt_md']),
            view_count=0,
            extinfo=extinfo,
            user_name=data_dic['user_name'],
            valid=data_dic['valid'] if 'valid' in data_dic else 1,
            kind=data_dic['kind'],
        )
        return uid

    def get_list(self, condition, kind='2'):
        db_data = self.tab.select().where(
            (self.tab.kind == kind) &
            (self.tab.valid == 1) &
            (self.tab.extinfo.contains(condition))
        ).order_by(
            self.tab.time_update.desc()
        )

        return db_data

    def get_num_condition(self, con):

        return self.get_list(con).count()

    def addata_init(self, data_dic, ext_dic={}):
        if len(data_dic['sig']) < 4:
            return False
        title = data_dic['title'].strip()
        if len(title) < 2:
            return False

        if self.get_by_uid(data_dic['sig']):
            uu = self.get_by_uid(data_dic['sig'])
            if data_dic['title'] == uu.title and data_dic['kind'] == uu.kind:
                pass
            else:
                self.modify_init(data_dic['sig'], data_dic)
        else:
            time_stamp = int(time.time())

            entry = self.tab.create(
                uid=data_dic['sig'],
                title=data_dic['title'],
                create_time=time_stamp,
                time_update=time_stamp,
                cnt_md=data_dic['cnt_md'],
                cnt_html=data_dic['cnt_html'],
                date=datetime.now(),
                keywords=data_dic['keywords'],
                extinfo=ext_dic
            )

    def get_list_fenye(self, tag_slug, idx, kind='2'):
        # ('get_list_fenye para:', tag_slug, idx)

        all_list = self.get_list(tag_slug, kind=kind)
        current_list = all_list[(idx - 1) * cfg_render['info_per_page']: idx * cfg_render['info_per_page']]
        return current_list

    def get_cat_recs_count(self, catid, kind='2'):
        '''
        获取某一分类下的数目
        '''
        condition = {'catid': [catid]}

        db_data = self.tab.select().where(
            (self.tab.kind == kind) &
            (self.tab.valid == 1) &
            (self.tab.extinfo.contains(condition))
        )
        return db_data.count()
