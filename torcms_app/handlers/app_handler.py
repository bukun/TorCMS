# -*- coding:utf-8 -*-

'''
App计算的扩展处理
'''
import os

from torcms.handlers.post_handler import PostHandler
from torcms_app.model.ext_model import MCalcInfo


class YuansuanHandler(PostHandler):
    '''
    App计算的扩展处理
    '''

    def initialize(self, **kwargs):
        super(YuansuanHandler, self).initialize()
        self.mcalcinfo = MCalcInfo()
        if 'kind' in kwargs:
            self.kind = kwargs['kind']
        else:
            self.kind = 's'

    def _redirect(self, url_arr):
        '''
        Redirection.
        :param url_arr:
        :return:
        '''
        direct_dic = {
            'recent': '/post_list/recent',
            'refresh': '/post_list/_refresh',
            '_refresh': '/post_list/_refresh',

        }
        sig = url_arr[0]
        for sig_enum in direct_dic:
            if sig == sig_enum:
                self.redirect(direct_dic[sig])
        pre_dic = {
            'cat_add': '_cat_add',
            'add_document': '_add',
            'add': '_add',
            'modify': '_edit',
            'edit': '_edit',
            'delete': '_delete',
            'ajax_count_plus': 'j_count_plus',
        }
        sig = url_arr[0]
        for sig_enum in pre_dic:
            if sig == sig_enum:
                url_arr = [pre_dic[sig_enum]] + url_arr[1:]
                url_str = '/post/' + '/'.join(url_arr)
                self.redirect(url_str)
        if len(url_arr) == 1 and len(url_arr[0]) == 4:
            self.redirect('/app/s' + url_arr[0])
        return True

    def get(self, *args):

        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if len(url_arr) > 0:
            self._redirect(url_arr)

        if url_str == '':
            self.index()
        elif url_arr[0] == '_cat_add':
            self._to_add(catid=url_arr[1])
        elif url_arr[0] == '_add':
            if len(url_arr) == 2:
                self._to_add(uid=url_arr[1])
            else:
                self._to_add()
        elif url_arr[0] == '_edit_kind':
            self._to_edit_kind(url_arr[1])
        elif url_arr[0] == '_edit':
            self._to_edit(url_arr[1])
        elif url_arr[0] == '_delete':
            self.delete(url_arr[1])
        elif url_arr[0] == 'j_delete':
            self.j_delete(url_arr[1])
        elif url_arr[0] == 'j_count_plus':
            self.j_count_plus(url_arr[1])
        elif len(url_arr) == 1 and url_str.endswith('.html'):
            # Deprecated
            self.redirect('/post/{uid}'.format(uid=url_str.split('.')[0]))
        elif len(url_arr) == 1 and len(url_str) in [4, 5]:
            self._view_or_add(url_str)
        else:
            kwd = {
                'title': '',
                'info': '404. Page not found!',
            }
            self.set_status(404)
            self.render('misc/html/404.html', kwd=kwd,
                        userinfo=self.userinfo)

    def ext_tmpl_view(self, rec):
        html_path = rec.extinfo['html_path']
        if os.path.exists('templates/jshtml/{0}.html'.format(html_path)):
            pass
        else:
            '''
            如果正常找不到，则在模板文件夹下面进行搜索。
            这个比较费时间
            '''
            html_path = ''
            getit = False
            for wroot, wdirs, wfiles in os.walk('./templates/jshtml'):
                for wfile in wfiles:
                    if wfile == '{0}.html'.format(rec.uid):
                        html_path = os.path.join(wroot, wfile[:-5])[len('./templates/jshtml'):]
                        getit = True
                        break
                if getit:
                    break

        if html_path == '':
            return False

        post_data = self.get_request_arguments()
        runid = ''

        if 'runid' in post_data:
            runid = post_data['runid']

        return 'jshtml/{0}.html'.format(html_path)

    def ext_view_kwd(self, info_rec):
        '''
        The additional information.
        :param info_rec:
        :return: directory.
        '''

        app_hist_recs = None
        if self.userinfo:
            app_hist_recs = self.mcalcinfo.query_hist_recs(self.userinfo.uid, info_rec.uid)

        kwd = {}
        post_data = self.get_request_arguments()
        # runid: 保存过的运行的数据
        runid = ''
        if 'runid' in post_data:
            runid = post_data['runid']
        kwd['runid'] = runid
        kwd['app_hist_recs'] = app_hist_recs
        return kwd
