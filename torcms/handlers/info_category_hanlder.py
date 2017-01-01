# -*- coding:utf-8 -*-

'''
根据Slug，依照分类的方式列出信息。
'''

from  math import ceil as math_ceil
import tornado.escape
from torcms.model.info_model import MInfor
from torcms.model.category_model import MCategory
import config

from torcms.handlers.category_handler import CategoryHandler
from torcms.model.infor2catalog_model import MInfor2Catalog
from config import router_post
from torcms.core.tools import logger


class InforCategoryHandler(CategoryHandler):
    '''
    List the infos by the slug of the catalog.
    '''

    def initialize(self):
        super(InforCategoryHandler, self).initialize()
        # self.kind = 'm'
        self.mequa = MInfor()
        self.mcat = MCategory()
        self.mapp2tag = MInfor2Catalog()

    def get(self, url_str=''):
        logger.info('tag: {0}'.format(url_str))
        if len(url_str.strip()) == 0:
            return False

        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1:
            self.list(url_str)
        elif len(url_arr) == 2:
            if url_arr[0] == 'j_subcat':
                self.ajax_subcat_arr(url_arr[1])

            else:
                self.list(url_arr[0], url_arr[1])

    def list(self, tag_slug, cur_p=''):
        '''
        根据 cat_handler.py 中的 def view_cat_new(self, cat_slug, cur_p = '')
        :param tag_slug:
        :return:
        '''
        if cur_p == '' or cur_p == '-1':
            current_page_number = 1
        else:
            current_page_number = int(cur_p)
        taginfo = self.mcat.get_by_slug(tag_slug)

        num_of_tag = self.mapp2tag.count_of_certain_category(taginfo.uid)
        page_num = math_ceil(num_of_tag / config.page_num)
        tag_name = taginfo.name

        kwd = {
            'tag_name': tag_name,
            'tag_slug': tag_slug,
            'title': tag_name,
            'current_page': current_page_number,
        }

        self.render('post_{0}/tag_list.html'.format(taginfo.kind),
                    taginfo=taginfo,
                    infos=self.mapp2tag.query_pager_by_slug(tag_slug, current_page_number),
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    pager=self.gen_pager_bootstrap(tag_slug, page_num, current_page_number),
                    userinfo=self.userinfo,
                    router=router_post[taginfo.kind],
                    )

    def gen_pager_bootstrap(self, cat_slug, page_num, current):
        # cat_slug 分类
        # page_num 页面总数
        # current 当前页面
        if page_num == 1:
            return ''

        pager_shouye = '''
        <li class=" {0}">
        <a  href="/tag/{1}">&lt;&lt; 首页</a>
                    </li>'''.format('hidden' if current <= 1 else '', cat_slug)

        pager_pre = '''
                    <li class=" {0}">
                    <a  href="/tag/{1}/{2}">&lt; 前页</a>
                    </li>
                    '''.format('hidden' if current <= 1 else '', cat_slug, current - 1)
        pager_mid = ''
        for ind in range(0, page_num):
            tmp_mid = '''
                    <li class="{0}">
                    <a  href="/tag/{1}/{2}">{2}</a></li>
                    '''.format('active' if ind + 1 == current else '', cat_slug, ind + 1)
            pager_mid += tmp_mid
        pager_next = '''
                    <li class=" {0}">
                    <a  href="/tag/{1}/{2}">后页 &gt;</a>
                    </li>
                    '''.format('hidden' if current >= page_num else '', cat_slug, current + 1)
        pager_last = '''
                    <li class=" {0}">
                    <a  href="/tag/{1}/{2}">末页
                        &gt;&gt;</a>
                    </li>
                    '''.format('hidden' if current >= page_num else '', cat_slug, page_num)
        pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
        return (pager)

    def gen_pager(self, cat_slug, page_num, current):
        # cat_slug 分类
        # page_num 页面总数
        # current 当前页面
        if page_num == 1:
            return ''

        pager_shouye = '''
        <li class="pure-menu-item first {0}">
        <a class="pure-menu-link" href="/tag/{1}">&lt;&lt; 首页</a>
                    </li>'''.format('hidden' if current <= 1 else '', cat_slug)

        pager_pre = '''
                    <li class="pure-menu-item previous {0}">
                    <a class="pure-menu-link" href="/tag/{1}/{2}">&lt; 前页</a>
                    </li>
                    '''.format('hidden' if current <= 1 else '', cat_slug, current - 1)
        pager_mid = ''
        for ind in range(0, page_num):
            tmp_mid = '''
                    <li class="pure-menu-item page {0}">
                    <a class="pure-menu-link" href="/tag/{1}/{2}">{2}</a></li>
                    '''.format('selected' if ind + 1 == current else '', cat_slug, ind + 1)
            pager_mid += tmp_mid
        pager_next = '''
                    <li class="pure-menu-item next {0}">
                    <a class="pure-menu-link" href="/tag/{1}/{2}">后页 &gt;</a>
                    </li>
                    '''.format('hidden' if current >= page_num else '', cat_slug, current + 1)
        pager_last = '''
                    <li class="pure-menu-item last {0}">
                    <a class="pure-menu-link" href="/tag/{1}/{2}">末页
                        &gt;&gt;</a>
                    </li>
                    '''.format('hidden' if current >= page_num else '', cat_slug, page_num)
        pager = pager_shouye + pager_pre + pager_mid + pager_next + pager_last
        return (pager)
