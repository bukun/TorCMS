# -*- coding:utf-8 -*-
from torcms.core import tools
from torcms.model.process_model import MProcess, MAction, MPermissionAction
from torcms.model.permission_model import MPermission

from faker import Faker


class TestMAction():
    def setup_method(self):

        print('setup 方法执行于本类中每条用例之前')

        self.uid = tools.get_uu4d()

        self.mprocess = MProcess()
        self.maction = MAction()
        self.mper_action = MPermissionAction()
        self.mpermission = MPermission()
        self.fake = Faker(locale="zh_CN")
        self.process_id = self.init_process()
        self.init_action()

    def teardown_method(self):
        print("function teardown")

        act_recs = MAction.query_by_proid(self.process_id)

        for act in act_recs:
            self.mper_action.delete_by_action(act.uid)
            self.maction.delete(act.uid)

        self.mprocess.delete_by_uid(self.process_id)
    def init_process(self):
        '''
        创建流程TabProcess
        '''

        process_name = 'test数据审核' + self.uid
        process_id = self.mprocess.create(process_name)
        return process_id

    def init_action(self):
        '''
        创建动作TabAction
        '''

        action_datas = [
            {'action_type': 'deny', 'role': 'can_verify',
             'name': '拒绝', 'description': '操作人将请求应移至上一个状态'},
            {'action_type': 'cancel', 'role': 'can_verify',
             'name': '撤消', 'description': '操作人将请求应在此过程中移至“已取消”状态'},

            {'action_type': 'approve', 'role': 'can_verify',
             'name': '通过', 'description': '操作人将请求应移至下一个状态'},
            {'action_type': 'restart', 'role': 'can_edit',
             'name': '提交审核', 'description': '操作人将将请求移回到进程中的“开始”状态'},

        ]

        action_uids = []
        for act in action_datas:
            act_uid = MAction.create(self.process_id, act)
            action_uids.append(act_uid)

            if act_uid:
                # 动作与权限关联
                self.mper_action.create(act['role'], act_uid)
        recs = self.maction.query_by_proid(self.process_id)
        for rec in recs:
            assert rec.uid in action_uids

    def text_update_action(self):

        post_data1 = {
            'process': 'adf',
            'name': 'asdf',
            'action_type': 'asdf',
            'description': 'afd'
        }
        recs = self.maction.query_by_proid(self.process_id)
        for rec in recs:
            uu = self.maction.update(rec.uid, post_data1)
            assert uu == False

        post_data2 = {
            'process': self.process_id,
            'name': 'asdf',
            'action_type': 'asdf',
            'description': 'afd'
        }
        recs = self.maction.query_by_proid(self.process_id)
        for rec in recs:
            uu = self.maction.update(rec.uid, post_data2)
            assert uu == False

        post_data3 = {
            'process': self.process_id,
            'name': '',
            'action_type': '',
            'description': 'afd'
        }
        recs = self.maction.query_by_proid(self.process_id)
        for rec in recs:
            uu = self.maction.update(rec.uid, post_data3)
            assert uu == True

        post_data4 = {
            'process': self.process_id,
            'name': '',
            'action_type': 'adf',
            'description': ''
        }
        recs = self.maction.query_by_proid(self.process_id)
        for rec in recs:
            uu = self.maction.update(rec.uid, post_data4)
            assert uu == False

        post_data5 = {
            'process': self.process_id,
            'name': '',
            'action_type': 'adf' + self.uid,
            'description': ''
        }
        recs = self.maction.query_by_proid(self.process_id)
        for rec in recs:
            uu = self.maction.update(rec.uid, post_data5)
            assert uu == True



    def test_query_all(self):


        pp = self.maction.query_all()
        TF = False
        for i in pp:

            if i.name in ['拒绝', '撤消', '通过', '提交审核']:
                TF = True

        assert TF

    def test_query_by_proid(self):


        pp = self.maction.query_by_proid(self.process_id)
        TF = False

        if pp.count() == 4:
            TF = True

        assert TF

    def test_get_by_name(self):


        pp = self.maction.get_by_name('撤消').get()
        TF = False
        if pp.action_type.startswith('cancel'):
            TF = True

        assert TF

    def test_get_by_action_type(self):

        act_type = 'deny_' + self.process_id
        pp = self.maction.get_by_action_type(act_type).get()
        TF = False

        if pp.name == '拒绝':
            TF = True

        assert TF

    def test_get_by_pro_actname(self):

        pp = self.maction.get_by_pro_actname(self.process_id, '通过').get()
        TF = False

        if pp.action_type == 'approve_' + self.process_id:
            TF = True

        assert TF

    def test_query_per_by_action(self):

        act_id = self.maction.get_by_action_type('deny' + self.process_id)
        rec_name = self.mper_action.query_per_by_action(act_id)
        per_rec = self.mpermission.get_by_uid('can_verify')
        assert rec_name == per_rec.name

        recs = self.mper_action.query_by_permission('can_verify')
        assert recs == ['拒绝', '撤消', '通过']

        self.mper_action.remove_relation(act_id, per_rec.uid)
        recs = self.mper_action.query_by_permission('can_verify')
        assert recs == ['撤消', '通过']



        
