# -*- coding:utf-8 -*-
from faker import Faker

from torcms.core import tools
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
from torcms.model.role_model import MRole
from torcms.model.user_model import MUser


class TestMtransition:
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
        self.init_data()
        self.init_transition()
        self.fake = Faker(locale="zh_CN")

    def init_process(self):
        '''
        创建流程TabProcess
        '''

        process_name = 'test数据审核' + self.uid
        process_id = self.mprocess.create(process_name)
        return process_id

    def init_data(self):
        '''
        初始化状态，动作
        '''

        # 创建状态TabState

        state_datas = [
            {
                'name': '开始',
                'state_type': 'start',
                'description': '每个进程只应该一个。此状态是创建新请求时所处的状态',
            },
            {
                'name': '拒绝',
                'state_type': 'denied',
                'description': '表示此状态下的任何请求已被拒绝的状态(例如，从未开始且不会被处理)',
            },
            {
                'name': '完成',
                'state_type': 'complete',
                'description': '表示此状态下的任何请求已正常完成的状态',
            },
            {
                'name': '取消',
                'state_type': 'cancelled',
                'description': '表示此状态下的任何请求已被取消的状态(例如，工作已开始但尚未完成)',
            },
            {
                'name': '正常',
                'state_type': 'normal',
                'description': '没有特殊名称的常规状态',
            },
        ]

        for state_data in state_datas:
            state_data['process'] = self.process_id
            state_uid = self.mstate.create(state_data)
            self.state_dic[state_data['state_type']] = state_uid

        # 创建动作TabAction

        action_datas = [
            {
                'action_type': 'deny',
                'role': 'can_verify',
                'name': '拒绝',
                'description': '操作人将请求应移至上一个状态',
            },
            {
                'action_type': 'cancel',
                'role': 'can_verify',
                'name': '撤消',
                'description': '操作人将请求应在此过程中移至“已取消”状态',
            },
            {
                'action_type': 'approve',
                'role': 'can_verify',
                'name': '通过',
                'description': '操作人将请求应移至下一个状态',
            },
            {
                'action_type': 'restart',
                'role': 'can_edit',
                'name': '提交审核',
                'description': '操作人将将请求移回到进程中的“开始”状态',
            },
        ]

        action_uids = []
        for act in action_datas:
            act_uid = self.maction.create(self.process_id, act)
            action_uids.append(act_uid)
            print("*" * 50)
            print(act['role'])
            if act_uid:
                self.mper_action.create(act['role'], act_uid)

        assert action_uids

    def init_transition(self):
        '''
        转换Tabtransition
        '''

        deny = 'deny_' + self.process_id
        cancel = 'cancel_' + self.process_id
        restart = 'restart_' + self.process_id
        approve = 'approve_' + self.process_id

        act_deny = self.maction.get_by_action_type(deny).uid
        act_cancel = self.maction.get_by_action_type(cancel).uid

        act_restart = self.maction.get_by_action_type(restart).uid
        act_approve = self.maction.get_by_action_type(approve).uid

        trans = [
            # 状态：“正常”对应的“开始”
            {
                'current_state': self.state_dic['normal'],
                'next_state': self.state_dic['start'],
                'act_id': act_restart,
            },
            # 状态：“开始”对应的“拒绝”，“完成”
            {
                'current_state': self.state_dic['start'],
                'next_state': self.state_dic['denied'],
                'act_id': act_deny,
            },
            {
                'current_state': self.state_dic['start'],
                'next_state': self.state_dic['complete'],
                'act_id': act_approve,
            },
            # 状态：“取消”对应的“拒绝”，“完成”
            {
                'current_state': self.state_dic['cancelled'],
                'next_state': self.state_dic['denied'],
                'act_id': act_deny,
            },
            {
                'current_state': self.state_dic['cancelled'],
                'next_state': self.state_dic['complete'],
                'act_id': act_approve,
            },
            # 状态：“拒绝”对应的“取消”
            {
                'current_state': self.state_dic['denied'],
                'next_state': self.state_dic['cancelled'],
                'act_id': act_cancel,
            },
        ]

        for tran in trans:
            tran_id = MTransition.create(
                self.process_id, tran['current_state'], tran['next_state']
            )

            # 创建转换动作
            self.mtransaction.create(tran_id, tran['act_id'])

    def test_trans_query_all(self):
        pp = self.mtrans.query_all()

        TF = False

        if pp.count() > 0:
            TF = True

        assert TF

    def test_query_by_proid(self):
        pp = self.mtrans.query_by_proid(self.process_id)
        TF = False

        if pp.count() == 6:
            TF = True

        assert TF

    def test_query_by_proid_state(self):
        state_id = self.mstate.get_by_pro_statename(self.process_id, '拒绝')
        pp = self.mtrans.query_by_proid_state(self.process_id, state_id)
        TF = False
        if pp.count() == 1:
            TF = True

        assert TF

    def test_get_by_state_type(self):
        cur_state = self.mstate.get_by_pro_statename(self.process_id, '开始')
        next_state = self.mstate.get_by_pro_statename(self.process_id, '拒绝')
        pp = self.mtrans.get_by_cur_next(self.process_id, cur_state, next_state)
        TF = False

        if pp.count() == 1:
            TF = True

        assert TF

    def test_get_by_state_type2(self):
        cur_state = self.mstate.get_by_pro_statename(self.process_id, '取消')
        next_state = self.mstate.get_by_pro_statename(self.process_id, '开始')
        pp = self.mtrans.get_by_cur_next(self.process_id, cur_state, next_state)
        TF = False

        if pp.count() == 0:
            TF = True

        assert TF

    def test_query_by_action(self):
        act_id = self.maction.get_by_action_type('restart_' + self.process_id)
        pp = self.mtrans.query_by_action(act_id, self.process_id)
        TF = False

        if pp.count() == 1:
            TF = True

        assert TF

    def test_tranaction_query_all(self):
        trans_arr = []
        trans_recs = self.mtrans.query_by_proid(self.process_id)
        for tran in trans_recs:
            trans_arr.append(tran.transition)
        pp = self.mtransaction.query_all()
        TF = False
        for i in pp:
            if i.uid in trans_arr:
                TF = True

        assert TF

    def teardown_method(self):
        print("function teardown")

        process_id = self.process_id

        trans = self.mtrans.query_by_proid(process_id)

        for tran in trans:
            self.mtransaction.delete_by_trans(tran.uid)
            self.mtrans.delete(tran.uid)

        act_recs = MAction.query_by_proid(self.process_id)

        for act in act_recs:
            self.mper_action.delete_by_action(act.uid)
            self.maction.delete(act.uid)

        state_recs = self.mstate.query_by_pro_id(process_id)

        for state in state_recs:
            self.mstate.delete(state.uid)

        self.mprocess.delete_by_uid(process_id)
