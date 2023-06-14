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

        self.ws_dir = Path('./xx_rst')
        if self.ws_dir.exists():
            pass
        else:
            self.ws_dir.mkdir(parents=True)
        self.ch_dir = self.ws_dir / 'ch01_the-name'
        if self.ch_dir.exists():
            pass
        else:
            self.ch_dir.mkdir()

        self.sec_name = 'sec01_name-the'
        self.sec_dir = self.ch_dir / self.sec_name
        if self.sec_dir.exists():
            pass
        else:
            self.sec_dir.mkdir()

        self.rst_file = self.sec_dir / 'section.rst'

        self.new_sec_dir = None
        self.new_rst_file = None

        self.init()

    def init(self):
        with open(self.rst_file, 'w') as fo:
            fo.write(self.fake.text().splitlines()[0][:20] + '\n')
            fo.write('=' * 40 + '\n\n')

            for ii in range(10):
                fo.write(self.fake.text() + '\n\n')

    def test(self):
        assert self.ws_dir.exists()

        ext_dic = {}
        post_data = {}

        uid = '1' + get_uu4d()
        while MPost.get_by_uid(uid):
            uid = '1' + get_uu4d()

        post_data['valid'] = 0
        post_data['title'] = self.fake.company_prefix()
        post_data['cnt_md'] = rst2html(
            open(self.rst_file).read()
        )
        post_data['user_name'] = 'admin'
        post_data['kind'] = '1'
        post_data['gcat0'] = '0101'

        ext_dic['def_uid'] = uid
        ext_dic['gcat0'] = '0101'
        ext_dic['def_cat_uid'] = '0101'

        # kwargsa = {
        #     'gcat0': '0101',
        #     'cat_id': '0101',
        # }
        assert not MPost.get_by_uid(uid)
        import_post(uid, post_data, ext_dic)
        assert MPost.get_by_uid(uid)

        self.new_sec_dir = (self.ch_dir / f'{self.sec_name}_{uid}')
        self.new_rst_file = self.new_sec_dir / 'section.rst'

        assert self.sec_dir.rename(self.new_sec_dir)
        print(uid)

    # def tearDown(self, process_id=''):
    #     self.ws_dir.rmdir()
    #     print("function teardown")

    # def teardown_class(self, process_id=''):
    #     self.ws_dir.rmdir()
    #     print("function teardown")

    def teardown_method(self, process_id=''):
        self.new_rst_file.unlink()
        self.new_sec_dir.rmdir()
        self.ch_dir.rmdir()
        print('x' * 40)
        # self.ws_dir.rmdir()
        print("function teardown .. ")
