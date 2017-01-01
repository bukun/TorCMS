# -*- coding:utf-8 -*-
import math

import config
import tornado.escape

from torcms.model.info_model import MInfor as  MInfor
from torcms.core.base_handler import BaseHandler
from torcms.model.category_model import MCategory

from torcms.core.torcms_redis import redisvr

from html2text import html2text

from torcms.core.tools import logger

'''
关键词过滤，涉及到不同分类，使用  session 来处理。
分类下面的过滤，则使用GET的url的参数。
'''


class InfoListHandler(BaseHandler):
    def initialize(self, hinfo=''):
        super(InfoListHandler, self).initialize()
        self.minfo = MInfor()
        self.mcat = MCategory()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        logger.info('infocat get url_str: {0}'.format(url_str))
        if len(url_str) == 4:
            self.list(url_str)
        elif len(url_str) > 4:
            self.echo_html(url_str)
        else:
            self.render('html/404.html', kwd={})

    def gen_redis_kw(self):
        condition = {}
        if self.get_current_user():
            redis_kw = redisvr.smembers(config.redis_kw + self.userinfo.user_name)
        else:
            redis_kw = []

        kw_condition_arr = []
        for x in redis_kw:
            kw_condition_arr.append(x.decode('utf-8'))
        if redis_kw:
            condition['def_tag_arr'] = kw_condition_arr
        return condition

    def echo_html(self, url_str):
        logger.info('info echo html: {0}'.format(url_str))

        condition = self.gen_redis_kw()

        url_arr = self.parse_url(url_str)
        sig = url_arr[0]

        num = (len(url_arr) - 2) // 2

        catinfo = self.mcat.get_by_uid(sig)

        if catinfo.pid == '0000':
            condition['def_cat_pid'] = sig
        else:
            condition['def_cat_uid'] = sig

        fenye_num = 1
        for ii in range(num):
            ckey = url_arr[ii * 2 + 2]
            tval = url_arr[ii * 2 + 3]

            if tval == '0':
                continue
            if ckey == 'fenye':
                # 分页参数。单独处理。
                fenye_num = int(tval)
                continue
            else:
                cval = tval
            ckey = 'tag_' + ckey
            condition[ckey] = cval

        if url_arr[1] == 'con':
            infos = self.minfo.get_list_fenye(condition, fenye_num, kind=catinfo.kind)
            self.echo_html_list_str(sig, infos)
        elif url_arr[1] == 'num':
            allinfos = self.minfo.get_list(condition, kind=catinfo.kind)
            self.echo_html_fenye_str(allinfos.count(), fenye_num)

    def echo_html_list_str(self, catid, infos):
        '''
        生成 list 后的 HTML 格式的字符串
        '''
        zhiding_str = ''
        tuiguang_str = ''
        imgname = 'fixed/zhanwei.png'

        kwd = {
            'imgname': imgname,
            'zhiding': zhiding_str,
            'tuiguang': tuiguang_str,
        }

        self.render('autogen/infolist/infolist_{0}.html'.format(catid),
                    userinfo=self.userinfo,
                    kwd=kwd,
                    html2text=html2text,
                    unescape=tornado.escape.xhtml_unescape,
                    post_infos=infos,
                    widget_info=kwd)

    def echo_html_fenye_str(self, rec_num, fenye_num):
        '''
        生成分页的导航
        '''

        pagination_num = int(math.ceil(rec_num * 1.0 / 10))

        if pagination_num == 1 or pagination_num == 0:
            fenye_str = ''

        elif pagination_num > 1:
            pager_mid = ''
            pager_pre = ''
            pager_next = ''
            pager_last = ''
            pager_home = ''
            fenye_str = '<ul class="pagination">'

            if fenye_num > 1:
                pager_home = '''

                  <li class="{0}" name='fenye' onclick='change(this);'
                  value='{1}'><a>First Page</a></li>'''.format('', 1)

                pager_pre = ''' <li class="{0}" name='fenye' onclick='change(this);'
                  value='{1}'><a>Previous Page</a></li>'''.format('', fenye_num - 1)
            if fenye_num > 5:
                cur_num = fenye_num - 4
            else:
                cur_num = 1

            if pagination_num > 10 and cur_num < pagination_num - 10:
                show_num = cur_num + 10

            else:
                show_num = pagination_num + 1

            for num in range(cur_num, show_num):
                if num == fenye_num:
                    checkstr = 'active'
                else:
                    checkstr = ''

                tmp_str_df = '''

                  <li class="{0}" name='fenye' onclick='change(this);'
                  value='{1}'><a>{1}</a></li>'''.format(checkstr, num)

                pager_mid += tmp_str_df
            if fenye_num < pagination_num:
                pager_next = '''

                  <li class="{0}" name='fenye' onclick='change(this);'
                  value='{1}'><a>Next Page</a></li>'''.format('', fenye_num + 1)
                pager_last = '''

                  <li class="{0}" name='fenye' onclick='change(this);'
                  value='{1}'><a>End Page</a></li>'''.format('', pagination_num)

            fenye_str += pager_home + pager_pre + pager_mid + pager_next + pager_last
            fenye_str += '</ul>'

        else:
            return False
        self.write(fenye_str)

    def list(self, catid):
        '''
        页面打开后的渲染方法，不包含 list 的查询结果与分页导航
        '''
        logger.info('Infocat input: {0}'.format(catid))
        condition = self.gen_redis_kw()
        sig = catid
        bread_title = ''
        bread_crumb_nav_str = '<li>当前位置：<a href="/">信息</a></li>'

        _catinfo = self.mcat.get_by_uid(catid)
        if _catinfo.pid == '0000':
            pcatinfo = _catinfo
            catinfo = None
            parent_id = catid
            parent_catname = self.mcat.get_by_id(parent_id).name
            condition['parentid'] = [parent_id]
            catname = self.mcat.get_by_id(sig).name
            bread_crumb_nav_str += '<li><a href="/list/{0}">{1}</a></li>'.format(sig, catname)
            bread_title = '{1}'.format(sig, catname)

        else:
            catinfo = _catinfo
            pcatinfo = self.mcat.get_by_uid(_catinfo.pid)
            condition['catid'] = [sig]
            parent_id = _catinfo.uid
            parent_catname = self.mcat.get_by_id(parent_id).name
            catname = self.mcat.get_by_id(sig).name
            bread_crumb_nav_str += '<li><a href="/list/{0}">{1}</a></li>'.format(parent_id, parent_catname)

            bread_crumb_nav_str += '<li><a href="/list/{0}">{1}</a></li>'.format(sig, catname)
            bread_title += '{1} - '.format(parent_id, parent_catname)
            bread_title += '{1}'.format(sig, catname)

        num = self.minfo.get_num_condition(condition)

        kwd = {
            'catid': catid,
            'daohangstr': bread_crumb_nav_str,
            'breadtilte': bread_title,
            'parentid': parent_id,
            'parentlist': self.mcat.get_parent_list(),
            'condition': condition,
            'catname': catname,
            'rec_num': num,
        }

        # cat_rec = self.mcat.get_by_uid(catid)
        if self.get_current_user():
            redis_kw = redisvr.smembers(config.redis_kw + self.userinfo.user_name)
        else:
            redis_kw = []
        kw_condition_arr = []
        for x in redis_kw:
            kw_condition_arr.append(x.decode('utf-8'))
        self.render('autogen/list/list_{0}.html'.format(catid),
                    userinfo=self.userinfo,
                    kwd=kwd,
                    widget_info=kwd,
                    condition_arr=kw_condition_arr,
                    cat_enum=self.mcat.get_qian2(parent_id[:2]),
                    pcatinfo=pcatinfo,
                    catinfo=catinfo,

                    )
