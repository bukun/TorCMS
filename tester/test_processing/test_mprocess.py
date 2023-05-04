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

        }
        self.mpost.add_or_update(self.uid, post_data)

    def test_insert_2(self):
        '''创建流程，根据post_id: self.uid'''
        process_id = self.mprocess.create(self.uid)
        if process_id:
            self.test_create(process_id)
        




        # self.tearDown(process_id)
        # print(process_id)
        # assert process_id
    def test_create(self,process_id=''):
        '''
        创建状态TabState，动作TabAction，转换Tabtransition，转换动作TransitionAction
        '''
        Tabstate = [
            {'uid': '2fa8c1dc-df24-11ed-b87f-898a446d722a', 'process': process_id, 'name': '编辑_开始审核',
             'state_type': 'editor_start', 'description': '编辑_开始审核'},
            {'uid': '35b69234-df24-11ed-b87f-898a446d722a', 'process': process_id, 'name': '编辑_取消审核',
             'state_type': 'editor_cancelled', 'description': '编辑_取消审核'},

            {'uid': '535ade26-df24-11ed-b87f-898a446d722a', 'process': process_id, 'name': '管理_拒绝',
             'state_type': 'admin_denied',
             'description': '表示此状态下的任何请求已被拒绝的状态（例如，从未开始且不会被处理）'},
            {'uid': 'bcf0b7be-df26-11ed-b87f-898a446d722a', 'process': process_id, 'name': '管理_完成',
             'state_type': 'admin_complete', 'description': '表示此状态下的任何请求已正常完成的状态'},
            {'uid': 'c1e51ada-df26-11ed-b87f-898a446d722a', 'process': process_id, 'name': '管理_取消',
             'state_type': 'admin_cancelled',
             'description': '表示此状态下的任何请求已被取消的状态（例如，工作已开始但尚未完成）。'},
            {'uid': 'de8c9f00-df26-11ed-b87f-898a446d722a', 'process': process_id, 'name': '管理_正常',
             'state_type': 'admin_normal', 'description': '没有特殊名称的常规状态'},
            {'uid': '3e2a0b6c-df24-11ed-b87f-898a446d722a', 'process': process_id, 'name': '管理_开始',
             'state_type': 'admin_start', 'description': '每个进程只应该一个。此状态是创建新请求时所处的状态'},

        ]

        action = [
            {'uid': '0113c550-df2a-11ed-b87f-898a446d722a', 'process': process_id, 'action_type': 'deny',
             'name': '管理拒绝', 'description': '操作人将请求应移至上一个状态'},
            {'uid': '08dca39c-df2a-11ed-b87f-898a446d722a', 'process': process_id, 'action_type': 'cancel',
             'name': '管理取消', 'description': '操作人将请求应在此过程中移至“已取消”状态'},
            {'uid': '3034c8c0-df2a-11ed-b87f-898a446d722a', 'process': process_id, 'action_type': 'resolve',
             'name': '管理完成', 'description': '操作人将将请求一直移动到Completed状态'},
            {'uid': 'f4d03b70-df29-11ed-b87f-898a446d722a', 'process': process_id, 'action_type': 'approve',
             'name': '管理通过', 'description': '操作人将请求应移至下一个状态'},
            {'uid': '265a4642-df50-11ed-b87f-898a446d722a', 'process': process_id, 'action_type': 'restart',
             'name': '提交审核', 'description': '操作人将将请求移回到进程中的“开始”状态'},
            {'uid': '0b4bdcc0-ea19-11ed-af58-07be5fc7ff5d', 'process': process_id, 'action_type': '编辑取消',
             'name': '编辑取消', 'description': '编辑取消'}

        ]

        Tabtransition = [
            {'uid': '7bb3e41c-df29-11ed-b87f-898a446d722a', 'process': process_id,
             'current_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a',
             'next_state': 'de8c9f00-df26-11ed-b87f-898a446d722a'},
            {'uid': '80f868da-df29-11ed-b87f-898a446d722a', 'process': process_id,
             'current_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a',
             'next_state': '535ade26-df24-11ed-b87f-898a446d722a'},
            {'uid': '8563c63a-df29-11ed-b87f-898a446d722a', 'process': process_id,
             'current_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a',
             'next_state': 'bcf0b7be-df26-11ed-b87f-898a446d722a'},
            {'uid': '8a900678-df29-11ed-b87f-898a446d722a', 'process': process_id,
             'current_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a',
             'next_state': 'c1e51ada-df26-11ed-b87f-898a446d722a'},
            {'uid': 'eb453d56-df44-11ed-b87f-898a446d722a', 'process': process_id,
             'current_state': '2fa8c1dc-df24-11ed-b87f-898a446d722a',
             'next_state': '35b69234-df24-11ed-b87f-898a446d722a'},
            {'uid': 'd6f3e3ba-df4f-11ed-b87f-898a446d722a', 'process': process_id,
             'current_state': '2fa8c1dc-df24-11ed-b87f-898a446d722a',
             'next_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a'},
            {'uid': 'e3e3d3ac-e597-11ed-97ca-1f2eef5a84c4', 'process': process_id,
             'current_state': 'c1e51ada-df26-11ed-b87f-898a446d722a',
             'next_state': '2fa8c1dc-df24-11ed-b87f-898a446d722a'},
            {'uid': 'ec1fd688-e597-11ed-97ca-1f2eef5a84c4', 'process': process_id,
             'current_state': '535ade26-df24-11ed-b87f-898a446d722a',
             'next_state': '2fa8c1dc-df24-11ed-b87f-898a446d722a'}

        ]

        TransitionAction = [
            {'uid': 'f4d03b71-df29-11ed-b87f-898a446d722a', 'transition': '7bb3e41c-df29-11ed-b87f-898a446d722a',
             'action': 'f4d03b70-df29-11ed-b87f-898a446d722a'},
            {'uid': '0113c551-df2a-11ed-b87f-898a446d722a', 'transition': '80f868da-df29-11ed-b87f-898a446d722a',
             'action': '0113c550-df2a-11ed-b87f-898a446d722a'},
            {'uid': '08dca39d-df2a-11ed-b87f-898a446d722a', 'transition': '8a900678-df29-11ed-b87f-898a446d722a',
             'action': '08dca39c-df2a-11ed-b87f-898a446d722a'},
            {'uid': '3034c8c1-df2a-11ed-b87f-898a446d722a', 'transition': '8563c63a-df29-11ed-b87f-898a446d722a',
             'action': '3034c8c0-df2a-11ed-b87f-898a446d722a'},
            {'uid': '265a4643-df50-11ed-b87f-898a446d722a', 'transition': 'd6f3e3ba-df4f-11ed-b87f-898a446d722a',
             'action': '265a4642-df50-11ed-b87f-898a446d722a'},
            {'uid': '0b4bdcc1-ea19-11ed-af58-07be5fc7ff5d', 'transition': 'eb453d56-df44-11ed-b87f-898a446d722a',
             'action': '0b4bdcc0-ea19-11ed-af58-07be5fc7ff5d'}

        ]
        try:
            for state in Tabstate:
                TabState.create(
                    uid=state['uid'],
                    process=state['process'],
                    name=state['name'],
                    state_type=state['state_type'],
                    description=state['description']
                )
            pass
        except Exception as err:
            print(repr(err))
            pass

        try:
            for act in action:
                TabAction.create(
                    uid=act['uid'],
                    process=act['process'],
                    name=act['name'],
                    action_type=act['action_type'],
                    description=act['description']
                )
            pass
        except Exception as err:
            print(repr(err))
            pass

        try:
            for tran in Tabtransition:
                TabTransition.create(
                    uid=tran['uid'],
                    process=tran['process'],
                    current_state=tran['current_state'],
                    next_state=tran['next_state']
                )
            pass
        except Exception as err:
            print(repr(err))
            pass

        try:
            for tran_action in TransitionAction:
                TabTransitionAction.create(
                    uid=tran_action['uid'],
                    transition=tran_action['transition'],
                    action=tran_action['action']
                )
            pass
        except Exception as err:
            print(repr(err))
            return False

 
