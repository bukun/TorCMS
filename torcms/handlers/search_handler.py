# -*- coding:utf-8 -*-

'''
For full text searching.
'''

from config import CMS_CFG
from torcms.core.base_handler import BaseHandler
from torcms.core.tool.whoosh_tool import YunSearch
from torcms.model.category_model import MCategory
from torcms.core.tools import logger


def gen_pager_bootstrap_url(cat_slug, page_num, current):
    '''
    pager for searching results.
    '''
    pager = ''
    if page_num == 1 or page_num == 0:
        pager = ''
    elif page_num > 1:
        pager_mid, pager_pre, pager_next, pager_last, pager_home = '', '', '', '', ''

        pager = '<ul class="pagination">'

        if current > 1:
            pager_home = '''

                  <li class="{0}" name='fenye' onclick='change(this);'
                  ><a href="{1}/{2}">首页</a></li>'''.format('', cat_slug, 1)

            pager_pre = ''' <li class="{0}" name='fenye' onclick='change(this);'>
                <a href="{1}/{2}">上一页</a></li>'''.format('', cat_slug, current - 1)
        if current > 5:
            cur_num = current - 4
        else:
            cur_num = 1

        if page_num > 10 and cur_num < page_num - 10:
            show_num = cur_num + 10

        else:
            show_num = page_num + 1

        for num in range(cur_num, show_num):
            if num == current:
                checkstr = 'active'
            else:
                checkstr = ''

            tmp_str_df = '''<li class="{0}" name='fenye' onclick='change(this);'>
                  <a href="{1}/{2}">{2}</a></li>'''.format(checkstr, cat_slug, num)

            pager_mid += tmp_str_df
        if current < page_num:
            pager_next = '''

                  <li class="{0}" name='fenye' onclick='change(this);'
                  ><a href="{1}/{2}">下一页</a></li>'''.format('', cat_slug, current + 1)
            pager_last = '''

                  <li class="{0}" name='fenye' onclick='change(this);'
                 ><a href="{1}/{2}">末页</a></li>'''.format('', cat_slug, page_num)

        pager += pager_home + pager_pre + pager_mid + pager_next + pager_last
        pager += '</ul>'
    else:
        pass

    return pager


class SearchHandler(BaseHandler):
    '''
    For full text searching.
    '''

    def initialize(self, **kwargs):
        super(SearchHandler, self).initialize()
        self.ysearch = YunSearch()

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str == '':
            self.index()
        elif len(url_arr) == 2:
            self.search(url_arr[0], url_arr[1])
        elif len(url_arr) == 3:
            self.search_cat(url_arr[0], url_arr[1], int(url_arr[2]))
        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('misc/html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo)

    def index(self):
        tag_enum = MCategory.query_pcat()
        self.render('misc/search/search_index.html', userinfo=self.userinfo,
                    cat_enum=tag_enum,
                    tag_enum=tag_enum)

    def post(self, *args, **kwargs):
        post_data = self.get_post_data()

        catid = post_data['searchcat'] if 'searchcat' in post_data else ''

        keyword = post_data['keyword']

        logger.info('Searching ... ')
        logger.info('    catid:    {uid}'.format(uid=catid))
        logger.info('    keyowrds: {kw}'.format(kw=keyword))

        if catid == '':
            self.redirect('/search/{0}/1'.format(keyword))
        else:
            self.redirect('/search/{0}/{1}/1'.format(catid, keyword))

    def search(self, keyword, p_index=''):
        '''
        perform searching.
        '''
        if p_index == '' or p_index == '-1':
            current_page_number = 1
        else:
            current_page_number = int(p_index)
        res_all = self.ysearch.get_all_num(keyword)
        results = self.ysearch.search_pager(
            keyword,
            page_index=current_page_number,
            doc_per_page=CMS_CFG['list_num']
        )
        page_num = int(res_all / CMS_CFG['list_num'])
        kwd = {'title': '查找结果',
               'pager': '',
               'count': res_all,
               'keyword': keyword,
               'catid': '',
               'current_page': current_page_number}
        self.render('misc/search/search_list.html',
                    kwd=kwd,
                    srecs=results,
                    pager=gen_pager_bootstrap_url('/search/{0}'.format(keyword),
                                                  page_num,
                                                  current_page_number),
                    userinfo=self.userinfo,
                    cfg=CMS_CFG)

    def search_cat(self, catid, keyword, p_index=1):
        '''
        Searching according the kind.
        '''
        catid = 'sid' + catid
        logger.info('-' * 20)
        logger.info('search cat')
        logger.info('catid: {0}'.format(catid))
        logger.info('keyword: {0}'.format(keyword))

        # catid = ''
        if p_index == '' or p_index == '-1':
            current_page_number = 1
        else:
            current_page_number = int(p_index)
        res_all = self.ysearch.get_all_num(keyword, catid=catid)

        results = self.ysearch.search_pager(
            keyword,
            catid=catid,
            page_index=current_page_number,
            doc_per_page=CMS_CFG['list_num']
        )
        page_num = int(res_all / CMS_CFG['list_num'])

        kwd = {'title': '查找结果',
               'pager': '',
               'count': res_all,
               'current_page': current_page_number,
               'catid': catid,
               'keyword': keyword}

        self.render('misc/search/search_list.html',
                    kwd=kwd,
                    srecs=results,
                    pager=gen_pager_bootstrap_url(
                        '/search/{0}/{1}'.format(catid, keyword),
                        page_num,
                        current_page_number
                    ),
                    userinfo=self.userinfo,
                    cfg=CMS_CFG)
