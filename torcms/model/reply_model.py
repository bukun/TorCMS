# -*- coding:utf-8 -*-
'''
Data model for reply.
'''

import datetime

import tornado.escape

from config import CMS_CFG
from torcms.core import tools
from torcms.model.core_tab import TabReply, TabUser2Reply
from torcms.model.replyid_model import TabReplyid


class MReply():
    @staticmethod
    def get_by_uid(uid):
        recs = TabReply.select().where(TabReply.uid == uid)
        if recs.count():
            return recs.get()
        return None

    @staticmethod
    def update_vote(reply_id, count):
        entry = TabReply.update(vote=count).where(TabReply.uid == reply_id)
        entry.execute()

    @staticmethod
    def create_reply(post_data, extinfo=None):
        '''
        Create the reply.
        '''
        if extinfo:
            pass
        else:
            extinfo = {}
        uid = tools.get_uuid()
        TabReply.create(
            uid=uid,
            post_id=post_data['post_id'],
            user_name=post_data['user_name'],
            user_id=post_data['user_id'],
            category=post_data['category'] if 'category' in post_data else '0',
            timestamp=tools.timestamp(),
            date=datetime.datetime.now(),
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_reply']),
            cnt_html=tools.markdown2html(post_data['cnt_reply']),
            vote=0,
            extinfo=extinfo)
        return uid

    @staticmethod
    def query_by_post(postid):
        '''
        Get reply list of certain post.
        '''
        return TabReply.select().where((TabReply.post_id == postid)
                                       & (TabReply.category != '1')).order_by(
            TabReply.timestamp.desc())

    @staticmethod
    def get_by_zan(reply_id):
        return TabUser2Reply.select().where(
            TabUser2Reply.reply_id == reply_id).count()

    @staticmethod
    def query_all():
        return TabReply.select().order_by(TabReply.timestamp.desc())

    @staticmethod
    def delete(del_id):
        return TabReply.delete().where(TabReply.post_id == del_id)

    @staticmethod
    def count_of_certain(ext_field=None):
        '''
        Get the count of certain kind.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        if ext_field:
            return TabReply.select().where(
                TabReply.extinfo['ext_field'] == str(ext_field)
            ).count(None)
        else:
            return TabReply.select().count(None)

    @staticmethod
    def total_number():
        '''
        Return the number.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return TabReply.select().count(None)

    @staticmethod
    def query_pager(current_page_num=1, ext_field=''):
        '''
        Query pager
        '''
        if ext_field:
            return TabReply.select().where(
                TabReply.category == '0' and TabReply.extinfo['ext_field'] == ext_field).paginate(current_page_num,
                                                                                                  CMS_CFG['list_num'])
        else:
            return TabReply.select().where(TabReply.category == '0').paginate(current_page_num,
                                                                              CMS_CFG['list_num'])

    @staticmethod
    def modify_by_uid(pid, post_data):
        rec = MReply.get_by_uid(pid)
        if rec:
            entry = TabReply.update(
                user_name=post_data['user_name'],
                user_id=post_data['user_id'],
                category=post_data['category'],
                timestamp=tools.timestamp(),
                date=datetime.datetime.now(),
                cnt_md=tornado.escape.xhtml_escape(post_data['cnt_reply']),
                cnt_html=tools.markdown2html(post_data['cnt_reply']),
            ).where(TabReply.uid == pid)
            entry.execute()
            return pid

    @staticmethod
    def delete_by_uid(del_id):
        delcom = TabReplyid.delete().where(TabReplyid.reply1 == del_id)
        delcom.execute()
        entry = TabReply.delete().where(TabReply.uid == del_id)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False
