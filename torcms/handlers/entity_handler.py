# -*- coding:utf-8 -*-
import os
import uuid

import tornado.ioloop
import tornado.web

import config
from torcms.core.base_handler import BaseHandler
from torcms.model.entity_model import MEntity
from torcms.core import tools
from PIL import Image

tmpl_size = (768, 768)
thub_size = (256, 256)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

ALLOWED_EXTENSIONS_PDF = set(['pdf', 'doc', 'docx', 'zip', 'rar', 'ppt'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PDF


class EntityHandler(BaseHandler):
    def initialize(self):
        super(EntityHandler, self).initialize()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_str == 'add':
            self.to_add()
        elif url_str == 'list' or url_str == '':
            self.list()
        elif len(url_str) > 36:
            self.view(url_str)
        elif len(url_arr) == 1:
            self.list(url_arr[0])
        else:
            self.render('misc/html/404.html', kwd={}, userinfo=self.userinfo)

    def post(self, url_str=''):
        url_arr = self.parse_url(url_str)
        if url_str == 'add_img' or url_str == 'add' or url_str == '':
            self.add_entity()
        else:
            self.render('misc/html/404.html', kwd={}, userinfo=self.userinfo)

    @tornado.web.authenticated
    def list(self, cur_p = '1'):

        if cur_p == '':
            current_page_number = 1
        else:
            current_page_number = int(cur_p)

        current_page_number = 1 if current_page_number < 1 else current_page_number
        kwd = {
               'current_page': current_page_number,
                'pager': ''
        }
        recs = MEntity.get_by_kind( current_page_num=current_page_number)
        self.render('misc/entity/entity_list.html',
                    imgs=recs,
                    cfg=config.CMS_CFG,
                    kwd=kwd,
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def to_add(self):
        kwd = {
            'pager': '',
        }
        self.render('misc/entity/entity_add.html',
                    cfg=config.CMS_CFG,
                    kwd=kwd,
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def add_entity(self):

        post_data = self.get_post_data()

        if 'kind' in post_data:
            if post_data['kind'] == '1':
                self.add_pic(post_data)
            elif post_data['kind'] == '2':
                self.add_pdf(post_data)
            elif post_data['kind'] == '3':
                self.add_url(post_data)
            else:
                pass
        else:
            self.add_pic()

    @tornado.web.authenticated
    def add_pic(self, post_data):
        img_entiry = self.request.files['file'][0]
        img_desc = post_data['desc']

        filename = img_entiry["filename"]

        if filename and allowed_file(filename):
            pass
        else:
            return False

        (qian, hou) = os.path.splitext(filename)
        signature = str(uuid.uuid1())
        outfilename = '{0}{1}'.format(signature, hou)
        outpath = 'static/upload/{0}'.format(signature[:2])
        if os.path.exists(outpath):
            pass
        else:
            os.makedirs(outpath)
        with open(os.path.join(outpath, outfilename), "wb") as f:
            f.write(img_entiry["body"])
        path_save = os.path.join(signature[:2], outfilename)
        sig_save = os.path.join(signature[:2], signature)

        imgpath = os.path.join(outpath, signature + '_m.jpg')
        imgpath_sm = os.path.join(outpath, signature + '_sm.jpg')

        im = Image.open(os.path.join('static/upload', path_save))
        tmpl_size = (768, 768)
        thub_size = (256, 256)
        (imgwidth, imgheight) = im.size
        if imgwidth < tmpl_size[0] and imgheight < tmpl_size[1]:
            tmpl_size = (imgwidth, imgheight)
        im.thumbnail(tmpl_size)

        im0 = im.convert('RGB')
        im0.save(imgpath, 'JPEG')

        im0.thumbnail(thub_size)
        im0.save(imgpath_sm, 'JPEG')

        MEntity.create_entity(signature, sig_save, img_desc, kind=1)

        self.redirect('/entity/{0}_m.jpg'.format(sig_save))

    @tornado.web.authenticated
    def add_pdf(self, post_data):

        img_entiry = self.request.files['file'][0]
        img_desc = post_data['desc']
        filename = img_entiry["filename"]

        qian, hou = os.path.splitext(filename)

        if filename and allowed_file_pdf(filename):
            pass
        else:
            return False

        (qian, hou) = os.path.splitext(filename)
        signature = str(uuid.uuid1())
        outfilename = '{0}{1}'.format(signature, hou)
        outpath = 'static/upload/{0}'.format(signature[:2])
        if os.path.exists(outpath):
            pass
        else:
            os.makedirs(outpath)
        with open(os.path.join(outpath, outfilename), "wb") as fout:
            fout.write(img_entiry["body"])

        sig_save = os.path.join(signature[:2], signature)

        MEntity.create_entity(signature, sig_save, img_desc, kind=2)

        self.redirect('/entity/{0}{1}'.format(sig_save, hou.lower()))
    @tornado.web.authenticated
    def add_url(self, post_data):

        img_desc = post_data['desc']
        img_path = post_data['file1']
        cur_uid = tools.get_uudd(4)
        while MEntity.get_by_uid(cur_uid):
            cur_uid = tools.get_uudd(4)
        MEntity.create_entity(cur_uid, img_path, img_desc, kind=3)

        self.redirect('/entity/'.format(img_path))

    @tornado.web.authenticated
    def view(self, outfilename):
        kwd = {
            'pager': '',

        }
        self.render('misc/entity/entity_view.html',
                    filename=outfilename,
                    cfg=config.CMS_CFG,
                    kwd=kwd,
                    userinfo=self.userinfo, )
