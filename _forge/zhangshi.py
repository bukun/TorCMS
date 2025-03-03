from torcms.core import privilege


class ZhaungshiClass:
    def __init__(self):
        self.info = 'asf'
        self.kind = '1'

    @privilege.permission(action='do_it')
    def run_it(self):
        print('Hello')


def test_it():
    pinfo = ZhaungshiClass()
    pinfo.run_it()


# if __name__ == '__main__':


def permission(kind='', action=''):
    def wrapper(func):
        def deco(*args, **kwargs):
            if kind and action:
                print(kind, action)
                return True
            else:
                return False

            # 真正执行函数的地方
            func(*args, **kwargs)

        return deco

    return wrapper


@permission(kind='1', action='can_add')
def do_it():
    print('func')


@permission(kind='1', action='')
def do_it2():
    print('func')
    return True


def test_all():
    vv = do_it()
    print(vv)
    tt = do_it2()
    print(tt)
