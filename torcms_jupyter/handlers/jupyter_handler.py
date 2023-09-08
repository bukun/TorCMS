import tornado.escape
import json
import config
import os
import uuid
import bs4
import re
import shutil
import subprocess

from pathlib import Path
from torcms.core.tools import get_uu4d, get_uu8d
from config import CMS_CFG, post_cfg
from torcms.handlers.post_handler import PostHandler
from torcms.core.tools import logger
from torcms.model.post_model import MPost
from torcms.core import privilege
from torcms.model.category_model import MCategory
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.label_model import MPost2Label
from torcms.model.post_hist_model import MPostHist
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from torcms.model.entity_model import MEntity

pwd = os.getcwd()

rest_regs = [
    # '\s:.+?:`.+?`\/:.+?:`.+?`\/:.+?:`.+?`'
    '\<img.+?\/\>',  # 形如：   ``sadf``: :sdf:`slfkj`

]


def update_category(uid, post_data):
    '''
    Update the category of the post.
    :param uid:  The ID of the post. Extra info would get by requests.
    '''

    # deprecated
    # catid = kwargs['catid'] if MCategory.get_by_uid(kwargs.get('catid')) else None
    # post_data = self.get_request_arguments()
    if 'gcat0' in post_data:
        pass
    else:
        return False

    # Used to update MPost2Category, to keep order.
    the_cats_arr = []
    # Used to update post extinfo.
    the_cats_dict = {}

    # for old page. deprecated
    # def_cate_arr.append('def_cat_uid')

    def_cate_arr = ['gcat{0}'.format(x) for x in range(10)]
    for key in def_cate_arr:
        if key not in post_data:
            continue
        if post_data[key] == '' or post_data[key] == '0':
            continue
        # 有可能选重复了。保留前面的
        if post_data[key] in the_cats_arr:
            continue

        the_cats_arr.append(post_data[key] + ' ' * (4 - len(post_data[key])))
        the_cats_dict[key] = post_data[key] + ' ' * (4 - len(post_data[key]))

    # if catid:
    #     def_cat_id = catid
    if the_cats_arr:
        def_cat_id = the_cats_arr[0]
    else:
        def_cat_id = None

    if def_cat_id:
        the_cats_dict['gcat0'] = def_cat_id
        the_cats_dict['def_cat_uid'] = def_cat_id
        the_cats_dict['def_cat_pid'] = MCategory.get_by_uid(def_cat_id).pid

    # Add the category
    logger.info('Update category: {0}'.format(the_cats_arr))
    logger.info('Update category: {0}'.format(the_cats_dict))

    MPost.update_jsonb(uid, the_cats_dict)

    for index, idx_catid in enumerate(the_cats_arr):
        MPost2Catalog.add_record(uid, idx_catid, index)

    # Delete the old category if not in post requests.
    current_infos = MPost2Catalog.query_by_entity_uid(uid, kind='').objects()
    for cur_info in current_infos:
        if cur_info.tag_id not in the_cats_arr:
            MPost2Catalog.remove_relation(uid, cur_info.tag_id)


def update_label(signature, post_data):
    '''
    Update the label when updating.
    '''
    current_tag_infos = MPost2Label.get_by_uid(signature).objects()
    if 'tags' in post_data:
        pass
    else:
        return False
    if '；' in post_data['tags']:
        tags_arr = [x.strip() for x in post_data['tags'].split('；')]
    elif ',' in post_data['tags']:
        tags_arr = [x.strip() for x in post_data['tags'].split(',')]
    elif '，' in post_data['tags']:
        tags_arr = [x.strip() for x in post_data['tags'].split('，')]
    elif ';' in post_data['tags']:
        tags_arr = [x.strip() for x in post_data['tags'].split(';')]
    else:
        tags_arr = [x.strip() for x in post_data['tags'].split(',')]

    for tag_name in tags_arr:
        if tag_name == '':
            pass
        else:
            MPost2Label.add_record(signature, tag_name, 1)

    for cur_info in current_tag_infos:
        if cur_info.tag_name in tags_arr:
            pass
        else:
            MPost2Label.remove_relation(signature, cur_info.tag_id)


