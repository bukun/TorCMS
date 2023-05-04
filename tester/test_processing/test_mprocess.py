# -*- coding:utf-8 -*-
import time

import tornado.escape

from torcms.core import tools
from torcms.model.category_model import MCategory
from torcms.model.label_model import MLabel, MPost2Label
from torcms.model.post2catalog_model import MPost2Catalog
from torcms.model.post_model import MPost
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
        self.insert()
        self.mprocess = MProcess()
        self.mstate = MState()
        self.mtrans = MTransition()
        self.mrequest = MRequest()
        self.maction = MAction()
        self.mreqaction = MRequestAction()
        self.mtransaction = MTransitionAction()

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

    def insert(self):

        post_data = {
            'title': self.post_title,
            'cnt_md': '## adslkfjasdf\n lasdfkjsadf',
            'user_name': 'Tome',
            'view_count': 1,
            'logo': '/static/',
            'keywords': 'sdf',
            'def_cat_uid': '9101',
            'gcat0': '9101',
            'def_cat_pid': '9100'
        }
        self.mpost.add_or_update(self.uid, post_data)

    def test_insert_2(self):
        '''创建流程，根据post_id: self.uid'''
        process_id = self.mprocess.create(self.uid)
        if process_id:
            # 创建状态
            self.test_create_state(process_id, self.uid)
            # 创建动作
            self.test_create_action(process_id, self.uid)
            # 创建转换
            # self.test_create_trans(process_id, self.uid)
            # 创建转换动作
            # self.test_create_transaction()
        # self.tearDown(process_id)
        # print(process_id)
        # assert process_id

    def test_create_state(self, process_id='', post_id=''):
        '''
        创建状态TabState
        '''
        state_datas = [
            {'process': process_id, 'name': '编辑_开始审核_{0}'.format(post_id),
             'state_type': 'editor_start_{0}'.format(post_id), 'description': '编辑_开始审核'.format(post_id)},
            {'process': process_id, 'name': '编辑_取消审核_{0}'.format(post_id),
             'state_type': 'editor_cancelled_{0}'.format(post_id), 'description': '编辑_取消审核_{0}'.format(post_id)},

            {'process': process_id, 'name': '管理_拒绝_{0}'.format(post_id),
             'state_type': 'admin_denied_{0}'.format(post_id),
             'description': '表示此状态下的任何请求已被拒绝的状态(例如，从未开始且不会被处理)_{0}'.format(post_id)},
            {'process': process_id, 'name': '管理_完成_{0}'.format(post_id),
             'state_type': 'admin_complete_{0}'.format(post_id),
             'description': '表示此状态下的任何请求已正常完成的状态_{0}'.format(post_id)},
            {'process': process_id, 'name': '管理_取消_{0}'.format(post_id),
             'state_type': 'admin_cancelled_{0}'.format(post_id),
             'description': '表示此状态下的任何请求已被取消的状态(例如，工作已开始但尚未完成)_{0}'.format(post_id)},
            {'process': process_id, 'name': '管理_正常_{0}'.format(post_id),
             'state_type': 'admin_normal_{0}'.format(post_id),
             'description': '没有特殊名称的常规状态_{0}'.format(post_id)},
            {'process': process_id, 'name': '管理_开始_{0}'.format(post_id),
             'state_type': 'admin_start_{0}'.format(post_id),
             'description': '每个进程只应该一个。此状态是创建新请求时所处的状态_{0}'.format(post_id)},

        ]

        state_uids = []
        for state_data in state_datas:
            state_uid = MState.create(state_data)
            state_uids.append(state_uid)
        assert state_uids

    def test_create_action(self, process_id='', post_id=''):
        '''
        创建动作TabAction
        '''

        action_datas = [
            {'process': process_id, 'action_type': 'deny_{0}'.format(post_id),
             'name': '管理拒绝_{0}'.format(post_id), 'description': '操作人将请求应移至上一个状态_{0}'.format(post_id)},
            {'process': process_id, 'action_type': 'cancel_{0}'.format(post_id),
             'name': '管理取消_{0}'.format(post_id),
             'description': '操作人将请求应在此过程中移至“已取消”状态_{0}'.format(post_id)},
            {'process': process_id, 'action_type': 'resolve_{0}'.format(post_id),
             'name': '管理完成_{0}'.format(post_id),
             'description': '操作人将将请求一直移动到Completed状态_{0}'.format(post_id)},
            {'process': process_id, 'action_type': 'approve_{0}'.format(post_id),
             'name': '管理通过_{0}'.format(post_id), 'description': '操作人将请求应移至下一个状态_{0}'.format(post_id)},
            {'process': process_id, 'action_type': 'restart_{0}'.format(post_id),
             'name': '提交审核_{0}'.format(post_id),
             'description': '操作人将将请求移回到进程中的“开始”状态_{0}'.format(post_id)},
            {'process': process_id, 'action_type': '编辑取消_{0}'.format(post_id),
             'name': '编辑取消_{0}'.format(post_id), 'description': '编辑取消_{0}'.format(post_id)}

        ]

        action_uids = []
        for act in action_datas:
            act_uid = MAction.create(process_id, act)
            action_uids.append(act_uid)
        assert action_uids

    # def test_create_trans(self, process_id='', post_id=''):
    #     '''
    #      转换Tabtransition
    #     '''
    #
    #     Tabtransition = [
    #         {'uid': '7bb3e41c-df29-11ed-b87f-898a446d722a', 'process': process_id,
    #          'current_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a',
    #          'next_state': 'de8c9f00-df26-11ed-b87f-898a446d722a'},
    #         {'uid': '80f868da-df29-11ed-b87f-898a446d722a', 'process': process_id,
    #          'current_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a',
    #          'next_state': '535ade26-df24-11ed-b87f-898a446d722a'},
    #         {'uid': '8563c63a-df29-11ed-b87f-898a446d722a', 'process': process_id,
    #          'current_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a',
    #          'next_state': 'bcf0b7be-df26-11ed-b87f-898a446d722a'},
    #         {'uid': '8a900678-df29-11ed-b87f-898a446d722a', 'process': process_id,
    #          'current_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a',
    #          'next_state': 'c1e51ada-df26-11ed-b87f-898a446d722a'},
    #         {'uid': 'eb453d56-df44-11ed-b87f-898a446d722a', 'process': process_id,
    #          'current_state': '2fa8c1dc-df24-11ed-b87f-898a446d722a',
    #          'next_state': '35b69234-df24-11ed-b87f-898a446d722a'},
    #         {'uid': 'd6f3e3ba-df4f-11ed-b87f-898a446d722a', 'process': process_id,
    #          'current_state': '2fa8c1dc-df24-11ed-b87f-898a446d722a',
    #          'next_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a'},
    #         {'uid': 'e3e3d3ac-e597-11ed-97ca-1f2eef5a84c4', 'process': process_id,
    #          'current_state': 'c1e51ada-df26-11ed-b87f-898a446d722a',
    #          'next_state': '2fa8c1dc-df24-11ed-b87f-898a446d722a'},
    #         {'uid': 'ec1fd688-e597-11ed-97ca-1f2eef5a84c4', 'process': process_id,
    #          'current_state': '535ade26-df24-11ed-b87f-898a446d722a',
    #          'next_state': '2fa8c1dc-df24-11ed-b87f-898a446d722a'}
    #
    #     ]
    #
    #     for tran in Tabtransition:
    #         TabTransition.create(
    #             uid=tran['uid'],
    #             process=tran['process'],
    #             current_state=tran['current_state'],
    #             next_state=tran['next_state']
    #         )
    #     assert True
    #
    # def test_create_transaction(self):
    #     '''
    #    转换动作TransitionAction
    #     '''
    #
    #     TransitionAction = [
    #         {'uid': 'f4d03b71-df29-11ed-b87f-898a446d722a', 'transition': '7bb3e41c-df29-11ed-b87f-898a446d722a',
    #          'action': 'f4d03b70-df29-11ed-b87f-898a446d722a'},
    #         {'uid': '0113c551-df2a-11ed-b87f-898a446d722a', 'transition': '80f868da-df29-11ed-b87f-898a446d722a',
    #          'action': '0113c550-df2a-11ed-b87f-898a446d722a'},
    #         {'uid': '08dca39d-df2a-11ed-b87f-898a446d722a', 'transition': '8a900678-df29-11ed-b87f-898a446d722a',
    #          'action': '08dca39c-df2a-11ed-b87f-898a446d722a'},
    #         {'uid': '3034c8c1-df2a-11ed-b87f-898a446d722a', 'transition': '8563c63a-df29-11ed-b87f-898a446d722a',
    #          'action': '3034c8c0-df2a-11ed-b87f-898a446d722a'},
    #         {'uid': '265a4643-df50-11ed-b87f-898a446d722a', 'transition': 'd6f3e3ba-df4f-11ed-b87f-898a446d722a',
    #          'action': '265a4642-df50-11ed-b87f-898a446d722a'},
    #         {'uid': '0b4bdcc1-ea19-11ed-af58-07be5fc7ff5d', 'transition': 'eb453d56-df44-11ed-b87f-898a446d722a',
    #          'action': '0b4bdcc0-ea19-11ed-af58-07be5fc7ff5d'}
    #
    #     ]
    #
    #     for tran_action in TransitionAction:
    #         TabTransitionAction.create(
    #             uid=tran_action['uid'],
    #             transition=tran_action['transition'],
    #             action=tran_action['action']
    #         )
    #     assert True
