# -*- coding:utf-8 -*-
import re
from pathlib import Path
from pprint import pprint

from faker import Faker

from torcms.core import tools
from torcms.core.tools import get_uu4d, rst2html
from torcms.handlers.post_handler import import_post
from torcms.model.post_model import MPost
from torcms.model.process_model import (
    MAction,
    MPermissionAction,
    MProcess,
    MRequest,
    MRequestAction,
    MState,
    MTransition,
    MTransitionAction,
)


class TestFoo:
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')

        self.uid = tools.get_uu4d()
        self.fake = Faker(locale="zh_CN")
        self.ws_dir = Path(__file__).parent / 'book_demo'
        self.re_pt = re.compile(r'/pt\d\d')
        self.re_ch = re.compile(r'/ch\d\d')
        self.re_sec = re.compile(r'/sec\d\d')
        print(self.ws_dir)

    def teardown_method(self):
        # self.new_rst_file.unlink()
        # self.new_sec_dir.rmdir()
        # self.ch_dir.rmdir()
        # print('x' * 40)
        # self.ws_dir.rmdir()
        print("function teardown .. ")

    def test(self):

        # ToDo: 需要构建出来
        # assert self.ws_dir.exists()

        for wfile in self.ws_dir.rglob('*.rst'):
            if 'sec' in wfile.parent.name:
                self.insert_rst(wfile)

    def insert_rst(self, rst_file):
        print('=' * 40)
        print(rst_file)
        post_data = {}

        pt_sig = self.re_pt.findall(str(rst_file))[0][-2:]
        ch_sig = self.re_ch.findall(str(rst_file))[0][-2:]
        sec_sig = self.re_sec.findall(str(rst_file))[0][-2:]

        order_str = pt_sig + ch_sig + sec_sig
        print(order_str)

        uid = rst_file.parent.name.split('_')[-1]
        # print(uid)
        # while MPost.get_by_uid(uid):
        #     uid = 'k' + get_uu4d()

        rst_info = rst2html(open(rst_file).read())
        post_data['valid'] = 0
        post_data['title'] = rst_info['title']
        post_data['cnt_md'] = rst_info['cnt']
        post_data['user_name'] = 'admin'
        post_data['kind'] = 'k'
        post_data['gcat0'] = rst_file.parent.parent.name.split('_')[-1]
        post_data['valid'] = 1
        post_data['order'] = int(order_str)

        # assert not MPost.get_by_uid(uid)
        import_post(uid, post_data)
        assert MPost.get_by_uid(uid)
        print(uid)
        pprint(post_data)

        sec_dir = rst_file.parent
        new_sec_dir = sec_dir.parent / f'{sec_dir.name}_{uid}'

        # sec_dir.rename(new_sec_dir)
