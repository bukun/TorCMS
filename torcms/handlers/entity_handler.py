# -*- coding:utf-8 -*-

'''
Hander for entiey, such as files or URL.
'''
import os
import uuid
import json
import tornado.web

import config
from torcms.core.base_handler import BaseHandler
from torcms.model.entity_model import MEntity
from torcms.model.entity2user_model import MEntity2User
from torcms.model.post_model import MPost
from torcms.core import tools

from PIL import Image

# TMPL_SIZE = (768, 768)
# THUMBNAIL_SIZE = (256, 256)

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'tif', 'bmp']

ALLOWED_EXTENSIONS_PDF = ['pdf', 'doc', 'docx', 'zip', 'rar', 'ppt', '7z', 'xlsx']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PDF


class EntityHandler(BaseHandler):
    '''
    Hander for entiey, such as files or URL.
    '''

    def initialize(self, **kwargs):
        super(EntityHandler, self).initialize()
        self.entity_ajax = False

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        if url_str in ['add', '_add']:
            self.to_add()
        elif url_str == 'list' or url_str == '':
            self.list()

        elif len(url_str) > 36:
            self.view(url_str)
        elif len(url_arr) == 1:
            self.list(url_arr[0])
        else:
            self.render('misc/html/404.html', kwd={}, userinfo=self.userinfo)

    def post(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        # url_arr = self.parse_url(url_str)
        if url_str in ['add_img', 'add', '', '_add']:
            self.add_entity()
        elif url_arr[0] == 'down':
            self.down(url_arr[1])
        else:
            self.render('misc/html/404.html', kwd={}, userinfo=self.userinfo)

    @tornado.web.authenticated
    def list(self, cur_p=''):
        '''
        Lists of the entities.
        '''

        current_page_number = int(cur_p) if cur_p else 1
        current_page_number = 1 if current_page_number < 1 else current_page_number

        kwd = {
            'current_page': current_page_number
        }
        recs = MEntity.get_all_pager(current_page_num=current_page_number)
        self.render('misc/entity/entity_list.html',
                    imgs=recs,
                    cfg=config.CMS_CFG,
                    kwd=kwd,
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def down(self, down_uid):
        '''
        Download the entity by UID.
        '''

        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)[0]

        down_url = MPost.get_by_uid(down_uid).extinfo.get('tag__file_download', '')
        if down_url:

            if allowed_file(down_url):
                kind = '1'
            elif allowed_file_pdf(down_url):
                kind = '2'
            else:
                kind = '3'

            ment_id = MEntity.get_id_by_impath(down_url)

            userip = self.get_host_ip()

            if ment_id:

                MEntity2User.create_entity2user(ment_id, self.userinfo.uid, userip)

                return True
            else:

                MEntity.create_entity(uid='', path=down_url, desc='', kind=kind)
                ment_id = MEntity.get_id_by_impath(down_url)
                if ment_id:
                    MEntity2User.create_entity2user(ment_id, self.userinfo.uid, userip)
                    return True
        else:
            return False



    @tornado.web.authenticated
    def to_add(self):
        '''
        To add the entity.
        '''
        kwd = {
            'pager': '',
        }
        self.render('misc/entity/entity_add.html',
                    cfg=config.CMS_CFG,
                    kwd=kwd,
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def add_entity(self):
        '''
        Add the entity. All the information got from the post data.
        '''
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
            self.add_pic(post_data)

    @tornado.web.authenticated
    def add_pic(self, post_data):
        '''
        Adding the picture.
        '''
        img_entity = self.request.files['file'][0]
        filename = img_entity["filename"]

        if filename and allowed_file(filename):
            pass
        else:
            return False

        _, hou = os.path.splitext(filename)
        signature = str(uuid.uuid1())
        outfilename = '{0}{1}'.format(signature, hou)
        outpath = 'static/upload/{0}'.format(signature[:2])
        if os.path.exists(outpath):
            pass
        else:
            os.makedirs(outpath)
        with open(os.path.join(outpath, outfilename), "wb") as fileout:
            fileout.write(img_entity["body"])
        path_save = os.path.join(signature[:2], outfilename)
        sig_save = os.path.join(signature[:2], signature)

        imgpath = os.path.join(outpath, signature + '_m.jpg')
        imgpath_sm = os.path.join(outpath, signature + '_sm.jpg')

        ptr_image = Image.open(os.path.join('static/upload', path_save))
        tmpl_size = (768, 768)
        thub_size = (256, 256)
        (imgwidth, imgheight) = ptr_image.size
        if imgwidth < tmpl_size[0] and imgheight < tmpl_size[1]:
            tmpl_size = (imgwidth, imgheight)
        ptr_image.thumbnail(tmpl_size)

        im0 = ptr_image.convert('RGB')
        im0.save(imgpath, 'JPEG')

        im0.thumbnail(thub_size)
        im0.save(imgpath_sm, 'JPEG')

        create_pic = MEntity.create_entity(signature,
                                           path_save,
                                           post_data['desc'] if 'desc' in post_data else '',
                                           kind=post_data['kind'] if 'kind' in post_data else '1')
        if self.entity_ajax == False:
            self.redirect('/entity/{0}_m.jpg'.format(sig_save))
        else:
            if create_pic:
                output = {'path_save': imgpath}
            else:
                output = {'path_save': ''}
            return json.dump(output, self)

    @tornado.web.authenticated
    def add_pdf(self, post_data):
        '''
        Adding the pdf file.
        '''

        img_entity = self.request.files['file'][0]
        img_desc = post_data['desc']
        filename = img_entity["filename"]

        if filename and allowed_file_pdf(filename):
            pass
        else:
            return False

        _, hou = os.path.splitext(filename)
        signature = str(uuid.uuid1())
        outfilename = '{0}{1}'.format(signature, hou)
        outpath = 'static/upload/{0}'.format(signature[:2])
        if os.path.exists(outpath):
            pass
        else:
            os.makedirs(outpath)
        with open(os.path.join(outpath, outfilename), "wb") as fout:
            fout.write(img_entity["body"])

        sig_save = os.path.join(signature[:2], signature)
        path_save = os.path.join(signature[:2], outfilename)
        create_pdf = MEntity.create_entity(signature, path_save, img_desc,
                                           kind=post_data['kind'] if 'kind' in post_data else '2')
        if self.entity_ajax == False:
            self.redirect('/entity/{0}{1}'.format(sig_save, hou.lower()))
        else:
            if create_pdf:
                output = {'path_save': path_save}
            else:
                output = {'path_save': ''}
            return json.dump(output, self)

    @tornado.web.authenticated
    def add_url(self, post_data):
        '''
        Adding the URL as entity.
        '''
        img_desc = post_data['desc']
        img_path = post_data['file1']
        cur_uid = tools.get_uudd(4)
        while MEntity.get_by_uid(cur_uid):
            cur_uid = tools.get_uudd(4)
        MEntity.create_entity(cur_uid, img_path, img_desc, kind=post_data['kind'] if 'kind' in post_data else '3')
        kwd = {
            'kind': post_data['kind'] if 'kind' in post_data else '3',

        }
        self.render('misc/entity/entity_view.html',
                    filename=img_path,
                    cfg=config.CMS_CFG,
                    kwd=kwd,
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def view(self, outfilename):
        kwd = {
            'pager': '',
            'kind': ''

        }
        self.render('misc/entity/entity_view.html',
                    filename=outfilename,
                    cfg=config.CMS_CFG,
                    kwd=kwd,
                    userinfo=self.userinfo, )


class EntityAjaxHandler(EntityHandler):
    '''
    Hander for entiey, such as files or URL.
    '''

    def initialize(self, **kwargs):
        super(EntityAjaxHandler, self).initialize()
        self.entity_ajax = True
