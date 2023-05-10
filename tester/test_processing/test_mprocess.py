# -*- coding:utf-8 -*-
import time

import tornado.escape

from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.label_model import MLabel, MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.user_model import MUser
from torcms.handlers.post_handler import update_label, update_category
from torcms.model.process_model import MProcess, MState, MTransition, MRequest, MAction, MRequestAction, \
    MTransitionAction, TabProcess, TabAction, TabTransition, TabRequest, TabState, TabTransitionAction, TabRole, \
    TabRequestAction

from faker import Faker


class TestMProcess():
    def setup_method(self):

        print('setup 方法执行于本类中每条用例之前')
        self.mpost = MPost()
        self.m2c = MPost2Catalog()
        self.ml = MLabel()
        self.m2l = MPost2Label()
        self.labeluid = '9999'
        self.raw_count = self.mpost.get_counts()
        self.post_title = 'ccc'
        self.uid = tools.get_uu4d()
        self.post_id = '66565'
        self.tag_id = '2342'
        self.post_id2 = '89898'
        self.slug = 'huio'
        self.test_insert()
        self.mprocess = MProcess()
        self.mstate = MState()
        self.mtrans = MTransition()
        self.mrequest = MRequest()
        self.maction = MAction()
        self.mreqaction = MRequestAction()
        self.mtransaction = MTransitionAction()
        self.state_arr = {}
        self.user_id = MUser.get_by_name('admin').uid
        self.fake = Faker(locale="zh_CN")

    def tearDown(self, process_id=''):
        print("function teardown")

        self.mpost.delete(self.uid)
        MCategory.delete(self.tag_id)
        self.mpost.delete(self.post_id2)
        self.mpost.delete(self.post_id)

        if process_id:
            self.mprocess.delete_by_uid(process_id)

        MPost2Catalog.remove_relation(self.post_id, self.tag_id)
        tt = MLabel.get_by_slug(self.slug)
        if tt:
            MLabel.delete(tt.uid)

    def test_insert(self):

        post_data = {
            'title': self.post_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '',
            'keywords': 'sdf',
            'def_cat_uid': '9101',
            'gcat0': '9101',
            'def_cat_pid': '9100',
            'valid': 1,
            'kind': '9'
        }

        self.mpost.add_or_update(self.uid, post_data)
        update_category(self.uid, post_data)

    def test_insert_2(self, state_id='', post_id=''):
        '''创建流程，根据post_id: self.uid'''
        if post_id:
            post_id = post_id
        else:
            post_id = self.uid
        pro_name = post_id + state_id
        process_id = self.mprocess.create(pro_name)
        if process_id:
            # 创建动作
            self.test_create_action(process_id, self.uid)

            # 创建状态
            self.test_create_state(process_id, self.uid)

            # 创建状态转换
            self.test_create_trans(process_id, self.state_arr, self.uid)
            print(self.user_id)

            # 创建请求
            self.test_create_request(process_id, self.uid)

        # self.tearDown(process_id)
        # print(process_id)
        # assert process_id

    def test_create_state(self, process_id='', post_id=''):
        '''
        创建状态TabState
        '''

        state_datas = [
            {'process': process_id, 'name': '开始_{0}'.format(post_id),
             'state_type': 'start_{0}'.format(post_id),
             'description': '每个进程只应该一个。此状态是创建新请求时所处的状态_{0}'.format(post_id)},
            {'process': process_id, 'name': '拒绝_{0}'.format(post_id),
             'state_type': 'denied_{0}'.format(post_id),
             'description': '表示此状态下的任何请求已被拒绝的状态(例如，从未开始且不会被处理)_{0}'.format(post_id)},
            {'process': process_id, 'name': '完成_{0}'.format(post_id),
             'state_type': 'complete_{0}'.format(post_id),
             'description': '表示此状态下的任何请求已正常完成的状态_{0}'.format(post_id)},
            {'process': process_id, 'name': '取消_{0}'.format(post_id),
             'state_type': 'cancelled_{0}'.format(post_id),
             'description': '表示此状态下的任何请求已被取消的状态(例如，工作已开始但尚未完成)_{0}'.format(post_id)},
            {'process': process_id, 'name': '正常_{0}'.format(post_id),
             'state_type': 'normal_{0}'.format(post_id),
             'description': '没有特殊名称的常规状态_{0}'.format(post_id)},

        ]

        for state_data in state_datas:
            state_uid = MState.create(state_data)
            self.state_arr[state_data['state_type']] = state_uid

        assert self.state_arr

    def test_create_action(self, process_id='', post_id=''):
        '''
        创建动作TabAction
        '''

        action_datas = [
            {'action_type': 'deny_{0}'.format(post_id),
             'name': '拒绝_{0}'.format(post_id), 'description': '操作人将请求应移至上一个状态_{0}'.format(post_id)},
            {'action_type': 'cancel_{0}'.format(post_id),
             'name': '取消_{0}'.format(post_id),
             'description': '操作人将请求应在此过程中移至“已取消”状态_{0}'.format(post_id)},
            {'action_type': 'resolve_{0}'.format(post_id),
             'name': '完成_{0}'.format(post_id),
             'description': '操作人将将请求一直移动到Completed状态_{0}'.format(post_id)},
            {'action_type': 'approve_{0}'.format(post_id),
             'name': '通过_{0}'.format(post_id), 'description': '操作人将请求应移至下一个状态_{0}'.format(post_id)},
            {'action_type': 'restart_{0}'.format(post_id),
             'name': '提交审核_{0}'.format(post_id),
             'description': '操作人将将请求移回到进程中的“开始”状态_{0}'.format(post_id)},

        ]

        action_uids = []
        for act in action_datas:
            act_uid = MAction.create(process_id, act)
            action_uids.append(act_uid)
        assert action_uids

    def test_create_trans(self, process_id='', state_arr={}, post_id=''):
        '''
         转换Tabtransition
        '''
        if post_id:
            deny = 'deny_' + post_id
            cancel = 'cancel_' + post_id
            resolve = 'resolve_' + post_id
            restart = 'restart_' + post_id
            approve = 'approve_' + post_id

            act_deny = MAction.get_by_action_type(deny).uid
            act_cancel = MAction.get_by_action_type(cancel).uid
            act_resolve = MAction.get_by_action_type(resolve).uid
            act_restart = MAction.get_by_action_type(restart).uid
            act_approve = MAction.get_by_action_type(approve).uid

            trans = [
                # 状态：“正常”对应的“开始”
                {'current_state': state_arr['normal_{}'.format(post_id)],
                 'next_state': state_arr['start_{}'.format(post_id)], 'act_id': act_restart},

                # 状态：“开始”对应的“拒绝”，“完成”，“取消”
                {'current_state': state_arr['start_{}'.format(post_id)],
                 'next_state': state_arr['denied_{}'.format(post_id)], 'act_id': act_deny},
                {'current_state': state_arr['start_{}'.format(post_id)],
                 'next_state': state_arr['complete_{}'.format(post_id)], 'act_id': act_approve},
                {'current_state': state_arr['start_{}'.format(post_id)],
                 'next_state': state_arr['cancelled_{}'.format(post_id)], 'act_id': act_cancel},


                # 状态：“取消”对应的“拒绝”，“完成”
                {'current_state': state_arr['cancelled_{}'.format(post_id)],
                 'next_state': state_arr['denied_{}'.format(post_id)], 'act_id': act_deny},
                {'current_state': state_arr['cancelled_{}'.format(post_id)],
                 'next_state': state_arr['complete_{}'.format(post_id)], 'act_id': act_approve},

                # 状态：“拒绝”对应的“正常”
                {'current_state': state_arr['denied_{}'.format(post_id)],
                 'next_state': state_arr['normal_{}'.format(post_id)], 'act_id': act_restart},

            ]

            for tran in trans:
                tran_id = MTransition.create(process_id, tran['current_state'], tran['next_state'])

                # 创建转换动作
                self.test_create_transaction(tran_id, tran['act_id'])

            # assert True

    def test_create_transaction(self, trans_id='', actid=''):
        '''
       转换动作TransitionAction
        '''

        trans_act = MTransitionAction.create(trans_id, actid)
        # assert trans_act

    def test_create_request(self, process_id='', post_id=''):
        '''
        创建请求以及请求对应状态的相关动作
        '''

        # 获取“开始”状态ID
        if post_id:
            state_type = 'start_{0}'.format(post_id)
            cur_state = MState.get_by_state_type(state_type)
            if cur_state:
                # 创建请求
                req_id = MRequest.create(process_id, self.uid, self.user_id, cur_state.uid)
                # trans_id=MTransition.query_by_state(cur_state.name)

                # 创建请求操作
                cur_actions = MTransitionAction.query_by_pro_state(process_id, cur_state.uid)
                for cur_act in cur_actions:
                    MRequestAction.create(req_id, cur_act['action'], cur_act['transition'])

                # 进行请求操作
                self.test_request_action(process_id, cur_state.uid)

    def test_request_action(self, process_id='', cur_state_id=''):
        '''
        进行请求操作
        '''

        request_id = MRequest.get_by_pro_state(process_id, cur_state_id)
        post_id = self.uid
        user_id = self.user_id
        act_type = 'approve_{0}'.format(post_id)
        cur_act = MAction.get_by_action_type(act_type)
        print("1" * 50)
        print(request_id)
        if cur_act:
            print("2" * 50)
            print(cur_act.uid)
            print(request_id)
            # 提交的Action与其中一个（is_active = true）的活动RequestActions匹配，设置 is_active = false 和 is_completed = true
            reqact = MRequestAction.get_by_action_request(cur_act.uid, request_id)
            print("3" * 50)
            if reqact:
                if reqact.is_active:
                    # 更新操作动态
                    print("gengxin")
                    MRequestAction.update_by_action(cur_act.uid, request_id)
                # 查询该请求中该转换的所有动作是否都为True
                istrues = MRequestAction.query_by_request_trans(request_id, reqact.transition).get()
                print(istrues)
                if istrues.is_complete:
                    # 禁用该请求下其它动作
                    MRequestAction.update_by_action_reqs(cur_act.uid, request_id)
                    # 转到下一状态
                    trans = MTransition.get_by_uid(reqact.transition).get()
                    new_state = MState.get_by_uid(trans.next_state).get()
                    if new_state.state_type.startswith('normal_'):
                        print("完成" * 5)
                        MPost.update_valid(post_id)

                    else:
                        act_arr = []
                        acts = MTransitionAction.query_by_pro_state(process_id, new_state.uid)
                        for act in acts:
                            act_arr.append({'trans': act['transition'], 'act': act['action']})
                        dics = {'new_state_id': new_state.uid, 'new_actarr': act_arr}
                        print("4" * 50)
                        print(dics)
                        self.test_insert_2(new_state.uid, post_id)

