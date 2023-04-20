from torcms.model.process_model import *


def test():
    Tabstate = [
        {'uid': '2fa8c1dc-df24-11ed-b87f-898a446d722a', 'process': '1editor', 'name': '编辑_开始审核',
         'state_type': '编辑_开始审核', 'description': '编辑_开始审核'},
        {'uid': '35b69234-df24-11ed-b87f-898a446d722a', 'process': '1editor', 'name': '编辑_取消审核',
         'state_type': '编辑_取消审核', 'description': '编辑_取消审核'},

        {'uid': '535ade26-df24-11ed-b87f-898a446d722a', 'process': 'uadministrators', 'name': '管理_拒绝',
         'state_type': '管理_拒绝', 'description': '管理_拒绝'},
        {'uid': 'bcf0b7be-df26-11ed-b87f-898a446d722a', 'process': 'uadministrators', 'name': '管理_完成',
         'state_type': '管理_完成', 'description': '管理_完成'},
        {'uid': 'c1e51ada-df26-11ed-b87f-898a446d722a', 'process': 'uadministrators', 'name': '管理_取消',
         'state_type': '管理_取消', 'description': '管理_取消'},
        {'uid': 'de8c9f00-df26-11ed-b87f-898a446d722a', 'process': 'uadministrators', 'name': '管理_通过',
         'state_type': '管理_通过', 'description': '管理_通过'},
        {'uid': '3e2a0b6c-df24-11ed-b87f-898a446d722a', 'process': 'uadministrators', 'name': '管理_开始',
         'state_type': '管理_开始', 'description': '管理_开始'},


    ]

    action = [
        {'uid': '0113c550-df2a-11ed-b87f-898a446d722a', 'process': 'uadministrators', 'action_type': '拒绝',
         'name': '拒绝', 'description': '拒绝'},
        {'uid': '08dca39c-df2a-11ed-b87f-898a446d722a', 'process': 'uadministrators', 'action_type': '取消',
         'name': '取消', 'description': '取消'},
        {'uid': '3034c8c0-df2a-11ed-b87f-898a446d722a', 'process': 'uadministrators', 'action_type': '完成',
         'name': '完成', 'description': '完成'},
        {'uid': 'f4d03b70-df29-11ed-b87f-898a446d722a', 'process': 'uadministrators', 'action_type': '通过',
         'name': '通过', 'description': '通过'},
        {'uid': '265a4642-df50-11ed-b87f-898a446d722a', 'process': '1editor', 'action_type': '提交审核',
         'name': '提交审核', 'description': '提交审核'}

    ]

    Tabtransition = [
        {'uid': '7bb3e41c-df29-11ed-b87f-898a446d722a', 'process': 'uadministrators',
         'current_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a', 'next_state': 'de8c9f00-df26-11ed-b87f-898a446d722a'},
        {'uid': '80f868da-df29-11ed-b87f-898a446d722a', 'process': 'uadministrators',
         'current_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a', 'next_state': '535ade26-df24-11ed-b87f-898a446d722a'},
        {'uid': '8563c63a-df29-11ed-b87f-898a446d722a', 'process': 'uadministrators',
         'current_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a', 'next_state': 'bcf0b7be-df26-11ed-b87f-898a446d722a'},
        {'uid': '8a900678-df29-11ed-b87f-898a446d722a', 'process': 'uadministrators',
         'current_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a', 'next_state': 'c1e51ada-df26-11ed-b87f-898a446d722a'},
        {'uid': 'eb453d56-df44-11ed-b87f-898a446d722a', 'process': '1editor',
         'current_state': '2fa8c1dc-df24-11ed-b87f-898a446d722a', 'next_state': '35b69234-df24-11ed-b87f-898a446d722a'},
        {'uid': 'd6f3e3ba-df4f-11ed-b87f-898a446d722a', 'process': '1editor',
         'current_state': '2fa8c1dc-df24-11ed-b87f-898a446d722a', 'next_state': '3e2a0b6c-df24-11ed-b87f-898a446d722a'}

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
         'action': '265a4642-df50-11ed-b87f-898a446d722a'}

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


if __name__ == '__main__':
    test()
