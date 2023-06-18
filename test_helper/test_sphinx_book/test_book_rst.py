# -*- coding:utf-8 -*-
from torcms.core import tools
from pathlib import Path
from torcms.model.post_model import MPost
from torcms.model.process_model import MProcess, MState, MTransition, MRequest, MAction, MRequestAction, \
    MTransitionAction, MPermissionAction
from torcms.handlers.post_handler import import_post

from torcms.core.tools import get_uu4d, rst2html

from faker import Faker


class TestFoo():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')

        self.uid = tools.get_uu4d()
        self.fake = Faker(locale="zh_CN")
        self.ws_dir = Path(__file__ ).parent / 'book_demo'
        print(self.ws_dir)
    def teardown_method(self):
        # self.new_rst_file.unlink()
        # self.new_sec_dir.rmdir()
        # self.ch_dir.rmdir()
        # print('x' * 40)
        # self.ws_dir.rmdir()
        print("function teardown .. ")


    def test(self):
        assert self.ws_dir.exists()

        for wfile in self.ws_dir.rglob('*.rst'):
            if 'sec' in wfile.parent.name :
                self.insert_rst(wfile)

    def insert_rst(self, rst_file):
        post_data = {}

        uid = rst_file.parent.name.split('_')[-1]
        print(uid)
        while MPost.get_by_uid(uid):
            uid = 'k' + get_uu4d()

        rst_info = rst2html(
            open(rst_file).read()
        )
        post_data['valid'] = 0
        post_data['title'] = rst_info['title']
        post_data['cnt_md'] = rst_info['cnt']
        post_data['user_name'] = 'admin'
        post_data['kind'] = 'k'
        post_data['gcat0'] = 'k101'
        post_data['valid'] = 1
        # post_data['order'] =

        # kwargsa = {
        #     'gcat0': '0101',
        #     'cat_id': '0101',
        # }
        assert not MPost.get_by_uid(uid)
        import_post(uid, post_data )
        assert MPost.get_by_uid(uid)
        print(uid)

        sec_dir = rst_file.parent
        new_sec_dir = sec_dir.parent / f'{sec_dir.name}_{uid}'

        # sec_dir.rename(new_sec_dir)