class JupyterHandler(PostHandler):

    def initialize(self, **kwargs):
        super(JupyterHandler, self).initialize(**kwargs)
        self.kind = kwargs.get('kind', 'j')

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        if url_str in ['data', 'index', '']:
            self.index()
        elif url_arr[0] == '_cat_add':
            self._to_add(catid=url_arr[1])

        elif url_arr[0] == '_add':
            if len(url_arr) == 2:
                self._to_add(uid=url_arr[1])
            else:
                self._to_add()
        elif len(url_arr) == 1:
            self._view_or_add(url_str)
        elif len(url_arr) == 2:
            dict_get = {
                '_edit_kind': self._to_edit_kind,
                '_edit': self._to_edit,
                '_delete': self._delete,
            }
            dict_get.get(url_arr[0])(url_arr[1])
        else:
            self.show404()

    def post(self, *args, **kwargs):

        url_str = args[0]
        logger.info('Post url: {0}'.format(url_str))
        url_arr = self.parse_url(url_str)

        if url_arr[0] in ['_edit']:
            self.update(url_arr[1])

        elif url_arr[0] in ['_add']:
            if len(url_arr) == 2:
                self.add(uid=url_arr[1])
            else:
                self.add()
        elif url_arr[0] == 'upload_jupyter':
            self.upload_jupyter()
        elif url_arr[0] == '_edit_kind':
            self._change_kind(url_arr[1])
        elif url_arr[0] in ['_cat_add']:
            self.add(catid=url_arr[1])
        elif len(url_arr) == 1 and len(url_str) >= 4:
            self.add(uid=url_str)
        elif url_arr[0] == 'rel' and len(url_arr) == 3:
            self._add_relation(url_arr[1], url_arr[2])
        else:
            self.show404()

    def fetch_post_data(self):
        '''
        fetch post accessed data. post_data, and ext_dic.
        '''
        post_data = {}
        ext_dic = {}
        ii = 1
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):

                ext_dic[key] = self.get_argument(key, default='')

            else:
                post_data[key] = self.get_arguments(key)[0]

        post_data['user_name'] = self.userinfo.user_name
        post_data['kind'] = self.kind

        if 'tags' in post_data:
            ext_dic['def_tag_arr'] = [
                x.strip() for x in post_data['tags'].strip().strip(',').split(',')
            ]
        ext_dic = dict(ext_dic, **self.ext_post_data(postdata=post_data))

        return (post_data, ext_dic)

    @tornado.web.authenticated
    @privilege.permission(action='can_add')
    # @tornado.web.asynchronous
    @tornado.gen.coroutine
    def add(self, **kwargs):
        '''
        in infor.
        '''

        post_data, ext_dic = self.fetch_post_data()

        if post_data.get('uid'):
            uid = post_data['uid']
        else:
            uid = self._gen_uid()

        title = post_data['title'].strip()

        if len(title) < 2:
            kwd = {
                'info': 'Title cannot be less than 2 characters',
                'link': '/'
            }
            self.render('misc/html/404.html', userinfo=self.userinfo, kwd=kwd)

        if 'gcat0' in post_data:
            pass
        else:
            return False

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = 1

        ext_dic['def_uid'] = uid
        ext_dic['gcat0'] = post_data['gcat0']
        ext_dic['def_cat_uid'] = post_data['gcat0']
        ext_dic['status'] = 'a0'

        # -----------------------------------------------

        MPost.add_or_update_post(ext_dic['def_uid'], post_data, extinfo=ext_dic)
        kwargs.pop('uid', None)  # delete `uid` if exists in kwargs

        self._add_download_entity(ext_dic)

        update_category(ext_dic['def_uid'], post_data)
        update_label(ext_dic['def_uid'], post_data)

        tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)
        self.redirect('/{0}/{1}'.format(post_cfg[self.kind]['router'], uid))

    @tornado.web.authenticated
    @privilege.permission(action='can_edit')
    @tornado.gen.coroutine
    def update(self, uid):
        '''
        in infor.
        '''

        post_data, ext_dic = self.fetch_post_data()
        if 'gcat0' in post_data:
            pass
        else:
            return False

        postinfo = MPost.get_by_uid(uid)

        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = postinfo.valid

        ext_dic['def_uid'] = postinfo.uid

        cnt_old = tornado.escape.xhtml_unescape(postinfo.cnt_md).strip()
        cnt_new = post_data['cnt_md'].strip()
        if cnt_old == cnt_new:
            pass
        else:
            MPostHist.create_post_history(postinfo, self.userinfo)

        MPost.add_or_update_post(postinfo.uid, post_data, extinfo=ext_dic)

        self._add_download_entity(ext_dic)

        update_category(postinfo.uid, post_data)
        update_label(postinfo.uid, post_data)

        logger.info('post kind:' + self.kind)
        tornado.ioloop.IOLoop.instance().add_callback(self.cele_gen_whoosh)
        self.redirect('/{0}/{1}'.format(post_cfg[postinfo.kind]['router'], postinfo.uid))

    @tornado.web.authenticated
    def upload_jupyter(self):
        '''
        Adding the pdf file.
        '''

        post_data = self.get_request_arguments()

        img_entity = self.request.files['file'][0]
        img_desc = img_entity["filename"]
        filename = img_entity["filename"]

        if filename and self.allowed_file_pdf(filename):
            pass
        else:
            kwd = {
                'pager': '',
                'err_info': '* The formats of uploadable files are: ipynb'
            }
            self.render('misc/entity/entity_add.html',
                        cfg=config.CMS_CFG,
                        kwd=kwd,
                        userinfo=self.userinfo)

        _, hou = os.path.splitext(filename)

        signature = str(uuid.uuid1())

        outfilename = filename
        outpath = 'static/zz_jupyter'

        if os.path.exists(outpath):
            pass
        else:
            os.makedirs(outpath)
        with open(os.path.join(outpath, outfilename), "wb") as fout:
            fout.write(img_entity["body"])

        sig_save = os.path.join(signature[:2], signature)
        path_save = os.path.join(signature[:2], outfilename)
        ispdf = MEntity.get_id_by_impath(outfilename)
        if ispdf:
            pass
        else:
            create_pdf = MEntity.create_entity(
                signature,
                outfilename,
                img_desc,
                kind=post_data['kind'] if 'kind' in post_data else 'j')


        file_src = os.path.join('./' + outpath + '/' + outfilename)

        ch_path = Path(os.path.join(file_src))

        uid = ch_path.stem.split('_')[-1]
        print(uid)

        subprocess.run(f'jupyter nbconvert --to html {ch_path.resolve()} --output /tmp/xx.html ', shell=True)

        html_file = '/tmp/xx.html'
        # File = open(str(the_file.resolve()))
        Soup = bs4.BeautifulSoup(open(html_file).read(), features="html.parser")
        title = Soup.select('h1')[0].getText()
        content = Soup.select('.jp-Notebook')
        print('========1111')

        # title.replace('{', '{{').replace('}', '}}')
        uu, vv = self.split_text(content)
        # content = vv.join(uu)

        # print(len(uu))
        # print(len(vv))
        result = [None] * (len(uu) + len(vv))
        result[::2] = uu
        result[1::2] = vv

        # print(result)

        content = ' '.join(result)[1:-1]

        # print('\033[0m')
        # content  = content.replace('&#182;', '')

        pp_data = {}

        pp_data['title'] = str(title)[:-1]
        pp_data['cnt_md'] = str(content).replace('class="container"', '')
        pp_data['kind'] = self.kind
        # 将主要数据添加到外扩展
        pp_data['extinfo'] = {
            'wx_vecode': get_uu4d(),
            'wx_dolink': os.path.join('/' + outpath + '/' + outfilename),
            'dc_uid': uid,
        }
        # 将kind修改为'k',输出外扩展方便查看验证码。
        print(pp_data['extinfo'])

        return json.dump(pp_data, self)

    @tornado.web.authenticated
    def split_text(self, in_text):
        '''
        根据正则表达式，找到特殊的字符串。
        对原始字符串进行切分。
        返回切分的结果，以及用来切分的特殊字符串。def get_docker_name(the_str):
        regobj = re.compile('\d\d\d-\d\d\d-\d\d\d\d')
        tt = regobj.search(the_str)
        print(tt)

        '''

        # in_text = in_text.replace('{', '{{').replace('}', '}}')

        # ToDo: '*,', '*.' ， 未处理。

        # 术语、参考
        phoneNumRegex = re.compile('|'.join(rest_regs))
        # print(in_text)
        in_text = str(in_text)

        out_reg_arr = phoneNumRegex.findall(in_text)
        #     print(out_reg_arr)
        # out_reg_arr = self.filter_reg_text(inws, out_reg_arr)

        if out_reg_arr:
            out_text_arr = phoneNumRegex.split(in_text)
        else:
            out_text_arr = [in_text]

        return out_text_arr, out_reg_arr

    def allowed_file_pdf(self, filename):
        '''
        Allowed xlsx files
        '''
        ALLOWED_EXTENSIONS_PDF = ['ipynb']
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PDF

    @tornado.web.authenticated
    def filter_reg_text(self, inws, out_reg_arr):
        outarr = []

        for item in out_reg_arr:
            item = item[5:-2]
            bbs = item.split()

            tt = []
            for bb in bbs:
                if bb.startswith('src'):
                    # print('=' * 40)
                    bb = bb.strip('"')
                    iiis = bb.split('/')
                    img = iiis[-1]
                    # print(img)

                    # ToDo: 图像的查找路径需要修改
                    img_path = Path(inws)
                    for wfile in img_path.rglob('*'):
                        # print('-' * 20)
                        # print(wfile.name)
                        if img == wfile.name:
                            img = str(wfile.resolve())[len(pwd):]
                    # print(img)
                    tt.append('src="{}"'.format(img))
                else:
                    tt.append(bb)

            outarr.append('<img {} />'.format(' '.join(tt)))
        return outarr
        # return '<img {} />'.format(' '.join(tt))
