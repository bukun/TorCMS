# -*- coding:utf-8 -*-

import time
from datetime import datetime

import tornado.escape
import tornado.web

from torcms.core import tools
from torcms.model.abc_model import  MHelper
from torcms.model.core_tab import TabPost as TabApp
from torcms.model.post_model import MPost
from torcms.model.reply_model import MReply
from torcms_app.model.ext import ExtabCalcInfo


class MCalcInfo():
    '''
    For App infor.
    '''

    def __init__(self):
        try:
            ExtabCalcInfo.create_table()
        except:
            pass

    @staticmethod
    def get_by_uid(uid):
        return MHelper.get_by_uid(ExtabCalcInfo, uid)

    @staticmethod
    def create_info(post_data):

        ExtabCalcInfo.create(
            uid=tools.get_uuid(),
            title='',
            post_id=post_data['infoid'],
            user_id=post_data['userid'],
            time_create=tools.timestamp(),
            time_update=tools.timestamp(),
            extinfo=post_data['extinfo'],

        )

    @staticmethod
    def query_hist_recs(userid, appid):
        return ExtabCalcInfo.select().where(
            (ExtabCalcInfo.user_id == userid) & (ExtabCalcInfo.post_id == appid)
        ).order_by(
            ExtabCalcInfo.time_create
        )


class MAppYun(MPost):
    def __init__(self):
        super(MAppYun, self).__init__()

        try:
            TabApp.create_table()
        except:
            pass

    @staticmethod
    def addata_init(data_dic, ext_dic=None):
        uu = MAppYun.get_by_uid(data_dic['sig'])
        if uu:
            # print('Exists in db.')
            ext_info = uu.extinfo
            if str(ext_info['html_path']).strip() == str(data_dic['html_path']).strip():
                pass
            else:
                ext_info['html_path'] = data_dic['html_path']
                MAppYun.modify_init_meta(data_dic['sig'], ext_info)
            MAppYun.update_misc(data_dic['sig'], kind=data_dic['kind'])
        else:
            time_stamp = int(time.time())
            ext_info = {'html_path': data_dic['html_path']}
            entry = TabApp.create(
                uid=data_dic['sig'],
                title=data_dic['title'],
                time_create=time_stamp,
                time_update=time_stamp,
                cnt_md=data_dic['cnt_md'],
                cnt_html=data_dic['cnt_html'],
                date=datetime.now(),
                view_count=0,
                extinfo=ext_info,
                kind=data_dic['kind']
            )

    @staticmethod
    def modify_init_meta(uid, ext_info):
        entry = TabApp.update(
            extinfo=ext_info,
        ).where(TabApp.uid == uid)
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
        entry = TabApp.update(
            title=data_dic['title'][0],
            keywords=data_dic['keywords'][0],
            desc=data_dic['desc'][0],
            update_time=int(time.time()),
            date=datetime.now(),
            cnt_md=data_dic['cnt_md'][0],
            cnt_html=tools.markdown2html(data_dic['cnt_md'][0])
        ).where(TabApp.uid == uid)
        entry.execute()
        return uid

