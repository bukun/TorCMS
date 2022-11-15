# -*- coding:utf-8 -*-
'''
Log handler.
'''

from concurrent.futures import ThreadPoolExecutor

from config import CMS_CFG
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.model.log_model import MLog


class LogHandler(BaseHandler):
    '''
    Log handler.
    '''
    executor = ThreadPoolExecutor(2)

    def initialize(self, **kwargs):
        super().initialize()

    def get(self, *args, **kwargs):

        url_str = args[0]

        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1:
            if url_arr[0] in ['pageview', 'search']:
                # 访问量
                self.search()

        # elif len(url_arr) == 2:
        #     if url_arr[0] == 'pageview':
        #         self.pageview(url_arr[1])
            # else:
            #     self.user_log_list(url_arr[0], url_arr[1])
        else:
            self.render('misc/html/404.html', userinfo=self.userinfo, kwd={})

    def post(self, *args, **kwargs):

        url_str = args[0]

        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['_add']:
            if len(url_arr) == 2:
                self.add(uid=url_arr[1])
            else:
                self.add()
        elif url_arr[0] == 'search':
            self.search()

        else:
            self.show404()

    def add(self, **kwargs):
        '''
        in infor.
        '''

        post_data = {}

        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)[0]

        MLog.add(post_data)
        kwargs.pop('uid', None)  # delete `uid` if exists in kwargs

        self.redirect('/log/')

    def list(self, cur_p=''):
        '''
        View the list of the Log.
        '''

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

        pager_num = int(MLog.total_number() / CMS_CFG['list_num'])
        kwd = {
            'pager': '',
            'title': '',
            'current_page': current_page_number,
        }

        if self.is_p:
            self.render('admin/log_ajax/user_list.html',
                        kwd=kwd,
                        user_list=MLog.query_all_user(),
                        no_user_list=MLog.query_all(
                            current_page_num=current_page_number),
                        format_date=tools.format_date,
                        userinfo=self.userinfo)
        else:
            self.render('misc/log/user_list.html',
                        kwd=kwd,
                        user_list=MLog.query_all_user(),
                        no_user_list=MLog.query_all(
                            current_page_num=current_page_number),
                        format_date=tools.format_date,
                        userinfo=self.userinfo)

    def user_log_list(self, userid, cur_p=''):
        '''
        View the list of the Log.
        '''

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

        pager_num = int(MLog.total_number() / CMS_CFG['list_num'])
        kwd = {
            'pager': '',
            'title': '',
            'current_page': current_page_number,
            'user_id': userid,
        }

        if self.is_p:
            self.render('admin/log_ajax/user_log_list.html',
                        kwd=kwd,
                        infos=MLog.query_pager_by_user(
                            userid, current_page_num=current_page_number),
                        format_date=tools.format_date,
                        userinfo=self.userinfo)
        else:
            self.render('misc/log/user_log_list.html',
                        kwd=kwd,
                        infos=MLog.query_pager_by_user(
                            userid, current_page_num=current_page_number),
                        format_date=tools.format_date,
                        userinfo=self.userinfo)

    def pageview(self, cur_p=''):
        '''
        View the list of the Log.
        '''

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

        pager_num = int(MLog.total_number() / CMS_CFG['list_num'])

        kwd = {
            'pager': '',
            'title': '',
            'current_page': current_page_number,
        }
        arr_num = []
        postinfo = MLog.query_all_current_url()

        for i in postinfo:
            postnum = MLog.count_of_current_url(i.current_url)
            arr_num.append(postnum)

        self.render('misc/log/pageview.html',
                    kwd=kwd,
                    # infos=MLog.query_all_pageview(
                    #     current_page_num=current_page_number),
                    postinfo=postinfo,
                    arr_num=arr_num,
                    format_date=tools.format_date,
                    userinfo=self.userinfo)

    def search(self, **kwargs):
        post_data = self.get_request_arguments()
        url = post_data.get('url')
        res = MLog.get_by_url(url)
        self.render('misc/log/pageview_search.html',
                    res=res,
                    format_date=tools.format_date,
                    userinfo=self.userinfo)


class LogPartialHandler(LogHandler):
    '''
    Partially render for user handler.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.is_p = True
