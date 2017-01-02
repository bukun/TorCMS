# -*- coding:utf-8 -*-

import tornado
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.model.category_model import MCategory

from config import router_post


class InfoPublishHandler(BaseHandler):
    def initialize(self, **kwargs):
        super(InfoPublishHandler, self).initialize()
        self.minforcatalog = MCategory()

    def get(self, *args):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if len(url_str) == 1:
            self.view_class1(url_str)
        elif len(url_str) == 4:
            self.view_class2(url_str)
        elif len(url_str) == 5:
            self.echo_class2(url_str)
        elif len(url_arr) == 2 and url_arr[1] == 'vip':
            self.view_class2(url_arr[0], 1)

    @tornado.web.authenticated
    def echo_class2(self, input=''):
        '''
        弹出的二级发布菜单
        '''
        fatherid = input[1:]
        self.write(self.format_class2(fatherid))

    @tornado.web.authenticated
    def format_class2(self, fatherid):
        # dbdata = self.minforcatalog.get_qian2(fatherid[:2])
        catinfo = self.minforcatalog.get_by_uid(fatherid)
        dbdata = self.minforcatalog.query_sub_cat(fatherid)
        outstr = '<ul class="list-group">'
        for rec in dbdata:
            outstr += '''
            <a href="/{0}/_cat_add/{1}" class="btn btn-primary" style="display: inline-block;margin:3px;" >{2}</a>
            '''.format(router_post[catinfo.kind], rec.uid, rec.name)
        outstr += '</ul>'
        return (outstr)

    @tornado.web.authenticated
    def view_class1(self, kind_sig):
        dbdata = self.minforcatalog.get_parent_list(kind=kind_sig)
        class1str = ''
        for rec in dbdata:
            class1str += '''
             <a onclick="select_sub_tag('/publish/2{0}');" class="btn btn-primary" style="display: inline-block;margin:3px;" >{1}</a>
            '''.format(rec.uid, rec.name)

        kwd = {
            'class1str': class1str,
            'parentid': '0',
            'parentlist': self.minforcatalog.get_parent_list(),
        }
        self.render('infor/publish/publish.html',
                    userinfo=self.userinfo,
                    kwd=kwd)

    @tornado.web.authenticated
    def view_class2(self, fatherid=''):
        '''
        从第二级分类发布
        :param fatherid:
        :return:
        '''
        if self.is_admin():
            pass
        else:
            return False

        kwd = {
            'class1str': self.format_class2(fatherid),
            'parentid': '0',
            'parentlist': self.minforcatalog.get_parent_list(),
        }
        self.render('infor/publish/publish2.html',
                    userinfo=self.userinfo,
                    kwd=kwd)
