from torcms.model.process_model import *


def test():
    Tabstate = [
        {'uid': 'cb072884-de4e-11ed-9d76-2544c8d60402', 'process': 'uadministrators', 'name': '管理_开始审核',
         'state_type': '管理_开始审核', 'description': '管理_开始审核'},
        {'uid': 'd3e39294-de4e-11ed-9d76-2544c8d60402', 'process': 'uadministrators', 'name': '管理_完成审核',
         'state_type': '管理_完成审核', 'description': '管理_完成审核'},
        {'uid': 'd957ac2e-de4e-11ed-9d76-2544c8d60402', 'process': 'uadministrators', 'name': '管理_拒绝审核',
         'state_type': '管理_拒绝审核', 'description': '管理_拒绝审核'},
        {'uid': 'fe7432e8-de4e-11ed-9d76-2544c8d60402', 'process': '1editor', 'name': '编辑_开始审核',
         'state_type': '编辑_开始审核', 'description': '编辑_开始审核'},
        {'uid': '06a263fe-de4f-11ed-9d76-2544c8d60402', 'process': '1editor', 'name': '编辑_完成审核',
         'state_type': '编辑_完成审核', 'description': '编辑_完成审核'},
        {'uid': '0f78610e-de4f-11ed-9d76-2544c8d60402', 'process': '1editor', 'name': '编辑_拒绝审核',
         'state_type': '编辑_拒绝审核', 'description': '编辑_拒绝审核'},
        {'uid': '8e935de0-de4f-11ed-9d76-2544c8d60402', 'process': '1editor', 'name': '编辑_取消审核',
         'state_type': '编辑_取消审核', 'description': '编辑_取消审核'},
        {'uid': '8e935de1-de4f-11ed-9d76-2544c8d60402', 'process': 'uadministrators', 'name': '管理_取消审核',
         'state_type': '管理_取消审核', 'description': '管理_取消审核'}
    ]

    action = [
        {'uid': '3687c848-de4f-11ed-9d76-2544c8d60402', 'process': '1editor', 'action_type': '通过审核',
         'name': '通过审核', 'description': '通过审核'},
        {'uid': '3f38c5c8-de4f-11ed-9d76-2544c8d60402', 'process': '1editor', 'action_type': '拒绝审核',
         'name': '拒绝审核', 'description': '拒绝审核'},
        {'uid': '569bf320-de4f-11ed-9d76-2544c8d60402', 'process': 'uadministrators', 'action_type': '管理通过',
         'name': '管理通过', 'description': '管理通过'},
        {'uid': '6149df3a-de4f-11ed-9d76-2544c8d60402', 'process': 'uadministrators', 'action_type': '管理拒绝',
         'name': '管理拒绝', 'description': '管理拒绝'},
        {'uid': 'a89f4b72-de4f-11ed-9d76-2544c8d60402', 'process': '1editor', 'action_type': '取消审核',
         'name': '取消审核', 'description': '取消审核'},
        {'uid': 'b58449dc-de4f-11ed-9d76-2544c8d60402', 'process': 'uadministrators', 'action_type': '管理取消',
         'name': '管理取消', 'description': '管理取消'}
    ]

    Tabtransition = [
        {'uid': '168d9b8a-de4f-11ed-9d76-2544c8d60402', 'process': '1editor',
         'current_state': 'fe7432e8-de4e-11ed-9d76-2544c8d60402', 'next_state': '06a263fe-de4f-11ed-9d76-2544c8d60402'},
        {'uid': '1b942b76-de4f-11ed-9d76-2544c8d60402', 'process': '1editor',
         'current_state': 'fe7432e8-de4e-11ed-9d76-2544c8d60402', 'next_state': '0f78610e-de4f-11ed-9d76-2544c8d60402'},
        {'uid': '2632b570-de4f-11ed-9d76-2544c8d60402', 'process': 'uadministrators',
         'current_state': 'cb072884-de4e-11ed-9d76-2544c8d60402', 'next_state': 'd3e39294-de4e-11ed-9d76-2544c8d60402'},
        {'uid': '29d73264-de4f-11ed-9d76-2544c8d60402', 'process': 'uadministrators',
         'current_state': 'cb072884-de4e-11ed-9d76-2544c8d60402', 'next_state': 'd957ac2e-de4e-11ed-9d76-2544c8d60402'},
        {'uid': '962395f2-de4f-11ed-9d76-2544c8d60402', 'process': '1editor',
         'current_state': 'fe7432e8-de4e-11ed-9d76-2544c8d60402', 'next_state': '8e935de0-de4f-11ed-9d76-2544c8d60402'},
        {'uid': '9a29745a-de4f-11ed-9d76-2544c8d60402', 'process': 'uadministrators',
         'current_state': 'cb072884-de4e-11ed-9d76-2544c8d60402', 'next_state': '8e935de1-de4f-11ed-9d76-2544c8d60402'}
    ]

    TransitionAction = [
        {'uid': '3687c849-de4f-11ed-9d76-2544c8d60402', 'transition': '168d9b8a-de4f-11ed-9d76-2544c8d60402',
         'action': '3687c848-de4f-11ed-9d76-2544c8d60402'},
        {'uid': '3f38c5c9-de4f-11ed-9d76-2544c8d60402', 'transition': '1b942b76-de4f-11ed-9d76-2544c8d60402',
         'action': '3f38c5c8-de4f-11ed-9d76-2544c8d60402'},
        {'uid': '569bf321-de4f-11ed-9d76-2544c8d60402', 'transition': '2632b570-de4f-11ed-9d76-2544c8d60402',
         'action': '569bf320-de4f-11ed-9d76-2544c8d60402'},
        {'uid': '6149df3b-de4f-11ed-9d76-2544c8d60402', 'transition': '29d73264-de4f-11ed-9d76-2544c8d60402',
         'action': '6149df3a-de4f-11ed-9d76-2544c8d60402'},
        {'uid': 'a89f4b73-de4f-11ed-9d76-2544c8d60402', 'transition': '962395f2-de4f-11ed-9d76-2544c8d60402',
         'action': 'a89f4b72-de4f-11ed-9d76-2544c8d60402'},
        {'uid': 'b58449dd-de4f-11ed-9d76-2544c8d60402', 'transition': '9a29745a-de4f-11ed-9d76-2544c8d60402',
         'action': 'b58449dc-de4f-11ed-9d76-2544c8d60402'}
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
        return True
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
        return True
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
        return True
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
        return True
    except Exception as err:
        print(repr(err))
        return False


if __name__ == '__main__':
    test()
