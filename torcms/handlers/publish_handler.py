# -*- coding:utf-8 -*-

'''
The web page for publish, with category.
'''

import tornado
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.model.category_model import MCategory

from config import router_post


class PublishHandler(BaseHandler):
    '''
    Try to add new post, with category information.
    '''

    def initialize(self, **kwargs):
        super(PublishHandler, self).initialize()

    def get(self, *args):
        url_str = args[0]
        # url_arr = self.parse_url(url_str)

        dict_get = {
            1: self.view_class1,
            4: self.view_class2,
            5: self.echo_class2,
        }

        dict_get.get(len(url_str), lambda x: self.redirect('/'))(url_str)

        # if len(url_str) == 1:
        #     # like:  /publish/s or  /publish/m
        #     self.view_class1(url_str)
        # elif len(url_str) == 4:
        #     # like:  /publish/s or  /publish/m
        #     self.view_class2(url_str)
        # elif len(url_str) == 5:
        #     self.echo_class2(url_str)

    # Todo: unused ?
    @tornado.web.authenticated
    def echo_class2(self, catstr=''):
        '''
        弹出的二级发布菜单
        '''
        fatherid = catstr[1:]
        self.write(self.format_class2(fatherid))

    @tornado.web.authenticated
    def format_class2(self, fatherid):
        catinfo = MCategory.get_by_uid(fatherid)
        dbdata = MCategory.query_sub_cat(fatherid)
        outstr = '<ul class="list-group">'
        for rec in dbdata:
            outstr += '''
            <a href="/{0}/_cat_add/{1}" class="btn btn-primary"
            style="display: inline-block;margin:3px;" >{2}</a>
            '''.format(router_post[catinfo.kind], rec.uid, rec.name)
        outstr += '</ul>'
        return outstr

    @tornado.web.authenticated
    def view_class1(self, kind_sig):
        '''
        Publishing from 1st range category.
        '''
        dbdata = MCategory.get_parent_list(kind=kind_sig)
        class1str = ''
        for rec in dbdata:
            class1str += '''
             <a onclick="select_sub_tag('/publish/2{0}');" class="btn btn-primary"
             style="display: inline-block;margin:3px;" >
             {1}</a>'''.format(rec.uid, rec.name)

        kwd = {'class1str': class1str,
               'parentid': '0',
               'parentlist': MCategory.get_parent_list()}
        self.render('misc/publish/publish.html',
                    userinfo=self.userinfo,
                    kwd=kwd)

    @tornado.web.authenticated
    def view_class2(self, fatherid=''):
        '''
        Publishing from 2ed range category.
        '''

        if self.is_admin():
            pass
        else:
            return False

        kwd = {'class1str': self.format_class2(fatherid),
               'parentid': '0',
               'parentlist': MCategory.get_parent_list()}

        if fatherid.endswith('00'):
            self.render('misc/publish/publish2.html',
                        userinfo=self.userinfo,
                        kwd=kwd)
        else:
            catinfo = MCategory.get_by_uid(fatherid)
            self.redirect('/{1}/_cat_add/{0}'.format(fatherid, router_post[catinfo.kind]))
