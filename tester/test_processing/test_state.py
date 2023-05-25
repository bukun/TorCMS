# -*- coding:utf-8 -*-
from torcms.core import tools
from torcms.model.user_model import MUser
from torcms.model.role_model import MRole
from torcms.model.process_model import MProcess, MState, MTransition, MRequest, MAction, MRequestAction, \
    MTransitionAction, MPermissionAction

from faker import Faker


class TestMstate():
    def setup_method(self):

        print('setup 方法执行于本类中每条用例之前')

        self.uid = tools.get_uu4d()

        self.mprocess = MProcess()
        self.mstate = MState()
        self.mtrans = MTransition()
        self.mrequest = MRequest()
        self.maction = MAction()
        self.mreqaction = MRequestAction()
        self.mtransaction = MTransitionAction()
        self.muser = MUser()
        self.mrole = MRole()
        self.mper_action = MPermissionAction()
        self.state_dic = {}
        self.process_id = self.init_process()

        self.fake = Faker(locale="zh_CN")

    def init_process(self):
        '''
        创建流程TabProcess
        '''

        process_name = '数据审核' + self.uid
        process_id = self.mprocess.create(process_name)
        return process_id

    def test_create_state(self):
        '''
        创建状态TabState
        '''

        state_datas = [
            {'name': '开始', 'state_type': 'start',
             'description': '每个进程只应该一个。此状态是创建新请求时所处的状态'},
            {'name': '拒绝', 'state_type': 'denied',
             'description': '表示此状态下的任何请求已被拒绝的状态(例如，从未开始且不会被处理)'},
            {'name': '完成', 'state_type': 'complete',
             'description': '表示此状态下的任何请求已正常完成的状态'},
            {'name': '取消', 'state_type': 'cancelled',
             'description': '表示此状态下的任何请求已被取消的状态(例如，工作已开始但尚未完成)'},
            {'name': '正常', 'state_type': 'normal',
             'description': '没有特殊名称的常规状态'},

        ]

        for state_data in state_datas:
            state_data['process'] = self.process_id
            state_uid = MState.create(state_data)
            self.state_dic[state_data['state_type']] = state_uid

            uu = self.mstate.get_by_state_type(state_data['state_type'] + '_' + self.process_id)

            assert uu.uid == state_uid

    def text_update_state(self):
        post_data1 = {
            'process': 'adf',
            'name': 'asdf',
            'state_type': 'asdf',
            'description': 'afd'
        }
        recs = self.mstate.get_by_name('开始')
        for rec in recs:
            uu = self.mstate.update(rec.uid, post_data1)
            assert uu == False

        post_data2 = {
            'process': self.process_id,
            'name': 'asdf',
            'state_type': 'asdf',
            'description': 'afd'
        }
        rec = self.mstate.get_by_name('开始')

        uu = self.mstate.update(rec.uid, post_data2)
        assert uu == False

        post_data3 = {
            'process': self.process_id,
            'name': '',
            'state_type': '',
            'description': 'afd'
        }
        recs = self.mstate.query_by_pro_id(self.process_id)
        for rec in recs:
            uu = self.mstate.update(rec.uid, post_data3)
            assert uu == True

        post_data4 = {
            'process': self.process_id,
            'name': '',
            'state_type': 'adf',
            'description': ''
        }
        recs = self.mstate.query_by_pro_id(self.process_id)
        for rec in recs:
            uu = self.mstate.update(rec.uid, post_data4)
            assert uu == False

        post_data5 = {
            'process': self.process_id,
            'name': '',
            'state_type': 'adf' + self.uid,
            'description': ''
        }
        recs = self.mstate.query_by_pro_id(self.process_id)
        for rec in recs:
            uu = self.mstate.update(rec.uid, post_data5)
            assert uu == True

        self.tearDown()

    def test_query_all(self):
        self.test_create_state()

        pp = self.mstate.query_all()
        TF = False
        for i in pp:

            if i.name in ['开始', '拒绝', '完成', '取消', '正常']:
                TF = True
        self.tearDown()
        assert TF

    def test_query_by_proid(self):
        self.test_create_state()

        pp = self.mstate.query_by_pro_id(self.process_id)
        TF = False

        if pp.count() == 5:
            TF = True
        self.tearDown()
        assert TF

    def test_get_by_name(self):
        self.test_create_state()

        pp = self.mstate.get_by_name('取消').get()
        TF = False
        if pp.state_type.startswith('cancelled'):
            TF = True
        self.tearDown()
        assert TF

    def test_get_by_state_type(self):
        self.test_create_state()
        act_type = 'denied_' + self.process_id
        pp = self.mstate.get_by_state_type(act_type)
        TF = False
        print('9' * 50)
        print(pp.name)
        if pp.name == '拒绝':
            TF = True
        self.tearDown()
        assert TF

    def test_get_by_pro_statename(self):
        self.test_create_state()
        pp = self.mstate.get_by_pro_statename(self.process_id, '完成').get()
        TF = False

        if pp.state_type == 'complete_' + self.process_id:
            TF = True
        self.tearDown()
        assert TF

    def test_update_process(self):
        process_id = self.mprocess.create('test_pro' + self.uid)

        self.test_create_state()
        post_data = {'process': process_id}
        state_id = self.state_dic['complete']
        self.mstate.update_process(state_id, post_data)
        state_rec = self.mstate.get_by_uid(state_id).get()

        assert state_rec.process_id == process_id
        self.tearDown(process_id)

    def tearDown(self, process_id=''):
        print("function teardown")
        if process_id:
            pass
        else:
            process_id = self.process_id
        act_recs = self.mstate.query_by_pro_id(process_id)

        for act in act_recs:
            self.mstate.delete(act.uid)

        self.mprocess.delete_by_uid(process_id)
