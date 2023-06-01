# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.user_model import MUser
from torcms.model.role_model import MRole
from torcms.model.process_model import MProcess, MState, MTransition, MRequest, MAction, MRequestAction, \
    MTransitionAction, MPermissionAction

from faker import Faker


class TestMProcess():
    def setup_method(self):

        print('setup 方法执行于本类中每条用例之前')

        self.uid = tools.get_uu4d()

        self.user_id = MUser.get_by_name('admin').uid
        self.state_dic = {}
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

        self.fake = Faker(locale="zh_CN")

    def test_process(self):
        '''
        创建流程TabProcess
        '''
        # 创建Post

        process_name = 'test数据审核' + self.uid
        process_id = self.mprocess.create(process_name)
        if process_id:
            self.process_id = process_id
            # 创建动作
            self.test_action(process_id)

            # 创建状态
            self.test_state(process_id)

            # 创建状态转换
            self.test_trans(process_id, self.state_dic)
        self.tearDown(process_id)

    def test_state(self, process_id=''):
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
            state_data['process'] = process_id
            state_uid = MState.create(state_data)
            self.state_dic[state_data['state_type']] = state_uid

        assert self.state_dic

    def test_action(self, process_id=''):
        '''
        创建动作TabAction
        '''

        action_datas = [
            {'action_type': 'deny', 'role': 'ucan_verify',
             'name': '拒绝', 'description': '操作人将请求应移至上一个状态'},
            {'action_type': 'cancel', 'role': 'ucan_verify',
             'name': '取消', 'description': '操作人将请求应在此过程中移至“已取消”状态'},
            {'action_type': 'approve', 'role': 'ucan_verify',
             'name': '通过', 'description': '操作人将请求应移至下一个状态'},
            {'action_type': 'restart', 'role': '9can_edit',
             'name': '提交审核', 'description': '操作人将将请求移回到进程中的“开始”状态'},

        ]

        action_uids = []
        for act in action_datas:
            act_uid = MAction.create(process_id, act)
            action_uids.append(act_uid)
            print("*" * 50)
            print(act['role'])
            if act_uid:
                self.mper_action.create(act['role'], act_uid)

        assert action_uids

    def test_trans(self, process_id='', state_dic={}):
        '''
         转换Tabtransition
        '''
        if process_id:
            deny = 'deny_' + process_id
            cancel = 'cancel_' + process_id
            restart = 'restart_' + process_id
            approve = 'approve_' + process_id

            act_deny = MAction.get_by_action_type(deny).uid
            act_cancel = MAction.get_by_action_type(cancel).uid

            act_restart = MAction.get_by_action_type(restart).uid
            act_approve = MAction.get_by_action_type(approve).uid

            trans = [
                # 状态：“正常”对应的“开始”
                {'current_state': state_dic['normal'],
                 'next_state': state_dic['start'], 'act_id': act_restart},

                # 状态：“开始”对应的“拒绝”，“完成”，“取消”
                {'current_state': state_dic['start'],
                 'next_state': state_dic['denied'], 'act_id': act_deny},
                {'current_state': state_dic['start'],
                 'next_state': state_dic['complete'], 'act_id': act_approve},
                {'current_state': state_dic['start'],
                 'next_state': state_dic['cancelled'], 'act_id': act_cancel},

                # 状态：“取消”对应的“拒绝”，“完成”
                {'current_state': state_dic['cancelled'],
                 'next_state': state_dic['denied'], 'act_id': act_deny},
                {'current_state': state_dic['cancelled'],
                 'next_state': state_dic['complete'], 'act_id': act_approve},

                # 状态：“拒绝”对应的“开始”
                {'current_state': state_dic['denied'],
                 'next_state': state_dic['start'], 'act_id': act_restart},

            ]

            for tran in trans:
                tran_id = MTransition.create(process_id, tran['current_state'], tran['next_state'])

                # 创建转换动作

                MTransitionAction.create(tran_id, tran['act_id'])

            # assert True

    def tearDown(self, process_id=''):
        print("function teardown")
        trans = self.mtrans.query_by_proid(process_id)
        print(trans.count())
        for tran in trans:
            print("*" * 50)
            print(tran.uid)

            self.mtransaction.delete_by_trans(tran.uid)
            self.mtrans.delete(tran.uid)

        req_recs = self.mrequest.get_by_pro(process_id)
        if req_recs:
            for req_rec in req_recs:
                print(req_rec.uid)
                self.mrequest.delete(req_rec.uid)

        act_recs = MAction.query_by_proid(process_id)
        for act in act_recs:
            self.mper_action.delete_by_action(act.uid)
            self.maction.delete(act.uid)

        states = self.mstate.query_by_pro_id(process_id)
        for state in states:
            self.mstate.delete(state.uid)

        self.mprocess.delete_by_uid(process_id)
