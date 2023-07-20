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
        # self.ws_dir = Path(__file__).parent / 'book_eb1243/xx_build/html'
        # self.ws_dir = Path('/home/bk/book-rst/doculet/pt01_language_eb00kh')
        self.ws_dir = Path('/home/bk/book-rst/doculet/pt02_web_eb00ka')
        self.re_pt = re.compile('\/pt\d\d')
        self.re_ch = re.compile('\/ch\d\d')
        self.re_sec = re.compile('\/sec\d\d')

        self.re_book = re.compile('eb\d\d..')
        print(self.ws_dir)

        self.book_sig = self.re_book.search(str(self.ws_dir))

        self.img_ws = Path(
            f'static/xx_book_{self.book_sig.group()}'
        )

    def test_sig_exists(self):
        assert self.re_book.search(str(self.ws_dir))

    def teardown_method(self):
        # self.new_rst_file.unlink()
        # self.new_sec_dir.rmdir()
        # self.ch_dir.rmdir()
        # print('x' * 40)
        # self.ws_dir.rmdir()
        print("function teardown .. ")

    def test(self):
        if self.img_ws.exists():
            pass
        else:
            self.img_ws.mkdir()
        for wdir in self.ws_dir.rglob('_images'):

            for wfile in wdir.rglob('*'):
                print(wfile)
                if wfile.is_file():
                    outfile = self.img_ws / wfile.name
                    outfile.write_bytes(wfile.read_bytes())
                # with open(outfile, 'w') as fo:
                #     fo.wr
        assert self.ws_dir.exists()

        for wfile in self.ws_dir.rglob('*.html'):
            if 'sec' in wfile.parent.name and '_build' in str(wfile.resolve()):
                self.insert_rst(wfile)

    def get_html(self, html_file):

        File = open(str(html_file.resolve())).read()
        File = File.replace('src="../../../_images/', f'src="/static/xx_book_{self.book_sig.group()}/')
        File = File.replace('src="../../_images/',  f'src="/static/xx_book_{self.book_sig.group()}/')
        Soup = bs4.BeautifulSoup(File, features="html.parser")
        title = Soup.title.text.split('—')[0]
        content = Soup.select('.body')[0]
        conz = ''
        for a in content:
            conz += str(a) + '\n'

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
        pprint(post_data)
        import_post(uid, post_data)
        assert MPost.get_by_uid(uid)
        print(uid)


        sec_dir = html_file.parent
        new_sec_dir = sec_dir.parent / f'{sec_dir.name}_{uid}'

        # sec_dir.rename(new_sec_dir)
