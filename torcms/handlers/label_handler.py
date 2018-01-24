# -*- coding:utf-8 -*-

'''
For Post Label.
'''

import json
import tornado.escape
import tornado.web
from torcms.core.base_handler import BaseHandler
from torcms.model.label_model import MPost2Label
from torcms.core.torcms_redis import redisvr
from config import CMS_CFG


class LabelHandler(BaseHandler):
    '''
    For Post Label. with 'kind'.
    '''

    def initialize(self, **kwargs):
        super(LabelHandler, self).initialize()

    def get(self, *args, **kwargs):
        '''
        /label/s/view
        '''
        url_arr = self.parse_url(args[0])

        if len(url_arr) == 2:
            if url_arr[0] == 'remove':
                self.remove_redis_keyword(url_arr[1])
            else:
                self.list(url_arr[0], url_arr[1])
        elif len(url_arr) == 3:
            self.list(url_arr[0], url_arr[1], url_arr[2])
        else:
            return False

    @tornado.web.authenticated
    def remove_redis_keyword(self, keyword):
        '''
        Remove the keyword for redis.
        '''
        redisvr.srem(CMS_CFG['redis_kw'] + self.userinfo.user_name, keyword)
        return json.dump({}, self)

    def list(self, kind, tag_slug, cur_p=''):
        '''
        根据 cat_handler.py 中的 def view_cat_new(self, cat_slug, cur_p = '')
        '''
        # 下面用来使用关键字过滤信息，如果网站信息量不是很大不要开启
        # Todo:
        # if self.get_current_user():
        #     redisvr.sadd(config.redis_kw + self.userinfo.user_name, tag_slug)

        if cur_p == '':
            current_page_number = 1
        else:
            current_page_number = int(cur_p)

        current_page_number = 1 if current_page_number < 1 else current_page_number

        pager_num = int(MPost2Label.total_number(tag_slug, kind) / CMS_CFG['list_num'])
        tag_name = ''
        kwd = {'tag_name': tag_name,
               'tag_slug': tag_slug,
               'title': tag_name,
               'current_page': current_page_number}

        self.render('list/label_{kind}.html'.format(kind=kind),
                    infos=MPost2Label.query_pager_by_slug(
                        tag_slug,
                        kind=kind,
                        current_page_num=current_page_number
                    ),
                    kwd=kwd,
                    userinfo=self.userinfo,
                    pager=self.gen_pager(kind, tag_slug, pager_num, current_page_number),
                    cfg=CMS_CFG)

    def gen_pager(self, kind, cat_slug, page_num, current):
        '''
        cat_slug 分类
        page_num 页面总数
        current 当前页面
        '''
        if page_num == 1:
            return ''

        pager_shouye = '''<li class="{0}">   <a href="/label/{1}/{2}">&lt;&lt; 首页</a>
        </li>'''.format(
            'hidden' if current <= 1 else '', kind, cat_slug
        )

        pager_pre = '''<li class="{0}"><a href="/label/{1}/{2}/{3}">&lt; 前页</a>
        </li>'''.format(
            'hidden' if current <= 1 else '', kind, cat_slug, current - 1
        )
        pager_mid = ''
        for ind in range(0, page_num):
            tmp_mid = '''<li class="{0}"><a  href="/label/{1}/{2}/{3}">{3}</a>
            </li>'''.format(
                'active' if ind + 1 == current else '', kind, cat_slug, ind + 1
            )
            pager_mid += tmp_mid
        pager_next = '''<li class=" {0}"><a  href="/label/{1}/{2}/{3}">后页 &gt;</a>
        </li>'''.format(
            'hidden' if current >= page_num else '', kind, cat_slug, current + 1
        )
        pager_last = '''<li class=" {0}"><a href="/label/{1}/{2}/{3}">末页&gt;&gt;</a>
        </li>'''.format(
            'hidden' if current >= page_num else '', kind, cat_slug, page_num
        )
        pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
        return pager


class InfoTagHandler(BaseHandler):
    '''
    Access label without 'kind'. redirect to /label/
    '''

    def initialize(self, **kwargs):
        super(InfoTagHandler, self).initialize()
        if 'kind' in kwargs:
            self.kind = kwargs['kind']
        else:
            self.kind = '9'

    def get(self, *args, **kwargs):
        url_arr = self.parse_url(args[0])

        if len(url_arr) == 1:

            self.redirect('/label/{kind}/{slug}'.format(
                slug=url_arr[0], kind=self.kind
            ))

        elif len(url_arr) == 2:

            self.redirect('/label/{kind}/{slug}/{page}'.format(
                slug=url_arr[0], kind=self.kind, page=url_arr[1]
            ))
