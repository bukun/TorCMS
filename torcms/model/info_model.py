# -*- coding:utf-8 -*-

import time
from datetime import datetime

import config
from config import cfg
import peewee
from torcms.core import tools
from torcms.model.supertable_model import MSuperTable
from torcms.model.post_model import MPost
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Post2Tag
from torcms.model.core_tab import g_Post2Tag as CabPost2Label
from torcms.model.core_tab import g_Usage
from torcms.model.core_tab import g_Rel
from torcms.model.core_tab import g_Reply


class MInforBase(MSuperTable):
    def __init__(self):
        self.kind = '2'
        self.tab_app = g_Post
        self.tab_app2catalog = g_Post2Tag
        self.tab_relation = g_Rel
        self.tab_app2label = CabPost2Label
        self.tab_usage = g_Usage
        self.cab_reply = g_Reply

    def get_all(self, kind='2'):
        return (self.tab_app.select().where((self.tab_app.kind == kind) & (self.tab_app.valid == 1)).order_by(
            self.tab_app.time_update.desc()))
    def update_kind(self, uid, kind):
        entry = self.tab_app.update(
            kind = kind,
        ).where(self.tab_app.uid == uid)
        entry.execute()
        return True
    def update_jsonb(self, uid, extinfo):
        cur_extinfo = self.get_by_uid(uid).extinfo
        for key in extinfo:
            cur_extinfo[key] = extinfo[key]
        entry = self.tab_app.update(
            extinfo=cur_extinfo,
        ).where(self.tab_app.uid == uid)
        entry.execute()
        return (uid)

    def delete(self, del_id):
        #todo: 
        # u1 = self.tab_app2catalog.delete().where(self.tab_app2catalog.post == del_id)
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
        # uu = self.tab_app.delete().where(self.tab_app.uid == del_id)
        # uu.execute()
        return False

    def modify_meta(self, app_id, data_dic):
        '''
        手工修改的。
        :param uid:
        :param data_dic:
        :return:
        '''
        pass

    def modify_init(self, uid, data_dic):
        '''
        命令行更新的
        :param uid:
        :param data_dic:
        :return:
        '''
        entry = self.tab_app.update(
            time_update=int(time.time()),
            # html_path=data_dic['html_path'],
            date=datetime.now(),
            keywords=data_dic['keywords'],
            kind=data_dic['kind'],
        ).where(self.tab_app.uid == uid)
        entry.execute()
        return (uid)

    def get_view_count(self, sig):
        try:
            return self.tab_app.get(uid=sig).view_count
        except:
            return False

    def view_count_increase(self, uid):
        infor = self.get_by_uid(uid)
        entry = self.tab_app.update(
            view_count=infor.view_count + 1,
        ).where(self.tab_app.uid == uid)
        entry.execute()

    def get_run_count(self, sig):
        try:
            return self.tab_app.get(uid=sig).run_count
        except:
            return False

    def run_count_increase(self, uid):

        entry = self.tab_app.update(
            run_count=self.get_run_count(uid) + 1,
        ).where(self.tab_app.uid == uid)
        entry.execute()

    def query_random(self, num=8, kind='2'):

        return self.tab_app.select().where((self.tab_app.kind == kind) & (self.tab_app.valid == 1)).order_by(
            peewee.fn.Random()).limit(num)

    def query_cat_random(self, catid, num=8, kind='2'):
        return self.tab_app.select().join(self.tab_app2catalog).where(
            (self.tab_app.kind == kind) & (self.tab_app.valid == 1) & (self.tab_app2catalog.tag == catid)).order_by(
            peewee.fn.Random()).limit(num)

    def query_most(self, kind='2', num=8, ):
        return self.tab_app.select().where((self.tab_app.kind == kind) & (self.tab_app.valid == 1)).order_by(
            self.tab_app.view_count.desc()).limit(num)

    def query_most_by_cat(self, num=8, catid=None, kind='2'):
        if catid:
            return self.tab_app.select().join(self.tab_app2catalog).where(
                (self.tab_app.kind == kind) & (self.tab_app.valid == 1) &
                (self.tab_app2catalog.tag == catid)).order_by(self.tab_app.view_count.desc()).limit(num)
        else:
            return False

    def query_least_by_cat(self, num=8, cat_str=1, kind='2'):
        return self.tab_app.select().join(self.tab_app2catalog).where(
            (self.tab_app.kind == kind) & (self.tab_app.valid == 1) &
            (self.tab_app2catalog.tag == cat_str)).order_by(self.tab_app.view_count).limit(num)

    def get_by_keyword(self, par2, kind='2'):
        return self.tab_app.select().where((self.tab_app.kind == kind) & (self.tab_app.valid == 1)
                                           & (self.tab_app.title.contains(par2))).order_by(
            self.tab_app.time_update.desc()).limit(20)

    def query_recent(self, num=8, kind='2'):
        return self.tab_app.select().where((self.tab_app.kind == kind) & (self.tab_app.valid == 1)).order_by(
            self.tab_app.time_update.desc()).limit(num)

    def get_by_uid(self, sig):
        cur_recs = self.tab_app.select().where(self.tab_app.uid ==  sig )
        if cur_recs.count() > 0:
            return cur_recs.get()
        else:
            return False
        # return self.tab_app.get(uid=sig)
        # try:
        #     return self.tab_app.get(uid=sig)
        # except:
        #     return False


