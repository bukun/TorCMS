# -*- coding:utf-8 -*-

'''
Model for Posts.
'''
import time
from datetime import datetime
import peewee
import tornado.escape
from torcms.core import tools
from torcms.model.core_tab import TabPost
from torcms.model.core_tab import TabPost2Tag
from torcms.model.abc_model import Mabc, MHelper
from config import CMS_CFG, DB_CFG


class MPost(Mabc):
    '''
    Model for Posts.
    '''

    def __init__(self):
        super(MPost, self).__init__()

    @staticmethod
    def query_recent_most(num=8, recent=30):
        '''
        Query the records from database that recently updated.
        :param num: the number that will returned.
        :param recent: the number of days recent.
        :return:
        '''
        time_that = int(time.time()) - recent * 24 * 3600
        return TabPost.select().where(TabPost.time_update > time_that).order_by(
            TabPost.view_count.desc()
        ).limit(num)

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        :param uid:
        :return:
        '''
        return MHelper.delete(TabPost, uid)


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

    @staticmethod
    def get_by_uid(uid):
        '''
        return the record by uid
        :param uid:
        :return:
        '''
        return MHelper.get_by_uid(TabPost, uid)

    @staticmethod
    def get_counts():
        '''
        The count in table.
        :return:
        '''
        return TabPost.select().count()

    @staticmethod
    def __update_rating(uid, rating):
        '''
        :param uid:
        :param rating:
        :return:
        '''
        entry = TabPost.update(
            rating=rating
        ).where(TabPost.uid == uid)
        entry.execute()

    @staticmethod
    def __update_kind(uid, kind):
        '''
        update the kind of post.
        :param uid:
        :param kind:
        :return:
        '''

        entry = TabPost.update(
            kind=kind,
        ).where(TabPost.uid == uid)
        entry.execute()
        return True

    @staticmethod
    def update_field(uid, post_id=None):
        if post_id:
            entry = TabPost.update(
                uid=post_id
            ).where(TabPost.uid == uid)
            entry.execute()


    @staticmethod
    def update_cnt(uid, post_data):
        '''
        :param uid:
        :param post_data:
        :return:
        '''

        entry = TabPost.update(
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'].strip()),
            time_update=tools.timestamp(),
        ).where(TabPost.uid == uid)
        entry.execute()

    @staticmethod
    def update_order(uid, order):

        entry = TabPost.update(
            order=order
        ).where(TabPost.uid == uid)
        entry.execute()

    @staticmethod
    def update(uid, post_data, update_time=False):
        '''
        :param uid:
        :param post_data:
        :param update_time:
        :return:
        '''

        title = post_data['title'].strip()
        if len(title) < 2:
            return False
        cnt_html = tools.markdown2html(post_data['cnt_md'])
        try:
            if update_time:
                entry2 = TabPost.update(
                    date=datetime.now(),
                    time_create=tools.timestamp(),
                ).where(TabPost.uid == uid)
                entry2.execute()
        except:
            pass
        cur_rec = MPost.get_by_uid(uid)

        entry = TabPost.update(
            title=title,
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'].strip()),
            cnt_html=cnt_html,
            logo=post_data['logo'],
            order=post_data['order'] if 'order' in post_data else '',
            keywords=post_data['keywords'] if 'keywords' in post_data else '',
            kind=post_data['kind'] if 'kind' in post_data else 1,
            extinfo=post_data['extinfo'] if 'extinfo' in post_data else cur_rec.extinfo,
            time_update=tools.timestamp(),
            valid=1,
        ).where(TabPost.uid == uid)
        entry.execute()

    @staticmethod
    def add_or_update(uid, post_data):
        '''
        :param uid:
        :param post_data:
        :return:
        '''

        cur_rec = MPost.get_by_uid(uid)
        if cur_rec:
            MPost.update(uid, post_data)
        else:
            MPost.create_post(uid, post_data)

    @staticmethod
    def create_post(post_uid, post_data):
        '''
        :param post_uid:
        :param post_data:
        :return:
        '''
        title = post_data['title'].strip()
        if len(title) < 2:
            return False

        cur_rec = MPost.get_by_uid(post_uid)
        if cur_rec:
            return False

        entry = TabPost.create(
            title=title,
            date=datetime.now(),
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'].strip()),
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            uid=post_uid,
            time_create=(post_data['time_create'] if 'time_create' in post_data
                         else tools.timestamp()),
            time_update=(post_data['time_update'] if 'time_update' in post_data
                         else tools.timestamp()),
            user_name=post_data['user_name'],
            view_count=post_data['view_count'] if 'view_count' in post_data else 1,
            logo=post_data['logo'],
            order=post_data['order'] if 'order' in post_data else '',
            keywords=post_data['keywords'] if 'keywords' in post_data else '',
            extinfo=post_data['extinfo'] if 'extinfo' in post_data else {},
            kind=post_data['kind'] if 'kind' in post_data else '1',
            valid=1,
        )
        return entry.uid

    @staticmethod
    def query_cat_random(catid, **kwargs):
        '''
        Get random lists of certain category.
        :param cat_id:
        :param num:
        :return:
        '''
        if 'limit' in kwargs:
            num = kwargs['limit']
        else:
            num = 8
        if catid == '':
            return TabPost.select().order_by(peewee.fn.Random()).limit(num)

        else:
            return TabPost.select().join(TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)).where(
                (TabPost.valid == 1) &
                (TabPost2Tag.tag_id == catid)
            ).order_by(
                peewee.fn.Random()
            ).limit(num)

    @staticmethod
    def query_random(**kwargs):
        '''
        Return the random records of centain kind.
        :param num:
        :param kind:
        :return:
        '''

        if 'limit' in kwargs:
            limit = kwargs['limit']
        elif 'num' in kwargs:
            limit = kwargs['num']
        else:
            limit = 10

        if 'kind' in kwargs:
            kind = kwargs['kind']
        else:
            kind = None

        if kind:
            return TabPost.select().where(
                (TabPost.kind == kind) &
                (TabPost.valid == 1)
            ).order_by(
                peewee.fn.Random()
            ).limit(limit)
        else:
            return TabPost.select().order_by(
                peewee.fn.Random()
            ).limit(limit)

    @staticmethod
    def query_recent(num=8, **kwargs):
        '''
        :param num:
        :param kind:
        :return:
        '''

        if 'kind' in kwargs:
            kind = kwargs['kind']
            return TabPost.select().where((TabPost.kind == kind) & (TabPost.valid == 1)).order_by(
                TabPost.time_update.desc()).limit(num)
        else:
            return TabPost.select().where(
                TabPost.valid == 1
            ).order_by(
                TabPost.time_update.desc()
            ).limit(num)

    @staticmethod
    def query_all(**kwargs):
        '''
            :param kwargs:
            :return:
        '''
        if 'kind' in kwargs:
            kind = kwargs['kind']
        else:
            kind = '1'
        if 'limit' in kwargs:
            limit = kwargs['limit']
        else:
            limit = 10

        return TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.valid == 1)
        ).order_by(
            TabPost.time_update.desc()
        ).limit(limit)

    @staticmethod
    def query_keywords_empty(kind='1'):
        '''
        :param kind:
        :return:
        '''
        return TabPost.select().where((TabPost.kind == kind) & (TabPost.keywords == ''))

    @staticmethod
    def query_recent_edited(timstamp, kind='1'):
        '''
        :param timstamp:
        :param kind:
        :return:
        '''
        return TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.time_update > timstamp)
        ).order_by(TabPost.time_update.desc())

    @staticmethod
    def query_dated(num=8, kind='1'):
        '''
        :param num:
        :param kind:
        :return:
        '''
        return TabPost.select().where(
            TabPost.kind == kind
        ).order_by(
            TabPost.time_update.asc()
        ).limit(num)

    @staticmethod
    def query_most_pic(num, kind='1'):
        '''
        :param num:
        :param kind:
        :return:
        '''
        return TabPost.select().where(
            (TabPost.kind == kind) & (TabPost.logo != "")
        ).order_by(TabPost.view_count.desc()).limit(num)

    @staticmethod
    def query_cat_recent(cat_id, label=None, num=8, kind='1'):
        '''
        :param cat_id:
        :param num:
        :param kind:
        :return:
        '''

        if label:
            return MPost.query_cat_recent_with_label(cat_id, label=label, num=num, kind=kind)
        else:
            return MPost.query_cat_recent_no_label(cat_id, num=num, kind=kind)

    @staticmethod
    def query_cat_recent_with_label(cat_id, label=None, num=8, kind='1'):
        '''
        :param cat_id:
        :param num:
        :param kind:
        :return:
        '''
        return TabPost.select().join(TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)).where(
            (TabPost.kind == kind) &
            (TabPost2Tag.tag_id == cat_id) &
            (TabPost.extinfo['def_tag_arr'].contains(label))
        ).order_by(
            TabPost.time_create.desc()
        ).limit(num)

    @staticmethod
    def query_cat_recent_no_label(cat_id, num=8, kind='1'):
        '''
        :param cat_id:
        :param num:
        :param kind:
        :return:
        '''
        return TabPost.select().join(TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)).where(
            (TabPost.kind == kind) &
            (TabPost2Tag.tag_id == cat_id)
        ).order_by(
            TabPost.time_create.desc()
        ).limit(num)

    @staticmethod
    def query_total_cat_recent(cat_id_arr, label=None, num=8, kind='1'):
        '''
        :param cat_id_arr:   list of categories. ['0101', '0102']
        :param label: the additional label
        :param num:
        :param kind:
        :return:
        '''
        if label:
            return MPost.query_total_cat_recent_with_label(cat_id_arr, label=label, num=num, kind=kind)
        else:
            return MPost.query_total_cat_recent_no_label(cat_id_arr, num=num, kind=kind)

    @staticmethod
    def query_total_cat_recent_with_label(cat_id_arr, label=None, num=8, kind='1'):
        '''
        :param cat_id_arr:   list of categories. ['0101', '0102']
        :param num:
        :param kind:
        :return:
        '''
        return TabPost.select().join(TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)).where(
            (TabPost.kind == kind) &
            (TabPost2Tag.tag_id << cat_id_arr) &  # the "<<" operator signifies an "IN" query
            (TabPost.extinfo['def_tag_arr'].contains(label))
        ).order_by(
            TabPost.time_create.desc()
        ).limit(num)

    @staticmethod
    def query_total_cat_recent_no_label(cat_id_arr, num=8, kind='1'):
        '''
        :param cat_id_arr:   list of categories. ['0101', '0102']
        :param num:
        :param kind:
        :return:
        '''
        return TabPost.select().join(TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)).where(
            (TabPost.kind == kind) &
            (TabPost2Tag.tag_id << cat_id_arr)  # the "<<" operator signifies an "IN" query
        ).order_by(
            TabPost.time_create.desc()
        ).limit(num)

    @staticmethod
    def query_most(num=8, kind='1'):
        '''
        :param num:
        :param kind:
        :return:
        '''

        return TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.valid == 1)
        ).order_by(
            TabPost.view_count.desc()
        ).limit(num)

    @staticmethod
    def update_misc(uid, **kwargs):
        '''
        update rating, kind, or count
        :param uid:
        :param kwargs:
        :return:
        '''
        if 'rating' in kwargs:
            MPost.__update_rating(uid, kwargs['rating'])
        elif 'kind' in kwargs:
            MPost.__update_kind(uid, kwargs['kind'])
        elif 'keywords' in kwargs:
            MPost.__update_keywords(uid, kwargs['keywords'])
        elif 'count' in kwargs:
            MPost.__update_view_count(uid)

    @staticmethod
    def __update_view_count(uid):
        '''
        :param uid:
        :return:
        '''
        entry = TabPost.update(view_count=TabPost.view_count + 1).where(TabPost.uid == uid)
        try:
            entry.execute()
            return True
        except:
            return False

    @staticmethod
    def __update_keywords(uid, inkeywords):
        '''
        :param uid:
        :param inkeywords:
        :return:
        '''
        entry = TabPost.update(keywords=inkeywords).where(TabPost.uid == uid)
        entry.execute()

    @staticmethod
    def get_next_record(in_uid, kind='1'):
        '''
        :param in_uid:
        :param kind:
        :return:
        '''
        current_rec = MPost.get_by_uid(in_uid)
        query = TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.time_create < current_rec.time_create)
        ).order_by(TabPost.time_create.desc())
        if query.count() == 0:
            return None
        else:
            return query.get()

    @staticmethod
    def get_previous_record(in_uid, kind='1'):
        '''
        :param in_uid:
        :param kind:
        :return:
        '''
        current_rec = MPost.get_by_uid(in_uid)
        query = TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.time_create > current_rec.time_create)
        ).order_by(TabPost.time_create)
        if query.count() == 0:
            return None
        else:
            return query.get()

    @staticmethod
    def get_all(kind='2'):
        return TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.valid == 1)
        ).order_by(
            TabPost.time_update.desc()
        )

    @staticmethod
    def update_jsonb(uid, extinfo):
        cur_extinfo = MPost.get_by_uid(uid).extinfo
        for key in extinfo:
            cur_extinfo[key] = extinfo[key]
        entry = TabPost.update(
            extinfo=cur_extinfo,
        ).where(TabPost.uid == uid)
        entry.execute()
        return uid

    @staticmethod
    def modify_meta(uid, data_dic, extinfo=None):
        '''
        手工修改的。
        :param uid:
        :param data_dic:
        :return:
        '''
        if extinfo is None:
            extinfo = {}
        title = data_dic['title'].strip()
        if len(title) < 2:
            return False

        cur_info = MPost.get_by_uid(uid)
        if cur_info:
            if DB_CFG['kind'] == 's':
                entry = TabPost.update(
                    title=title,
                    user_name=data_dic['user_name'],
                    keywords='',
                    time_create=tools.timestamp(),
                    time_update=tools.timestamp(),
                    date=datetime.now(),
                    cnt_md=data_dic['cnt_md'],
                    logo=data_dic['logo'],
                    order=data_dic['order'],
                    cnt_html=tools.markdown2html(data_dic['cnt_md']),
                    valid=data_dic['valid']
                ).where(TabPost.uid == uid)
                entry.execute()
            else:
                cur_extinfo = cur_info.extinfo
                # Update the extinfo, Not replace
                for key in extinfo:
                    cur_extinfo[key] = extinfo[key]

                entry = TabPost.update(
                    title=title,
                    user_name=data_dic['user_name'],
                    keywords='',
                    time_create=tools.timestamp(),
                    time_update=tools.timestamp(),
                    date=datetime.now(),
                    cnt_md=data_dic['cnt_md'],
                    logo=data_dic['logo'],
                    order=data_dic['order'] if 'order' in data_dic else '',
                    cnt_html=tools.markdown2html(data_dic['cnt_md']),
                    extinfo=cur_extinfo,
                    valid=data_dic['valid']
                ).where(TabPost.uid == uid)
                entry.execute()
        else:
            return MPost.add_meta(uid, data_dic, extinfo)
        return uid

    @staticmethod
    def modify_init(uid, data_dic):
        '''
        命令行更新的
        :param uid:
        :param data_dic:
        :return:
        '''
        postinfo = MPost.get_by_uid(uid)
        entry = TabPost.update(
            time_update=tools.timestamp(),
            date=datetime.now(),
            kind=data_dic['kind'] if 'kind' in data_dic else postinfo.kind,
            keywords=data_dic['keywords'] if 'keywords' in data_dic else postinfo.keywords,
        ).where(TabPost.uid == uid)
        entry.execute()
        return uid

    @staticmethod
    def get_view_count(sig):
        try:
            return TabPost.get(uid=sig).view_count
        except:
            return False

    @staticmethod
    def query_most_by_cat(num=8, catid=None, kind='2'):
        if catid:
            return TabPost.select().join(TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)).where(
                (TabPost.kind == kind) &
                (TabPost.valid == 1) &
                (TabPost2Tag.tag_id == catid)
            ).order_by(
                TabPost.view_count.desc()
            ).limit(num)
        else:
            return False

    @staticmethod
    def query_least_by_cat(num=8, cat_str=1, kind='2'):
        return TabPost.select().join(TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)).where(
            (TabPost.kind == kind) &
            (TabPost.valid == 1) &
            (TabPost2Tag.tag_id == cat_str)
        ).order_by(
            TabPost.view_count
        ).limit(num)

    @staticmethod
    def get_by_keyword(par2, kind='2'):
        return TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.valid == 1) &
            (TabPost.title.contains(par2))
        ).order_by(
            TabPost.time_update.desc()
        ).limit(20)

    @staticmethod
    def query_extinfo_by_cat(cat_id, kind='2'):
        return TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.valid == 1) &
            (TabPost.extinfo['def_cat_uid'] == cat_id)
        ).order_by(
            TabPost.time_update.desc()
        )

    @staticmethod
    def query_by_tagname(tag_name, kind='2'):
        return TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.valid == 1) &
            (TabPost.extinfo['def_tag_arr'].contains(tag_name))
        ).order_by(
            TabPost.time_update.desc()
        )

    @staticmethod
    def get_label_fenye(tag_slug, idx):
        all_list = MPost.query_by_tagname(tag_slug)

        # 当前分页的记录
        # Todo
        # current_list = all_list[(idx - 1) * CMS_CFG['list_num']: idx * CMS_CFG['list_num']]
        return all_list

    @staticmethod
    def query_pager_by_tag(tag, current_page_num=1, kind='2'):
        recs = MPost.query_by_tagname(
            tag, kind
        ).paginate(
            current_page_num, CMS_CFG['list_num']
        )
        return recs

    @staticmethod
    def add_meta(uid, data_dic, extinfo=None):
        if extinfo is None:
            extinfo = {}
        if len(uid) < 4:
            return False
        title = data_dic['title'].strip()
        if len(title) < 2:
            return False
        TabPost.create(
            uid=uid,
            title=title,
            keywords='',
            time_create=tools.timestamp(),
            time_update=tools.timestamp(),
            create_time=tools.timestamp(),
            date=datetime.now(),
            cnt_md=data_dic['cnt_md'].strip(),
            logo=data_dic['logo'].strip(),
            order=data_dic['order'] if 'order' in data_dic else '',
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
        if DB_CFG['kind'] == 's':
            return TabPost.select().where((TabPost.kind == kind) & (TabPost.valid == 1)).order_by(
                TabPost.time_update.desc())
        else:

            return TabPost.select().where(
                (TabPost.kind == kind) & (TabPost.valid == 1) & (TabPost.extinfo.contains(condition))
            ).order_by(TabPost.time_update.desc())

    @staticmethod
    def get_num_condition(con):
        '''
        Return the number under condition.
        :param con:
        :return:
        '''
        return MPost.query_under_condition(con).count()

    @staticmethod
    def addata_init(data_dic, ext_dic=None):
        if ext_dic is None:
            ext_dic = {}

        if len(data_dic['sig']) < 4:
            return False
        title = data_dic['title'].strip()
        if len(title) < 2:
            return False

        postinfo = MPost.get_by_uid(data_dic['sig'])
        if postinfo:

            if data_dic['title'] == postinfo.title and data_dic['kind'] == postinfo.kind:
                pass
            else:
                MPost.modify_init(data_dic['sig'], data_dic)
        else:
            time_stamp = int(time.time())

            TabPost.create(
                uid=data_dic['sig'],
                title=data_dic['title'],
                create_time=time_stamp,
                time_update=time_stamp,
                cnt_md=data_dic['cnt_md'],
                cnt_html=data_dic['cnt_html'],
                date=datetime.now(),
                keywords='',
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

        all_list = MPost.query_under_condition(con, kind=kind)
        return all_list[(idx - 1) * CMS_CFG['list_num']: idx * CMS_CFG['list_num']]
