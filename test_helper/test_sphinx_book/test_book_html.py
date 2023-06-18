# -*- coding:utf-8 -*-
import re

from torcms.core import tools
from pathlib import Path
from torcms.model.post_model import MPost
from torcms.model.process_model import MProcess, MState, MTransition, MRequest, MAction, MRequestAction, \
    MTransitionAction, MPermissionAction
from torcms.handlers.post_handler import import_post


import bs4

from faker import Faker
from pprint import pprint


class TestFoo():
    def setup_method(self):
        print('setup 方法执行于本类中每条用例之前')

        self.uid = tools.get_uu4d()
        self.fake = Faker(locale="zh_CN")
        self.ws_dir = Path(__file__).parent / 'book_demo/xx_build/html'
        self.re_pt = re.compile('\/pt\d\d')
        self.re_ch = re.compile('\/ch\d\d')
        self.re_sec = re.compile('\/sec\d\d')
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

        for wfile in self.ws_dir.rglob('*.html'):
            if 'sec' in wfile.parent.name:
                self.insert_rst(wfile)

    def get_html(self, html_file):

        File = open(str(html_file.resolve()))
        Soup = bs4.BeautifulSoup(File.read(), features="html.parser")
        title = 'title'
        content = Soup.select('.body')[0]
        conz = ''
        for a in content.find_all(["h1", "p"]):
            conz += str(a)

        return {'title': title, 'cnt': conz}

    def insert_rst(self, html_file):
        print('=' * 40)
        print(html_file)
        post_data = {}

        pt_sig = self.re_pt.findall(str(html_file))[0][-2:]
        ch_sig = self.re_ch.findall(str(html_file))[0][-2:]
        sec_sig = self.re_sec.findall(str(html_file))[0][-2:]

        order_str = pt_sig + ch_sig + sec_sig
        print(order_str)

        uid = html_file.parent.name.split('_')[-1]
        # print(uid)
        # while MPost.get_by_uid(uid):
        #     uid = 'k' + get_uu4d()

        rst_info = self.get_html(html_file)
        post_data['valid'] = 0
        post_data['title'] = rst_info['title']
        post_data['cnt_md'] = rst_info['cnt']
        post_data['user_name'] = 'admin'
        post_data['kind'] = 'k'
        post_data['gcat0'] = html_file.parent.parent.name.split('_')[-1]
        post_data['valid'] = 1
        post_data['order'] = int(order_str)

        # assert not MPost.get_by_uid(uid)
        import_post(uid, post_data)
        assert MPost.get_by_uid(uid)
        print(uid)
        pprint(post_data)

        sec_dir = html_file.parent
        new_sec_dir = sec_dir.parent / f'{sec_dir.name}_{uid}'

        # sec_dir.rename(new_sec_dir)
