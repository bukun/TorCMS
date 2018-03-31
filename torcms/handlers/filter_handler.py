# -*- coding:utf-8 -*-
'''
关键词过滤，涉及到不同分类，使用  session 来处理。
分类下面的过滤，则使用GET的url的参数。
'''

import math
from html2text import html2text
import tornado.escape
from torcms.model.post_model import MPost
from torcms.core.base_handler import BaseHandler
from torcms.model.category_model import MCategory
from torcms.core.torcms_redis import redisvr
from torcms.core.tools import logger
from config import CMS_CFG

def echo_html_fenye_str(rec_num, fenye_num):
    '''
    生成分页的导航
    '''

    pagination_num = int(math.ceil(rec_num * 1.0 / 10))

    if pagination_num == 1 or pagination_num == 0:
        fenye_str = ''

    elif pagination_num > 1:
        pager_mid, pager_pre, pager_next, pager_last, pager_home = '', '', '', '', ''

        fenye_str = '<ul class="pagination">'

        if fenye_num > 1:
            pager_home = '''<li class="{0}" name='fenye' onclick='change(this);'
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

            tmp_str_df = '''<li class="{0}" name='fenye' onclick='change(this);'
              value='{1}'><a>{1}</a></li>'''.format(checkstr, num)

            pager_mid += tmp_str_df
        if fenye_num < pagination_num:
            pager_next = '''<li class="{0}" name='fenye' onclick='change(this);'
              value='{1}'><a>Next Page</a></li>'''.format('', fenye_num + 1)
            pager_last = '''<li class="{0}" name='fenye' onclick='change(this);'
              value='{1}'><a>End Page</a></li>'''.format('', pagination_num)

        fenye_str += pager_home + pager_pre + pager_mid + pager_next + pager_last
        fenye_str += '</ul>'

    else:
        return ''
    return fenye_str


class FilterHandler(BaseHandler):
    '''
    List view,by category uid. The list could be filtered.
    '''

    def initialize(self, **kwargs):
        super(FilterHandler, self).initialize()

    def get(self, *args, **kwargs):
        url_str = args[0]

        logger.info('infocat get url_str: {0}'.format(url_str))
        if len(url_str) == 4:
            self.list(url_str)
        elif len(url_str) > 4:
            self.echo_html(url_str)
        else:
            self.render('misc/html/404.html', kwd={})

    def gen_redis_kw(self):
        condition = {}
        if self.get_current_user() and self.userinfo:
            redis_kw = redisvr.smembers(CMS_CFG['redis_kw'] + self.userinfo.user_name)
        else:
            redis_kw = []

        kw_condition_arr = []
        for the_key in redis_kw:
            kw_condition_arr.append(the_key.decode('utf-8'))
        if redis_kw:
            condition['def_tag_arr'] = kw_condition_arr
        return condition

    def echo_html(self, url_str):
        '''
        Show the HTML
        '''

        logger.info('info echo html: {0}'.format(url_str))

        condition = self.gen_redis_kw()

        url_arr = self.parse_url(url_str)
        sig = url_arr[0]

        num = (len(url_arr) - 2) // 2

        catinfo = MCategory.get_by_uid(sig)

        if catinfo.pid == '0000':
            condition['def_cat_pid'] = sig
        else:
            condition['def_cat_uid'] = sig

        fenye_num = 1
        for idx in range(num):
            ckey = url_arr[idx * 2 + 2]
            tval = url_arr[idx * 2 + 3]

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
            infos = MPost.query_list_pager(condition, fenye_num, kind=catinfo.kind)
            self.echo_html_list_str(sig, infos)
        elif url_arr[1] == 'num':
            allinfos = MPost.query_under_condition(condition, kind=catinfo.kind)
            self.write(
                tornado.escape.xhtml_unescape(
                    echo_html_fenye_str(
                        allinfos.count(),
                        fenye_num
                    )
                )
            )

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
                    post_infos=infos,
                    widget_info=kwd)

    def list(self, catid):
        '''
        页面打开后的渲染方法，不包含 list 的查询结果与分页导航
        '''
        logger.info('Infocat input: {0}'.format(catid))
        condition = self.gen_redis_kw()
        sig = catid
        bread_title = ''
        bread_crumb_nav_str = '<li>当前位置：<a href="/">信息</a></li>'

        _catinfo = MCategory.get_by_uid(catid)
        logger.info('Infocat input: {0}'.format(_catinfo))
        if _catinfo.pid == '0000':
            pcatinfo = _catinfo
            catinfo = None
            parent_id = catid
            parent_catname = MCategory.get_by_uid(parent_id).name
            condition['parentid'] = [parent_id]
            catname = MCategory.get_by_uid(sig).name
            bread_crumb_nav_str += '<li><a href="/list/{0}">{1}</a></li>'.format(sig, catname)
            bread_title = '{0}'.format(catname)

        else:
            catinfo = _catinfo
            pcatinfo = MCategory.get_by_uid(_catinfo.pid)
            condition['catid'] = [sig]
            parent_id = _catinfo.uid
            parent_catname = MCategory.get_by_uid(parent_id).name
            catname = MCategory.get_by_uid(sig).name
            bread_crumb_nav_str += '<li><a href="/list/{0}">{1}</a></li>'.format(
                parent_id,
                parent_catname
            )

            bread_crumb_nav_str += '<li><a href="/list/{0}">{1}</a></li>'.format(sig, catname)
            bread_title += '{0} - '.format(parent_catname)
            bread_title += '{0}'.format(catname)

        num = MPost.get_num_condition(condition)

        kwd = {'catid': catid,
               'daohangstr': bread_crumb_nav_str,
               'breadtilte': bread_title,
               'parentid': parent_id,
               'parentlist': MCategory.get_parent_list(),
               'condition': condition,
               'catname': catname,
               'rec_num': num}

        # cat_rec = MCategory.get_by_uid(catid)
        if self.get_current_user() and self.userinfo:
            redis_kw = redisvr.smembers(CMS_CFG['redis_kw'] + self.userinfo.user_name)
        else:
            redis_kw = []
        kw_condition_arr = []
        for the_key in redis_kw:
            kw_condition_arr.append(the_key.decode('utf-8'))
        self.render('autogen/list/list_{0}.html'.format(catid),
                    userinfo=self.userinfo,
                    kwd=kwd,
                    widget_info=kwd,
                    condition_arr=kw_condition_arr,
                    cat_enum=MCategory.get_qian2(parent_id[:2]),
                    pcatinfo=pcatinfo,
                    catinfo=catinfo)


class ListHandler(BaseHandler):
    '''
    List view,by category uid. The list could be filtered.
    '''

    def initialize(self):
        super(ListHandler, self).initialize()

    def get(self, *args):
        url_str = args[0]
        self.redirect('/filter/{0}'.format(url_str))
