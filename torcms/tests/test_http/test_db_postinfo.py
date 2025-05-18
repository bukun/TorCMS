# 针对导入的测试内容进行测试，当前测试页面时候能正常打开。
# 测试添加的能容能否正确打开。
'''
测试报错信息：
ERROR    tornado.general:web.py:3118 Could not open static file '/home/yubiao/gitee/TorCMS/static/f2elib/bootstrap-star-rating-master/css/star-rating.css'
ERROR    tornado.general:web.py:3118 Could not open static file '/home/yubiao/gitee/TorCMS/static/f2elib/bootstrap-star-rating-master/js/star-rating.js'
'''

import os
from datetime import datetime

import requests
from faker import Faker
from tornado.testing import AsyncHTTPSTestCase

from cfg import SITE_CFG
from config import post_cfg
from server import APP
from torcms.core.tools import get_uu4d, get_uuid
from torcms.model.category_model import MCategory
from torcms.model.post_model import MPost

fak = Faker('zh_CN')
domain = SITE_CFG['site_url']


class TestPostHandler(AsyncHTTPSTestCase):
    def get_app(self):
        return APP

    def test_posthandler_view_edit_delete(self):
        for key in post_cfg:
            if key not in ['2', 's']:
                postinfos = MPost.query_all(kind=key)
                for post in postinfos:
                    pass
                    # # Todo：app类型数据报错信息tornado.general:web.py:3118 Could not open static file '/gitee/TorCMS/static/f2elib/bootstrap-star-rating-master/css/star-rating.css'
                    print('=' * 80)
                    print('/{0}/{1}'.format(post_cfg[key]['router'], post.uid))
                    print('=' * 80)

                    response = self.fetch(
                        '/{0}/{1}'.format(post_cfg[key]['router'], post.uid)
                    )
                    self.assertEqual(response.code, 200)
                    # response_edit = self.fetch('/{0}/_edit/{1}'.format(post_cfg[key]['router'],post.uid))
                    # self.assertEqual(response_edit.code, 200)
                    # response_edit_kind = self.fetch('/{0}/_edit_kind/{1}'.format(post_cfg[key]['router'],post.uid))
                    # self.assertEqual(response_edit_kind.code, 200)
                    # # Todo：测试删除。在服务器端慎用。当前未验证用户登录和权限问题。
                    # response_delete = self.fetch('/{0}/_delete/{1}'.format(post_cfg[key]['router'], post.uid))
                    # # self.assertEqual(response_delete.code, 200)

    def test_tags(self):
        tags = MCategory.query_all()
        for tag in tags:
            if tag.kind in ['1', 'm', 'k']:
                response = self.fetch('/list/{0}'.format(tag.slug))
                self.assertEqual(response.code, 200)
            elif tag.kind == '3':
                print('tag.uid')
                print(tag.uid)
                response = self.fetch('/filter/{0}'.format(tag.uid))
                self.assertEqual(response.code, 200)

    def test_posthandler_add(self):
        for k in post_cfg:
            for ii in range(3):
                postuid = f'{k}{get_uu4d()}'
                while MPost.get_by_uid(postuid):
                    postuid = f'{k}{get_uu4d()}'

                response = self.fetch(
                    '/{0}/_add/{1}'.format(post_cfg[k]['router'], postuid)
                )
                self.assertEqual(response.code, 200)

    # # Todo:测试post，需要登录用户并有相关权限。
    # def test_posthandler_post(self):
    #     dt = datetime.now()
    #     for key in post_cfg:
    #         post_uid = f'{key}{get_uu4d()}'
    #         extinfo =''
    #         if key == 'm':
    #             extinfo = {
    #                 'ext_lon': fak.pyfloat(left_digits=3, right_digits=3, min_value=0, max_value=180),
    #                 'ext_lat': fak.pyfloat(left_digits=2, right_digits=3, min_value=0, max_value=90),
    #                 'ext_zoom_current': '4',
    #                 'ext_zoom_max': '7',
    #                 'ext_zoom_min': '1',
    #             }
    #         dict_info = {
    #             'uid': post_uid,
    #             'title': fak.text(max_nb_chars=5),
    #             'cnt_md': fak.text(max_nb_chars=300),
    #             'cnt_html': fak.text(max_nb_chars=300),
    #             'date': dt,
    #             'time_create': dt.timestamp(),
    #             'time_update': dt.timestamp(),
    #             'kind': key,
    #             'extinfo': extinfo
    #         }
    #         response = requests.post(os.path.join(domain, "{0}/_add".format(post_cfg[key]['router'])), json=dict_info)
    #         self.assertEqual(response.status_code, 200)

    # def test_posthandler_json(self):
    #     url = '/post_j/'
    #     pass
