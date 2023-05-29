# -*- coding:utf-8 -*-
import time

import tornado.escape

from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.label_model import MLabel, MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
from torcms.model.user_model import MUser
from torcms.model.role_model import MRole
from torcms.handlers.post_handler import update_label, update_category
from torcms.model.process_model import MProcess, MState, MTransition, MRequest, MAction, MRequestAction, \
    MTransitionAction, MPermissionAction

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
        self.user_id = MUser.get_by_name('admin').uid
        self.state_dic = {}
        self.process_id = ''
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
        self.init_process()

        self.fake = Faker(locale="zh_CN")

    def init_post(self):

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
            'valid': '0',
            'kind': '9'
        }

        self.mpost.add_or_update(self.uid, post_data)
        update_category(self.uid, post_data)

    def init_process(self):
        '''
        创建流程TabProcess
        '''
        # 创建Post
        self.init_post()
        process_name = 'test数据审核' + self.uid
        process_id = self.mprocess.create(process_name)
        if process_id:
            self.process_id = process_id
            # 创建动作
            self.init_action(process_id)

            # 创建状态
            self.init_state(process_id)

            # 创建状态转换
            self.init_trans(process_id, self.state_dic)

    def init_state(self, process_id=''):
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

    def init_action(self, process_id=''):
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

    def init_trans(self, process_id='', state_dic={}):
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

    def test_create_request(self):
        '''
        创建请求以及请求对应状态的相关动作
        '''

        # 获取“开始”状态ID
        if self.process_id:
            state_type = 'start_' + self.process_id
            cur_state = MState.get_by_state_type(state_type)
            if cur_state:
                print("/" * 50)
                print(cur_state)
                # 创建请求
                req_id = MRequest.create(self.process_id, self.uid, self.user_id, cur_state.uid)
                # trans_id=MTransition.query_by_state(cur_state.name)
                print(req_id)
                # 创建请求操作
                cur_actions = MTransitionAction.query_by_pro_state(self.process_id, cur_state.uid)
                for cur_act in cur_actions:
                    MRequestAction.create(req_id, cur_act['action'], cur_act['transition'])

                    # 进行请求操作
                    self.test_request_action(req_id, self.process_id, self.uid, cur_act['action'])

            req_rec = self.mrequest.get_by_pro(self.process_id).get()
            assert req_rec.post_id == self.uid

            req_rec2 = self.mrequest.get_by_pro_state(self.process_id, cur_state.uid)
            assert req_rec2.user_id == self.user_id
            req_rec3 = self.mrequest.query_by_postid(self.uid)
            assert req_rec3.process_id == self.process_id
            # self.tearDown(self.process_id)

    def test_request_action(self, request_id='', process_id='', post_id='', act_id=''):
        '''
        进行请求操作
        '''

        act_arr = []
        if request_id:
            print("1-" * 50)
            print(act_id)
            print(request_id)

            # 提交的Action与其中一个（is_active = true）的活动RequestActions匹配，设置 is_active = false 和 is_completed = true
            reqact = MRequestAction.get_by_action_request(act_id, request_id)

            if reqact.is_active:
                # 更新操作动态
                print("gengxin")
                MRequestAction.update_by_action(act_id, request_id)

                # 查询该请求中该转换的所有动作是否都为True
                istrues = MRequestAction.query_by_request_trans(request_id, reqact.transition)

                if istrues:
                    if istrues.is_complete:
                        print("1.2 " * 50)
                        # 禁用该请求下其它动作
                        MRequestAction.update_by_action_reqs(act_id, request_id)
                        # 转到下一状态
                        trans = MTransition.get_by_uid(reqact.transition).get()
                        new_state = MState.get_by_uid(trans.next_state).get()

                        print(trans.current_state)
                        print(trans.next_state)

                        if new_state.state_type.startswith('complete'):
                            print("1.3 " * 50)
                            MPost.update_valid(post_id)
                            post_rec = MPost.get_by_uid(post_id)
                            assert post_rec.valid == 1

                        else:
                            print("1.4 " * 50)
                            print(new_state.name)
                            # 创建请求
                            new_request_id = MRequest.create(process_id, post_id, self.user_id, new_state.uid)

                            # 创建请求操作
                            cur_actions = MTransitionAction.query_by_pro_state(process_id, new_state.uid)

                            for cur_act in cur_actions:
                                MRequestAction.create(new_request_id, cur_act['action'], cur_act['transition'])
                                act = MAction.get_by_id(cur_act['action']).get()

                                act_arr.append({"act_name": act.name})

                            if new_state.name == '正常':
                                new_act_arr = [{"act_name": "提交审核"}]
                            elif new_state.name == '开始':
                                new_act_arr = [{"act_name": "拒绝"}, {"act_name": "通过"}, {"act_name": "取消"}]
                            elif new_state.name == '拒绝':
                                new_act_arr = [{"act_name": "提交审核"}]
                            elif new_state.name == '取消':
                                new_act_arr = [{"act_name": "拒绝"}, {"act_name": "通过"}]
                            else:
                                new_act_arr = []
                            print("~" * 50)
                            print(act_arr)
                            print(new_act_arr)
                            assert act_arr == new_act_arr
                            

    def tearDown(self, process_id=''):
        print("function teardown")
        trans = self.mtrans.query_by_proid(process_id)
        print(trans.count())
        for tran in trans:
            print("*" * 50)
            print(tran.uid)

            self.mreqaction.delete_by_trans(tran.uid)
            self.mtransaction.delete_by_trans(tran.uid)
            self.mtrans.delete(tran.uid)

        req_recs = self.mrequest.get_by_pro(process_id)
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

        self.mpost.delete(self.uid)

        MCategory.delete(self.tag_id)
        self.mpost.delete(self.post_id2)
        self.mpost.delete(self.post_id)

        MPost2Catalog.remove_relation(self.post_id, self.tag_id)
        tt = MLabel.get_by_slug(self.slug)
        if tt:
            MLabel.delete(tt.uid)

        pro_recs = self.mprocess.query_all()
        for pro in pro_recs:
            if pro.name.startswith('test数据审核'):
                trans = self.mtrans.query_by_proid(pro.uid)
                print(trans.count())
                for tran in trans:
                    print("*" * 50)
                    print(tran.uid)

                    self.mreqaction.delete_by_trans(tran.uid)
                    self.mtransaction.delete_by_trans(tran.uid)
                    self.mtrans.delete(tran.uid)

                req_recs = self.mrequest.get_by_pro(pro.uid)
                for req_rec in req_recs:
                    print(req_rec.uid)
                    self.mrequest.delete(req_rec.uid)

                act_recs = MAction.query_by_proid(pro.uid)
                for act in act_recs:
                    self.mper_action.delete_by_action(act.uid)
                    self.maction.delete(act.uid)

                states = self.mstate.query_by_pro_id(pro.uid)
                for state in states:
                    self.mstate.delete(state.uid)

                self.mprocess.delete_by_uid(pro.uid)

                self.mpost.delete(self.uid)

                MCategory.delete(self.tag_id)
                self.mpost.delete(self.post_id2)
                self.mpost.delete(self.post_id)

                MPost2Catalog.remove_relation(self.post_id, self.tag_id)
                tt = MLabel.get_by_slug(self.slug)
                if tt:
                    MLabel.delete(tt.uid)
