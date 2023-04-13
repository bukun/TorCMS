from torcms.model.process_model import TabProcess, TabState, TabAction, TabRequest, TabTransition, TabRequestAction, \
    TabMember
from torcms.model.state_model import MState, MTransition, MTransitionAction, MAction, MRequest, MProcess, \
    MRequestAction, MStateAction


def test():
    state_init_dics = [
        {"name": "start", "state_type": "start",
         "description": "开始审核:每个进程只应该一个。此状态是创建新请求时所处的状态",
         "action": [
             {"name": "approve", "action_type": "approve", "description": "操作人将请求应移至下一个状态"},
             {"name": "deny", "action_type": "deny", "description": "操作人将请求应移至上一个状态"},
             {"name": "cancel", "action_type": "cancel", "description": "操作人将请求应在此过程中移至“已取消”状态"}
         ]
         },

        {"name": "complete", "state_type": "complete",
         "description": "完成:表示此状态下的任何请求已正常完成的状态",
         "action": []
         },
        {"name": "denied", "state_type": "denied",
         "description": "拒绝:表示此状态下的任何请求已被拒绝的状态（例如，从未开始且不会被处理）",
         "action": [
             {"name": "deny", "action_type": "deny", "description": "操作人将请求应移至上一个状态"},
         ]
         },
        {"name": "cancelled", "state_type": "cancelled",
         "description": "取消:表示此状态下的任何请求已被取消的状态（例如，工作已开始但尚未完成）",
         "action": [
             {"name": "cancel", "action_type": "cancel", "description": "操作人将请求应在此过程中移至“已取消”状态"}
         ]

         }
    ]

    # process

    pro_id = MProcess.create('部门审核')
    if pro_id:
        pass
    else:
        return False

    # state
    state_get_dics = {}

    for state_dic in state_init_dics:
        post_data = {
            "process": pro_id,
            "name": state_dic['name'],
            "state_type": state_dic['state_type'],
            "description": state_dic['description']
        }

        state_uid = MState.create(post_data)

        if state_uid:
            pass
        else:
            continue

        # Action
        for action_dic in state_dic['action']:
            action = {
                "process": pro_id,
                "name": action_dic['name'],
                "action_type": action_dic['action_type'],
                "description": action_dic['description']
            }

            act_id = MAction.create(pro_id, action)
            MStateAction.create(state_uid, act_id)

    state_start_id = MState.query_by_name('start')
    state_com_id = MState.query_by_name('complete')
    state_denied_id = MState.query_by_name('denied')
    state_cancelled_id = MState.query_by_name('cancelled')
    com_action = MAction.query_by_name('approve')
    den_action = MAction.query_by_name('deny')
    can_action = MAction.query_by_name('cancel')
    for state_dic in state_init_dics:
        if state_dic['name'] == 'start':
            next_static = [{"state": state_com_id, "action": com_action},
                           {"state": state_denied_id, "action": den_action},
                           {"state": state_cancelled_id, "action": can_action}]

        elif state_dic['name'] == 'cancelled':
            next_static = [{"state": state_com_id, "action": com_action},
                           {"state": state_denied_id, "action": den_action}]
        else:
            next_static = {}

        cur_state_id = MState.query_by_name(state_dic['name'])
        if next_static:

            for next_state in next_static:
                trans_id = MTransition.create(pro_id, cur_state_id, next_state['state'])

                # TransitionAction
                MTransitionAction.create(trans_id, next_state['action'])


if __name__ == '__main__':
    test()