class MInfor(MInforBase):
    def __init__(self):
        self.kind = '2'
        self.tab = g_Post
        self.tab_app = g_Post
        self.tab_app2catalog = g_Post2Tag
        self.tab_relation = g_Rel
        self.tab_app2label = CabPost2Label
        self.tab_usage = g_Usage
        # self.tab_app2reply = g_Post2Reply
        self.cab_reply = g_Reply
        try:
            g_Post.create_table()
        except:
            pass

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
            entry = self.tab_app.update(
                title=title,
                user_name=data_dic['user_name'],
                keywords=','.join([x.strip() for x in data_dic['keywords'].strip().strip(',').split(',')]),
                time_create = tools.timestamp(),
                time_update = tools.timestamp(),
                date=datetime.now(),
                cnt_md=data_dic['cnt_md'],
                logo=data_dic['logo'],
                cnt_html=tools.markdown2html(data_dic['cnt_md']),
                extinfo=cur_extinfo,
                valid=data_dic['valid'],

            ).where(self.tab_app.uid == uid)
            entry.execute()
        else:

            entry = self.add_meta(uid, data_dic, extinfo)
            return entry
        return (uid)

    def query_extinfo_by_cat(self, cat_id, kind='2'):
        return self.tab_app.select().where((self.tab_app.kind == kind) &
                                           (self.tab_app.valid == 1) & (
                                               self.tab_app.extinfo['def_cat_uid'] == cat_id)).order_by(
            self.tab_app.time_update.desc())

    def query_by_tagname(self, tag_name, kind='2'):
        return self.tab_app.select().where((self.tab_app.kind == kind) &
                                           (self.tab_app.valid == 1) & (
                                               self.tab_app.extinfo['def_tag_arr'].contains(tag_name))).order_by(
            self.tab_app.time_update.desc())

    def count_of_certain_category(self, cat_id):
        return self.tab_app.select().where(self.tab_app.tag == cat_id).count()

    def get_label_fenye(self, tag_slug, page_num):
        all_list = self.query_by_tagname(tag_slug)

        # 当前分页的记录
        current_list = all_list[(page_num - 1) * cfg['info_per_page']: (page_num) * cfg['info_per_page']]
        return (all_list)

    def query_pager_by_tag(self, tag, current_page_num=1):
        recs = self.query_by_tagname(tag).paginate(current_page_num, config.page_num)
        return recs

    def add_meta(self, uid, data_dic, extinfo={}):
        if len(uid) < 4:
            return False
        title = data_dic['title'].strip()
        if len(title) < 2:
            return False
        self.tab_app.create(
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
            valid=data_dic['valid'] if 'valid' in data_dic else 1 ,
            kind= data_dic['kind'] ,
        )
        return uid






    def get_list(self, condition, kind='2'):
        db_data = self.tab_app.select().where((self.tab_app.kind == kind) &
                                              (self.tab_app.valid == 1) & (
                                                  self.tab_app.extinfo.contains(condition))).order_by(
            self.tab_app.time_update.desc())
        print('count:', db_data.count())
        return (db_data)

    def get_num_condition(self, con):

        return self.get_list(con).count()

    def modify_init(self, uid, data_dic):
        '''
        命令行更新的
        :param uid:
        :param data_dic:
        :return:
        '''
        entry = self.tab_app.update(
            time_update=int(time.time()),
            # html_path=data_dic['html_path'],
            date=datetime.now(),
            kind=data_dic['kind'],
        ).where(self.tab_app.uid == uid)
        entry.execute()
        return (uid)

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

            entry = self.tab_app.create(
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

    def get_list_fenye(self, tag_slug, page_num, kind = '2'):
        print('get_list_fenye para:', tag_slug, page_num)

        all_list = self.get_list(tag_slug, kind = kind )
        current_list = all_list[(page_num - 1) * cfg['info_per_page']: (page_num) * cfg['info_per_page']]
        return (current_list)

    def get_cat_recs_count(self, catid, kind='2'):
        '''
        获取某一分类下的数目
        '''
        condition = {'catid': [catid]}

        db_data = self.tab_app.select().where(
            (self.tab_app.kind == kind) & (self.tab_app.valid == 1) & (self.tab_app.extinfo.contains(condition)))
        return db_data.count()
