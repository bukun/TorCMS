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

        self.fake = Faker(locale="zh_CN")

    def init_process(self):
        '''
        创建流程TabProcess
        '''

        process_name = 'test数据审核' + self.uid
        process_id = self.mprocess.create(process_name)
        return process_id

    def test_creat_data(self):
        '''
        初始化流程TabProcess，状态，动作
        '''

        # 创建状态TabState
        if self.process_id:
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
            ]

            for state_data in state_datas:
                state_data['process'] = self.process_id
                state_uid = self.mstate.create(state_data)
                self.state_dic[state_data['state_type']] = state_uid

            # 创建动作TabAction
            action_datas = (
                {
                    'action_type': 'deny',
                    'role': 'can_verify',
                    'name': '拒绝',
                    'description': '操作人将请求应移至上一个状态',
                },
            )

            act_uid = self.maction.create(self.process_id, action_datas)

            if act_uid:
                self.mper_action.create(action_datas['role'], act_uid)

                # 状态：“开始”对应的“拒绝”
                tran = {
                    'current_state': self.state_dic['start'],
                    'next_state': self.state_dic['denied'],
                    'act_id': act_uid,
                }

                tran_id = self.mtrans.create(
                    self.process_id, tran['current_state'], tran['next_state']
                )

                # 创建转换动作
                pp = self.mtransaction.create(tran_id, tran['act_id'])
                assert pp

                pp = self.mtransaction.create(tran_id, 'sdfs')
                assert pp == False

                rec = self.mtransaction.get_by_trans(tran_id)

                assert rec.action == tran['act_id']

                recs = self.mtransaction.query_by_pro_state(
                    self.process_id, self.state_dic['start']
                )
                assert recs['transition'] == tran_id
                assert recs['action'] == tran['act_id']

                recs = self.mtransaction.query_by_process(self.process_id)
                pp = False
                for rec in recs:
                    if rec.name == '拒绝':
                        pp = True
                assert pp

    def teardown_method(self):
        print("function teardown")

        trans = self.mtrans.query_by_proid(self.process_id)

        for tran in trans:
            self.mtransaction.delete_by_trans(tran.uid)
            self.mtrans.delete(tran.uid)

        act_recs = MAction.query_by_proid(self.process_id)

        for act in act_recs:
            self.mper_action.delete_by_action(act.uid)
            self.maction.delete(act.uid)

        state_recs = self.mstate.query_by_pro_id(self.process_id)

        for state in state_recs:
            self.mstate.delete(state.uid)

        self.mprocess.delete_by_uid(self.process_id)
