from torcms.model.state_model import MState, MTransition, MTransitionAction, MAction, \
    MRequest, MRequestAction


def test():
    # process = MProcess.query_all().dicts()
    # print("*" * 50)
    # print("process")
    # [print(x) for x in process]
    # print("process")
    # print("-" * 50)

    states = MState.query_all().dicts()
    print("*" * 50)
    print("Tabstate")
    [print(x) for x in states]
    print("Tabstate")
    print("-" * 50)

    action = MAction.query_all().dicts()
    print("*" * 50)
    print("action")
    [print(x) for x in action]
    print("action")
    print("-" * 50)

    # stateaction = MStateAction.query_all().dicts()
    # print("*" * 50)
    # print("stateaction")
    # [print(x) for x in stateaction]
    # print("stateaction")
    # print("-" * 50)

    trans = MTransition.query_all().dicts()
    print("*" * 50)
    print("Tabtrans")
    [print(x) for x in trans]
    print("Tabtrans")
    print("-" * 50)

    transaction = MTransitionAction.query_all().dicts()
    print("*" * 50)
    print("TransitionAction")
    [print(x) for x in transaction]
    print("TransitionAction")
    print("-" * 50)

    request = MRequest.query_all().dicts()
    print("*" * 50)
    print("request")
    [print(x) for x in request]
    print("request")
    print("-" * 50)

    RequestAction = MRequestAction.query_all().dicts()
    print("*" * 50)
    print("RequestAction")
    [print(x) for x in RequestAction]
    print("RequestAction")
    print("-" * 50)


if __name__ == '__main__':
    test()
    # uu = MState()
    # tt = MProcess()
    # tt.create_or_update('1', 'Post')
    #
    # state_arr = [
    #     ['started', '开始'],
    #     ['denied', '回退'],
    #     ['complated', '完成'],
    #     ['cancceled', '取消'],
    # ]
    #
    # for statinfo in state_arr:
    #     info = {'state_type': statinfo[0], 'name': statinfo[1]}
    #     uu.create_or_update(info)
    # all_state = uu.query_all().dicts()
    # [print(x) for x in all_state]
