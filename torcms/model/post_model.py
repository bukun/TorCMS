# -*- coding:utf-8 -*-
'''
Model for Posts.
'''
import time
from datetime import datetime

import peewee
import tornado.escape

from config import CMS_CFG
from torcms.core.tools import logger
from torcms.core import tools
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import (TabCollect, TabEvaluation, TabPost,
                                   TabPost2Tag, TabPostHist, TabRating, TabRel,
                                   TabReply, TabUsage, TabUser2Reply)


class MPost():
    '''
    Model for Posts.
    '''

    @staticmethod
    def query_recent_most(num=8, recent=30):
        '''
        Query the records from database that recently updated.
        :param num: the number that will returned.
        :param recent: the number of days recent.
        '''
        time_that = int(time.time()) - recent * 24 * 3600
        return TabPost.select().where(
            (TabPost.time_update > time_that) & (TabPost.valid == 1)
        ).order_by(
            TabPost.view_count.desc()
        ).limit(num)

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''

        q_u1 = TabPostHist.delete().where(TabPostHist.post_id == uid)
        q_u1.execute()
        q_u2 = TabRel.delete().where(TabRel.post_f_id == uid
                                     or TabRel.post_t_id == uid)
        q_u2.execute()
        q_u3 = TabCollect.delete().where(TabCollect.post_id == uid)
        q_u3.execute()
        q_u4 = TabPost2Tag.delete().where(TabPost2Tag.post_id == uid)
        q_u4.execute()
        q_u5 = TabUsage.delete().where(TabUsage.post_id == uid)
        q_u5.execute()

        reply_arr = []
        for reply in TabUser2Reply.select().where(
                TabUser2Reply.reply_id == uid):
            reply_arr.append(reply.reply_id.uid)

        q_u6 = TabUser2Reply.delete().where(TabUser2Reply.reply_id == uid)
        q_u6.execute()

        for replyid in reply_arr:
            TabReply.delete().where(TabReply.uid == replyid).execute()

        q_u7 = TabEvaluation.delete().where(TabEvaluation.post_id == uid)
        q_u7.execute()
        q_u8 = TabRating.delete().where(TabRating.post_id == uid)
        q_u8.execute()
        return MHelper.delete(TabPost, uid)

    @staticmethod
    def get_by_uid(uid):
        '''
        return the record by uid
        '''
        return MHelper.get_by_uid(TabPost, uid)

    @staticmethod
    def get_counts():
        '''
        The count in table.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return TabPost.select().count(None)

    @staticmethod
    def __update_rating(uid, rating):
        '''
        Update the rating for post.
        '''
        entry = TabPost.update(rating=rating).where(TabPost.uid == uid)
        entry.execute()

    @staticmethod
    def __update_kind(uid, kind):
        '''
        update the kind of post.
        '''

        entry = TabPost.update(kind=kind).where(TabPost.uid == uid)
        entry.execute()
        return True

    @staticmethod
    def update_cnt(uid, post_data):
        '''
        update content.
        '''

        entry = TabPost.update(
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'].strip()),
            time_update=tools.timestamp()
        ).where(TabPost.uid == uid)
        entry.execute()

    @staticmethod
    def update_order(uid, order):
        '''
        Update the order of the posts.
        '''
        entry = TabPost.update(order=order).where(TabPost.uid == uid)
        entry.execute()

    @staticmethod
    def query_cat_random(catid, **kwargs):
        '''
        Get random lists of certain category.
        '''
        num = kwargs.get('limit', 8)
        if catid == '':
            rand_recs = TabPost.select().where(
                TabPost.valid == 1
            ).order_by(
                peewee.fn.Random()
            ).limit(num)
        else:
            rand_recs = TabPost.select().join(
                TabPost2Tag,
                on=(TabPost.uid == TabPost2Tag.post_id)
            ).where(
                (TabPost.valid == 1) &
                (TabPost2Tag.tag_id == catid)
            ).order_by(peewee.fn.Random()).limit(num)
        return rand_recs

    @staticmethod
    def query_random(**kwargs):
        '''
        Return the random records of centain kind.
        '''

        if 'limit' in kwargs:
            limit = kwargs['limit']
        elif 'num' in kwargs:
            limit = kwargs['num']
        else:
            limit = 10

        kind = kwargs.get('kind', None)

        if kind:
            rand_recs = TabPost.select().where(
                (TabPost.kind == kind) &
                (TabPost.valid == 1)
            ).order_by(peewee.fn.Random()).limit(limit)
        else:
            rand_recs = TabPost.select().where(
                TabPost.valid == 1
            ).order_by(peewee.fn.Random()).limit(limit)
        return rand_recs

    @staticmethod
    def query_recent(num=8, **kwargs):
        '''
        获取最近发布，或更新的Post列表
        '''
        order_by_create = kwargs.get('order_by_create', False)
        kind = kwargs.get('kind', None)
        if order_by_create:
            if kind:
                recent_recs = TabPost.select().where(
                    (TabPost.kind == kind) & (TabPost.valid == 1)
                ).order_by(
                    TabPost.time_create.desc()
                ).limit(num)
            else:
                recent_recs = TabPost.select().where(
                    TabPost.valid == 1
                ).order_by(
                    TabPost.time_create.desc()
                ).limit(num)
        else:
            if kind:
                recent_recs = TabPost.select().where(
                    (TabPost.kind == kind) & (TabPost.valid == 1)
                ).order_by(
                    TabPost.time_update.desc()).limit(num)
            else:
                recent_recs = TabPost.select().where(
                    TabPost.valid == 1
                ).order_by(
                    TabPost.time_update.desc()
                ).limit(num)
        return recent_recs

    @staticmethod
    def query_all(**kwargs):
        '''
        query all the posts.
        '''
        kind = kwargs.get('kind', '1')
        limit = kwargs.get('limit', 10)

        return TabPost.select().where(
            (TabPost.kind == kind) & (TabPost.valid == 1)
        ).order_by(
            TabPost.time_update.desc()
        ).limit(limit)

    @staticmethod
    def query_keywords_empty(kind='1'):
        '''
        Query keywords, empty.
        '''
        return TabPost.select().where(
            (TabPost.kind == kind) & (TabPost.keywords == '')
        )

    @staticmethod
    def query_recent_edited(timstamp, kind='1'):
        '''
        获取最近更新的Post，以时间戳为条件
        '''
        return TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.time_update > timstamp)
        ).order_by(
            TabPost.time_update.desc()
        )

    @staticmethod
    def query_dated(num=8, kind='1'):
        '''
        获取久未更新的Post列表。
        '''
        return TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.valid == 1)
        ).order_by(
            TabPost.time_update.asc()
        ).limit(num)

    @staticmethod
    def query_most_pic(num, kind='1'):
        '''
        Query most pics.
        '''
        return TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.logo != "") &
            (TabPost.valid == 1)
        ).order_by(
            TabPost.view_count.desc()).limit(num)

    @staticmethod
    def query_cat_recent(cat_id, label=None, num=8, kind='1', order=False):
        '''
        Query recent posts of catalog.
        '''

        if label:
            recent_recs = MPost.query_cat_recent_with_label(
                cat_id,
                label=label,
                num=num,
                kind=kind,
                order=order
            )
        else:
            recent_recs = MPost.query_cat_recent_no_label(
                cat_id,
                num=num,
                kind=kind,
                order=order
            )
        return recent_recs

    @staticmethod
    def query_by_tag(cat_id, kind='1'):
        '''
        Query posts of catalog.
        '''

        return TabPost.select().join(
            TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)
        ).where(
            (TabPost.kind == kind) & (TabPost2Tag.tag_id == cat_id) & (TabPost.valid == 1)
        ).order_by(
            TabPost.time_create.desc()
        )

    @staticmethod
    def query_by_parid(par_id, kind='9'):
        '''
        Query recent posts of catalog.

        '''

        return TabPost.select().join(
            TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)
        ).where(
            (TabPost.kind == kind) &
            (TabPost2Tag.par_id == par_id) &
            (TabPost.valid == 1)
        ).order_by(
            TabPost.time_create.desc()
        )

    @staticmethod
    def query_cat_recent_with_label(cat_id,
                                    label=None,
                                    num=8,
                                    kind='1',
                                    order=False):
        '''
        query_cat_recent_with_label
        '''
        if order:
            sort_criteria = TabPost.order.asc()
        else:
            sort_criteria = TabPost.time_update.desc()

        return TabPost.select().join(
            TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)).where(
            (TabPost.kind == kind) & (TabPost2Tag.tag_id == cat_id)
            & (TabPost.valid == 1)
            & (TabPost.extinfo['def_tag_arr'].contains(label))).order_by(
            sort_criteria).limit(num)

    @staticmethod
    def query_cat_recent_no_label(cat_id, num=8, kind='1', order=False):
        '''
        query_cat_recent_no_label
        '''
        if order:
            sort_criteria = TabPost.order.asc()
        else:
            sort_criteria = TabPost.time_update.desc()

        return TabPost.select().join(
            TabPost2Tag, on=(TabPost.uid == TabPost2Tag.post_id)).where(
            (TabPost.kind == kind) & (TabPost2Tag.tag_id == cat_id)
            & (TabPost.valid == 1)).order_by(sort_criteria).limit(num)

    @staticmethod
    def query_total_cat_recent(cat_id_arr, label=None, num=8, kind='1'):
        '''
        :param cat_id_arr:   list of categories. ['0101', '0102']
        :param label: the additional label
        '''
        if label:
            return MPost.__query_with_label(cat_id_arr,
                                            label=label,
                                            num=num,
                                            kind=kind)
        return MPost.query_total_cat_recent_no_label(cat_id_arr,
                                                     num=num,
                                                     kind=kind)

    @staticmethod
    def __query_with_label(cat_id_arr, label=None, num=8, kind='1'):
        '''
        :param cat_id_arr:   list of categories. ['0101', '0102']
        '''
        return TabPost.select().join(
            TabPost2Tag,
            on=(TabPost.uid == TabPost2Tag.post_id
                )).where((TabPost.kind == kind)
                         & (TabPost2Tag.tag_id << cat_id_arr)
                         &  # the "<<" operator signifies an "IN" query
                         (TabPost.extinfo['def_tag_arr'].contains(label)
                          & (TabPost.valid == 1))).order_by(
            TabPost.time_create.desc()).limit(num)

    @staticmethod
    def query_total_cat_recent_no_label(cat_id_arr, num=8, kind='1'):
        '''
        :param cat_id_arr:   list of categories. ['0101', '0102']
        '''
        return TabPost.select().join(
            TabPost2Tag,
            on=(TabPost.uid == TabPost2Tag.post_id
                )).where((TabPost.kind == kind)
                         & (TabPost2Tag.tag_id << cat_id_arr)
                         &  # the "<<" operator signifies an "IN" query
                         (TabPost.valid == 1)).order_by(
            TabPost.time_create.desc()).limit(num)

    @staticmethod
    def query_most(num=8, kind='1'):
        '''
        Query most viewed.
        '''
        return TabPost.select().where((TabPost.kind == kind)
                                      & (TabPost.valid == 1)).order_by(
            TabPost.view_count.desc()).limit(num)

    @staticmethod
    def update_misc(uid, **kwargs):
        '''
        update rating, kind, or count
        '''
        if 'rating' in kwargs:
            MPost.__update_rating(uid, kwargs['rating'])
        if 'kind' in kwargs:
            MPost.__update_kind(uid, kwargs['kind'])
        if 'keywords' in kwargs:
            MPost.__update_keywords(uid, kwargs['keywords'])
        if 'count' in kwargs:
            MPost.__update_view_count(uid)

    @staticmethod
    def __update_view_count(uid):
        '''
        '''
        entry = TabPost.update(
            view_count=TabPost.view_count + 1
        ).where(TabPost.uid == uid)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def __update_keywords(uid, inkeywords):
        '''
        Update with keywords.
        '''
        entry = TabPost.update(keywords=inkeywords).where(TabPost.uid == uid)
        entry.execute()

    @staticmethod
    def get_next_record(in_uid, kind='1'):
        '''
        Get next record by time_create.
        '''
        current_rec = MPost.get_by_uid(in_uid)
        recs = TabPost.select().where(
            (TabPost.kind == kind)
            & (TabPost.time_create < current_rec.time_create)
            & (TabPost.valid == 1)).order_by(TabPost.time_create.desc())
        if recs.count():
            return recs.get()
        return None

    @staticmethod
    def get_previous_record(in_uid, kind='1'):
        '''
        Get previous record by time_create.
        '''
        current_rec = MPost.get_by_uid(in_uid)
        recs = TabPost.select().where(
            (TabPost.kind == kind)
            & (TabPost.time_create > current_rec.time_create)
            & (TabPost.valid == 1)).order_by(TabPost.time_create)
        if recs.count():
            return recs.get()
        return None

    @staticmethod
    def get_all(kind='2'):
        '''
        Get All the records.
        '''
        return TabPost.select().where(
            (TabPost.kind == kind) & (TabPost.valid == 1)
        ).order_by(TabPost.time_update.desc())

    @staticmethod
    def update_jsonb(uid, extinfo):
        '''
        Update the json.
        '''
        cur_extinfo = MPost.get_by_uid(uid).extinfo
        cur_extinfo.update(extinfo)
        entry = TabPost.update(extinfo=cur_extinfo).where(TabPost.uid == uid)
        entry.execute()
        return uid

    @staticmethod
    def add_or_update(uid, post_data, update_time=None):
        '''
        Add or update the post.
        '''
        uid = MPost.add_or_update_post(uid, post_data)
        return uid

    @staticmethod
    def add_or_update_post(uid, post_data, extinfo=None):
        '''
        update meta of the rec.
        '''
        if len(uid) < 4:
            return False
        title = post_data['title'].strip()
        if len(title) < 2:
            return False
        post_data['title'] = title

        post_extdata = post_data.get('extinfo', {})
        if extinfo:
            post_extdata.update(extinfo)

        cur_info = MPost.get_by_uid(uid)

        if cur_info:
            cur_extinfo = cur_info.extinfo
            # Update the extinfo, Not replace
            cur_extinfo.update(post_extdata)
            cur_extinfo['def_editor_name'] = post_data['user_name'].strip()

            MPost.__update_post(uid, post_data, cur_extinfo)
        else:
            MPost.__add_post(uid, post_data, post_extdata)
        return uid

    #
    # @staticmethod
    # def __update_post(uid, post_data, update_time=False):
    #     '''
    #     参数 `update_time` ， 是否更新时间。对于导入的数据，有时不需要更新。
    #     '''
    #
    #
    #     # cnt_html = tools.markdown2html(post_data['cnt_md'])
    #
    #     cur_rec = MPost.get_by_uid(uid)
    #
    #     entry = TabPost.update(
    #         # title='',
    #         # user_name=post_data['user_name'],
    #         # cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'].strip()),
    #         # memo=post_data['memo'] if 'memo' in post_data else '',
    #         # cnt_html=cnt_html,
    #         # logo=post_data['logo'],
    #         # order=post_data['order'] if 'order' in post_data else '',
    #
    #         # kind=post_data['kind'] if 'kind' in post_data else 1,
    #         # extinfo=post_data['extinfo'] if 'extinfo' in post_data else cur_rec.extinfo,
    #         # time_update=tools.timestamp(),
    #         # valid=post_data.get('valid', 1)
    #     ).where(TabPost.uid == uid)
    #
    #     entry.execute()
    #     return uid

    @staticmethod
    def __update_post(uid, post_data, cur_extinfo):
        '''
        注意，不更新 kind
        '''
        entry = TabPost.update(
            title=post_data['title'].strip(),
            # user_name=data_dic['user_name'],
            keywords=post_data['keywords'] if 'keywords' in post_data else '',
            time_update=tools.timestamp(),
            date=datetime.now(),
            # cnt_md=post_data['cnt_md'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'].strip()),
            memo=post_data.get('memo', ''),
            logo=post_data.get('logo', '').strip(),
            order=post_data.get('order', ''),
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            extinfo=cur_extinfo,
            valid=post_data.get('valid', 1)
        ).where(TabPost.uid == uid)
        entry.execute()

    @staticmethod
    def query_most_by_cat(num=8, catid=None, kind='2'):
        '''
        获取某类别下最多访问的列表
        '''
        if catid:
            return TabPost.select().join(
                TabPost2Tag,
                on=(TabPost.uid == TabPost2Tag.post_id
                    )).where((TabPost.kind == kind) & (TabPost.valid == 1)
                             & (TabPost2Tag.tag_id == catid)).order_by(
                TabPost.view_count.desc()).limit(num)
        return False

    @staticmethod
    def query_least_by_cat(num=8, cat_str=1, kind='2'):
        '''
        获取某类别下最少访问的列表
        '''
        return TabPost.select().join(
            TabPost2Tag,
            on=(TabPost.uid == TabPost2Tag.post_id
                )).where((TabPost.kind == kind) & (TabPost.valid == 1)
                         & (TabPost2Tag.tag_id == cat_str)).order_by(
            TabPost.view_count).limit(num)

    @staticmethod
    def get_by_keyword(par2, kind='2'):
        '''
        根据关键字对标题进行检索
        '''
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
    def query_by_extinfo(key='', val=''):
        '''
        根据扩展字段查询
        '''
        return TabPost.select().where(
            (TabPost.extinfo[key] == val)
        ).order_by(TabPost.time_update.desc())

    @staticmethod
    def query_by_tagname(tag_name, kind='2'):
        '''
        根据标签进行查询
        '''
        return TabPost.select().where(
            (TabPost.kind == kind) &
            (TabPost.valid == 1) &
            (TabPost.extinfo['def_tag_arr'].contains(tag_name))
        ).order_by(
            TabPost.time_update.desc())

    @staticmethod
    def query_pager_by_tag(tag, current_page_num=1, kind='2'):
        recs = MPost.query_by_tagname(
            tag,
            kind
        ).paginate(
            current_page_num,
            CMS_CFG['list_num']
        )
        return recs

    @staticmethod
    def __add_post(uid, post_data, extinfo=None):
        '''
        adding meta for post.
        '''

        if extinfo is None:
            extinfo = {}

        TabPost.create(
            uid=uid,
            title=post_data['title'],
            keywords=post_data.get('keywords', ''),
            time_create=post_data.get('time_create', tools.timestamp()),
            time_update=post_data.get('time_update', tools.timestamp()),
            date=datetime.now(),
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'].strip()),
            memo=post_data.get('memo', ''),
            logo=post_data.get('logo', '').strip(),
            order=post_data.get('order', ''),
            state=post_data.get('state', 'a000'),
            cnt_html=tools.markdown2html(post_data['cnt_md']),
            view_count=post_data.get('view_count', 1),
            extinfo=extinfo,
            user_name=post_data['user_name'],
            valid=post_data.get('valid', 1),
            kind=post_data.get('kind', '1'),
        )
        return uid

    @staticmethod
    def query_under_condition(condition, kind='9', sort_option=''):
        '''
        Get All data of certain kind according to the condition
        '''

        logger.info(f'TorCMS:: condition: {condition}')

        if sort_option:
            if sort_option == 'time_update':
                sort_criteria = TabPost.time_update.desc()
            elif sort_option == 'time_create':
                sort_criteria = TabPost.time_create.desc()
            elif sort_option == 'access_1d':
                sort_criteria = TabPost.access_1d.desc()
            elif sort_option == 'access_7d':
                sort_criteria = TabPost.access_7d.desc()
            elif sort_option == 'access_30d':
                sort_criteria = TabPost.access_30d.desc()
            else:
                sort_criteria = TabPost.view_count.desc()
        else:
            sort_criteria = TabPost.time_update.desc()

        return TabPost.select().where(
            (TabPost.kind == kind) & (TabPost.valid == 1) & TabPost.extinfo.contains(condition)
        ).order_by(sort_criteria)

    @staticmethod
    def get_num_condition(con):
        '''
        Return the number under condition.
        '''
        return MPost.query_under_condition(con).count()

    @staticmethod
    def query_list_pager(con, idx, kind='2', sort_option='', list_num=''):
        '''
        Get records of certain pager.
        '''

        if sort_option:
            recs = MPost.query_under_condition(con,
                                               kind=kind,
                                               sort_option=sort_option)
        else:
            recs = MPost.query_under_condition(con, kind=kind)
        if list_num:
            list_num = list_num
        else:
            list_num = CMS_CFG['list_num']

        return recs[(int(idx) - 1) * int(list_num):int(idx) * int(list_num)]

    @staticmethod
    def count_of_certain_kind(kind):
        '''
        Get the count of certain kind.
        '''

        recs = TabPost.select().where((TabPost.kind == kind)
                                      & (TabPost.valid == 1))

        return recs.count()

    @staticmethod
    def total_number(kind):
        '''
        Return the number of certian slug.
        '''
        return TabPost.select().where((TabPost.kind == kind)
                                      & (TabPost.valid == 1)).count()

    @staticmethod
    def query_pager_by_slug(kind, current_page_num=1):
        '''
        Query pager
        '''
        return TabPost.select().where((TabPost.kind == kind)
                                      & (TabPost.valid == 1)).order_by(
            TabPost.time_create.desc()).paginate(
            current_page_num,
            CMS_CFG['list_num'])

    @staticmethod
    def query_access(kind, day_sig, limit=10):
        '''
        返回最近几天访问的列表。
        day_sig为标识 : 'd' 为 近24小时， 'w'为近1击， 'm' 为近1月
        '''
        if day_sig == 'd':
            return TabPost.select().where(TabPost.kind == kind).order_by(
                TabPost.access_1d.desc()).limit(limit)
        elif day_sig == 'w':
            return TabPost.select().where(TabPost.kind == kind).order_by(
                TabPost.access_7d.desc()).limit(limit)
        elif day_sig == 'm':
            return TabPost.select().where(TabPost.kind == kind).order_by(
                TabPost.access_30d.desc()).limit(limit)

        return None

    @staticmethod
    def nullify(uid):
        '''
        使无效
        '''

        entry = TabPost.update(valid=0).where(TabPost.uid == uid)

        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def update_valid(uid):

        entry = TabPost.update(valid=1).where(TabPost.uid == uid)

        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def update_state(uid, state):
        '''
        更新审核状态
        '''
        try:
            entry = TabPost.update(
                state=state
            ).where(TabPost.uid == uid)
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def query_by_state(state, kind, current_page_num=1):
        if state:
            recent_recs = TabPost.select().where(
                TabPost.state.endswith(state) & (TabPost.kind == kind)
            ).order_by(
                TabPost.time_create.desc()
            ).paginate(
                current_page_num,
                CMS_CFG['list_num']
            )
        else:
            recent_recs = TabPost.select().where(TabPost.kind == kind).order_by(
                TabPost.time_create.desc()).paginate(
                current_page_num,
                CMS_CFG['list_num'])

        return recent_recs

    @staticmethod
    def count_of_certain_by_state(state, kind):
        if state:
            recs = TabPost.select().where(
                TabPost.state.endswith(state) & (TabPost.kind == kind)
            )
        else:
            recs = TabPost.select().where(TabPost.kind == kind)
        return recs.count()

    @staticmethod
    def query_by_username(username, state, kind, current_page_num=1):
        if state:
            recent_recs = TabPost.select().where(
                (TabPost.user_name == username) &
                (TabPost.state.endswith(state)) &
                (TabPost.kind == kind)
            ).order_by(
                TabPost.time_create.desc()
            ).paginate(
                current_page_num,
                CMS_CFG['list_num']
            )
        else:
            recent_recs = TabPost.select().where(
                (TabPost.user_name == username) & (TabPost.kind == kind)
            ).order_by(
                TabPost.time_create.desc()
            ).paginate(
                current_page_num,
                CMS_CFG['list_num']
            )
        return recent_recs

    @staticmethod
    def count_of_certain_by_username(username, state, kind):
        if state:
            recs = TabPost.select().where(
                (TabPost.user_name == username) &
                (TabPost.state.endswith(state)) &
                (TabPost.kind == kind)
            )
        else:
            recs = TabPost.select().where(
                (TabPost.user_name == username) & (TabPost.kind == kind))
        return recs.count()
