# -*- coding:utf-8 -*-
'''
For Post Label.
'''

import json
import os
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.core.torcms_redis import redisvr
from torcms.model.label_model import MLabel, MPost2Label
from config import CMS_CFG, router_post


class LabelHandler(BaseHandler):
    '''
    For Post Label. with 'kind'.
    '''

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):
        '''
        /label/s/view
        '''
        url_arr = self.parse_url(args[0])

        if len(url_arr) == 2:
            if url_arr[0] == 'remove':
                # ToDo: 此情况应该未使用，可以删除.
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
        # if self.get_current_user():
        #     redisvr.sadd(config.redis_kw + self.userinfo.user_name, tag_slug)

        # ToDo: 可能会有类似于 `('s')`  这样的请求。 发起的地方未找到。暂按如下处理。
        if len(kind) == 1:
            pass
        else:
            print('Invalid requst: ', kind)
            self.set_status(406)
            return

        current_page_number = 1
        if cur_p == '':
            current_page_number = 1
        else:
            try:
                current_page_number = int(cur_p)
            except TypeError:
                current_page_number = 1
            except Exception as err:
                print(err.args)
                print(str(err))
                print(repr(err))

        current_page_number = 1 if current_page_number < 1 else current_page_number

        pager_num = int(
            MPost2Label.total_number(tag_slug, kind) / CMS_CFG['list_num'])
        tag_info = MLabel.get_by_slug(tag_slug)
        if tag_info:
            tag_name = tag_info.name
        else:
            tag_name = 'Label search results'
        kwd = {
            'tag_name': tag_name,
            'tag_slug': tag_slug,
            'title': tag_name,
            'current_page': current_page_number,
            'router': router_post[kind],
            'kind': kind
        }

        the_list_file = './templates/list/label_{kind}.html'.format(kind=kind)

        if os.path.exists(the_list_file):
            tmpl = 'list/label_{kind}.html'.format(kind=kind)

        else:
            tmpl = 'list/label.html'

        self.render(tmpl,
                    infos=MPost2Label.query_pager_by_slug(
                        tag_slug,
                        kind=kind,
                        current_page_num=current_page_number),
                    kwd=kwd,
                    userinfo=self.userinfo,
                    pager=self.gen_pager(kind, tag_slug, pager_num,
                                         current_page_number),
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
        </li>'''.format('hidden' if current <= 1 else '', kind, cat_slug)

        pager_pre = '''<li class="{0}"><a href="/label/{1}/{2}/{3}">&lt; 前页</a>
        </li>'''.format('hidden' if current <= 1 else '', kind, cat_slug,
                        current - 1)
        pager_mid = ''
        for ind in range(0, page_num):
            tmp_mid = '''<li class="{0}"><a  href="/label/{1}/{2}/{3}">{3}</a>
            </li>'''.format('active' if ind + 1 == current else '', kind,
                            cat_slug, ind + 1)
            pager_mid += tmp_mid
        pager_next = '''<li class=" {0}"><a  href="/label/{1}/{2}/{3}">后页 &gt;</a>
        </li>'''.format('hidden' if current >= page_num else '', kind,
                        cat_slug, current + 1)
        pager_last = '''<li class=" {0}"><a href="/label/{1}/{2}/{3}">末页&gt;&gt;</a>
        </li>'''.format('hidden' if current >= page_num else '', kind,
                        cat_slug, page_num)
        pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
        return pager


class InfoTagHandler(BaseHandler):
    '''
    Access label without 'kind'. redirect to /label/
    '''

    def __init__(self):
        super().__init__()
        self.kind = '9'

    def initialize(self, **kwargs):
        super().initialize()
        if 'kind' in kwargs:
            self.kind = kwargs['kind']
        else:
            self.kind = '9'

    def get(self, *args, **kwargs):
        url_arr = self.parse_url(args[0])

        if len(url_arr) == 1:

            self.redirect('/label/{kind}/{slug}'.format(slug=url_arr[0],
                                                        kind=self.kind))

        elif len(url_arr) == 2:

            self.redirect('/label/{kind}/{slug}/{page}'.format(
                slug=url_arr[0], kind=self.kind, page=url_arr[1]))
