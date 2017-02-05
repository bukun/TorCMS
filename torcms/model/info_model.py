# -*- coding:utf-8 -*-

'''
Model for infor.
'''

import time
from datetime import datetime

import peewee
from torcms.core import tools
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Post2Tag

from config import CMS_CFG
from torcms.model.abc_model import Mabc


class MInfor(Mabc):
    @staticmethod
    def get_all(kind='2'):
        return g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.valid == 1)
        ).order_by(
            g_Post.time_update.desc()
        )

    @staticmethod
    def query_all(limit=10, kind='2'):
        return g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.valid == 1)
        ).order_by(
            g_Post.time_update.desc()
        ).limit(limit)

    @staticmethod
    def update_kind(uid, kind):
        entry = g_Post.update(
            kind=kind,
        ).where(g_Post.uid == uid)
        entry.execute()
        return True

    @staticmethod
    def update_jsonb(uid, extinfo):
        cur_extinfo = MInfor.get_by_uid(uid).extinfo
        for key in extinfo:
            cur_extinfo[key] = extinfo[key]
        entry = g_Post.update(
            extinfo=cur_extinfo,
        ).where(g_Post.uid == uid)
        entry.execute()
        return uid

    @staticmethod
    def delete(del_id):
        # todo:
        # u1 = g_Post2Tag.delete().where(g_Post2Tag.post == del_id)
        # u1.execute()
        # u2 = g_Rel.delete().where(g_Rel.post_f == del_id)
        # u2.execute()
        # u3 = g_Rel.delete().where(g_Rel.post_t == del_id)
        # u3.execute()
        # u4 = g_Post2Tag.delete().where(g_Post2Tag.post == del_id)
        # u4.execute()
        # u5 = g_Usage.delete().where(g_Usage.post == del_id)
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
        #     g_Reply.delete().where(g_Reply.uid == replyid).execute()
        #
        # uu = g_Post.delete().where(g_Post.uid == del_id)
        # uu.execute()
        return False

    @staticmethod
    def modify_meta(uid, data_dic, extinfo={}):
        '''
        手工修改的。
        :param uid:
        :param data_dic:
        :return:
        '''
        title = data_dic['title'].strip()
        if len(title) < 2:
            return False

        cur_info = MInfor.get_by_uid(uid)
        if cur_info:
            cur_extinfo = cur_info.extinfo
            # Update the extinfo, Not replace
            for key in extinfo:
                cur_extinfo[key] = extinfo[key]
            entry = g_Post.update(
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

            ).where(g_Post.uid == uid)
            entry.execute()
        else:

            entry = MInfor.add_meta(uid, data_dic, extinfo)
            return entry
        return uid

    @staticmethod
    def modify_init(uid, data_dic):
        '''
        命令行更新的
        :param uid:
        :param data_dic:
        :return:
        '''
        postinfo = MInfor.get_by_uid(uid)
        entry = g_Post.update(
            time_update=tools.timestamp(),
            date=datetime.now(),
            kind=data_dic['kind'] if 'kind' in data_dic else postinfo.kind,
            keywords=data_dic['keywords'] if 'keywords' in data_dic else postinfo.keywords,
        ).where(g_Post.uid == uid)
        entry.execute()
        return uid

    @staticmethod
    def get_view_count(sig):
        try:
            return g_Post.get(uid=sig).view_count
        except:
            return False

    @staticmethod
    def view_count_increase(uid):
        infor = MInfor.get_by_uid(uid)
        entry = g_Post.update(
            view_count=infor.view_count + 1,
        ).where(g_Post.uid == uid)
        entry.execute()

    @staticmethod
    def get_run_count(sig):
        try:
            return g_Post.get(uid=sig).run_count
        except:
            return False

    @staticmethod
    def run_count_increase(uid):

        entry = g_Post.update(
            run_count=MInfor.get_run_count(uid) + 1,
        ).where(g_Post.uid == uid)
        entry.execute()

    @staticmethod
    def query_random(num=8, kind='2'):

        return g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.valid == 1)
        ).order_by(
            peewee.fn.Random()
        ).limit(num)

    @staticmethod
    def query_cat_random(catid, num=8, kind='2'):
        return g_Post.select().join(g_Post2Tag).where(
            (g_Post.kind == kind) &
            (g_Post.valid == 1) &
            (g_Post2Tag.tag == catid)
        ).order_by(
            peewee.fn.Random()
        ).limit(num)

    @staticmethod
    def query_most(kind='2', num=8, ):
        return g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.valid == 1)
        ).order_by(
            g_Post.view_count.desc()
        ).limit(num)

    @staticmethod
    def query_most_by_cat(num=8, catid=None, kind='2'):
        if catid:
            return g_Post.select().join(g_Post2Tag).where(
                (g_Post.kind == kind) &
                (g_Post.valid == 1) &
                (g_Post2Tag.tag == catid)
            ).order_by(
                g_Post.view_count.desc()
            ).limit(num)
        else:
            return False

    @staticmethod
    def query_least_by_cat(num=8, cat_str=1, kind='2'):
        return g_Post.select().join(g_Post2Tag).where(
            (g_Post.kind == kind) &
            (g_Post.valid == 1) &
            (g_Post2Tag.tag == cat_str)
        ).order_by(
            g_Post.view_count
        ).limit(num)

    @staticmethod
    def get_by_keyword(par2, kind='2'):
        return g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.valid == 1) &
            (g_Post.title.contains(par2))
        ).order_by(
            g_Post.time_update.desc()
        ).limit(20)

    @staticmethod
    def query_recent(num=8, kind='2'):
        return g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.valid == 1)
        ).order_by(
            g_Post.time_update.desc()
        ).limit(num)

    @staticmethod
    def get_by_uid(sig):
        cur_recs = g_Post.select().where(g_Post.uid == sig)
        if cur_recs.count() > 0:
            return cur_recs.get()
        else:
            return None

    @staticmethod
    def query_extinfo_by_cat(cat_id, kind='2'):
        return g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.valid == 1) &
            (g_Post.extinfo['def_cat_uid'] == cat_id)
        ).order_by(
            g_Post.time_update.desc()
        )

    @staticmethod
    def query_by_tagname(tag_name, kind='2'):
        return g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.valid == 1) &
            (g_Post.extinfo['def_tag_arr'].contains(tag_name))
        ).order_by(
            g_Post.time_update.desc()
        )

    @staticmethod
    def get_label_fenye(tag_slug, idx):
        all_list = MInfor.query_by_tagname(tag_slug)

        # 当前分页的记录
        # Todo
        current_list = all_list[(idx - 1) * CMS_CFG['list_num']: idx * CMS_CFG['list_num']]
        return all_list

    @staticmethod
    def query_pager_by_tag(tag, current_page_num=1, kind='2'):
        recs = MInfor.query_by_tagname(
            tag, kind
        ).paginate(
            current_page_num, CMS_CFG['list_num']
        )
        return recs

    @staticmethod
    def add_meta(uid, data_dic, extinfo={}):
        if len(uid) < 4:
            return False
        title = data_dic['title'].strip()
        if len(title) < 2:
            return False
        g_Post.create(
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

    @staticmethod
    def query_under_condition(condition, kind='2'):
        '''
        Get All data of certain kind according to the condition
        :param condition:
        :param kind:
        :return:
        '''
        return g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.valid == 1) &
            (g_Post.extinfo.contains(condition))
        ).order_by(
            g_Post.time_update.desc()
        )

    @staticmethod
    def get_num_condition(con):
        '''
        Return the number under condition.
        :param con:
        :return:
        '''
        return MInfor.query_under_condition(con).count()

    @staticmethod
    def addata_init(data_dic, ext_dic={}):
        if len(data_dic['sig']) < 4:
            return False
        title = data_dic['title'].strip()
        if len(title) < 2:
            return False

        postinfo = MInfor.get_by_uid(data_dic['sig'])
        if postinfo:

            if data_dic['title'] == postinfo.title and data_dic['kind'] == postinfo.kind:
                pass
            else:
                MInfor.modify_init(data_dic['sig'], data_dic)
        else:
            time_stamp = int(time.time())

            g_Post.create(
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

    @staticmethod
    def query_list_pager(con, idx, kind='2'):
        '''
        Get records of certain pager.
        :param con:
        :param idx:
        :param kind:
        :return:
        '''

        all_list = MInfor.query_under_condition(con, kind=kind)
        current_list = all_list[(idx - 1) * CMS_CFG['list_num']: idx * CMS_CFG['list_num']]
        return current_list

    @staticmethod
    def get_cat_recs_count(catid, kind='2'):
        '''
        获取某一分类下的数目
        '''
        condition = {'catid': [catid]}

        db_data = g_Post.select().where(
            (g_Post.kind == kind) &
            (g_Post.valid == 1) &
            (g_Post.extinfo.contains(condition))
        )
        return db_data.count()
