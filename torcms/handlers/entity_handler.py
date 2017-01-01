# -*- coding:utf-8 -*-
import os
import uuid

import tornado.ioloop
import tornado.web

import config
from torcms.core.base_handler import BaseHandler
from torcms.model.picture_model import MEntity

from PIL import Image

tmpl_size = (768, 768)
thub_size = (256, 256)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

ALLOWED_EXTENSIONS_PDF = set(['pdf', 'doc', 'docx', 'zip','rar'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PDF


class EntityHandler(BaseHandler):
    def initialize(self):
        super(EntityHandler, self).initialize()
        self.mpic = MEntity()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_str == 'add':
            self.to_add()
        elif (url_str == 'list' or url_str == ''):
            self.list()
        elif len(url_str) > 36:
            self.view(url_str)
        else:
            self.render('html/404.html', kwd={}, userinfo=self.userinfo)

    def post(self, url_str=''):
        url_arr = self.parse_url(url_str)
        if url_str == 'add_img' or url_str == 'add' or url_str == '':
            self.add_entity()
        else:
            self.render('html/404.html', kwd={}, userinfo=self.userinfo)

    @tornado.web.authenticated
    def list(self):
        recs = self.mpic.getall()
        kwd = {
            'pager': '',
        }
        self.render('doc/entry/entry_list.html',
                    imgs=recs,
                    cfg=config.cfg,
                    kwd=kwd,
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def to_add(self):
        kwd = {
            'pager': '',
        }
        self.render('doc/entry/entry_add.html',
                    cfg=config.cfg,
                    kwd=kwd,
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def add_entity(self):

        post_data = self.get_post_data()

        if 'kind' in post_data:
            if post_data['kind'] == '1':
                self.add_pic()
            elif post_data['kind'] == '2':
                self.add_pdf()
            else:
                pass
        else:
            self.add_pic()


    @tornado.web.authenticated
    def add_pic(self):
        img_entiry = self.request.files['file'][0]

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

        self.mpic.insert_data(signature, sig_save)

        self.redirect('/entity/{0}_m.jpg'.format(sig_save))

    @tornado.web.authenticated
    def add_pdf(self):

        img_entiry = self.request.files['file'][0]

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
        with open(os.path.join(outpath, outfilename), "wb") as f:
            f.write(img_entiry["body"])

        sig_save = os.path.join(signature[:2], signature)


        self.mpic.insert_data(signature, sig_save)

        self.redirect('/entity/{0}{1}'.format(sig_save,  hou.lower()))

    @tornado.web.authenticated
    def view(self, outfilename):
        kwd = {
            'pager': '',

        }
        self.render('doc/entry/entry_view.html',
                    filename=outfilename,
                    cfg=config.cfg,
                    kwd=kwd,
                    userinfo=self.userinfo, )
