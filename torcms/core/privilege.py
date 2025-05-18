# -*- coding:utf-8 -*-
'''
针对增删改查的权限进行处理。
'''
import json

from config import ROLE_CFG
from torcms.model.staff2role_model import MStaff2Role


def is_prived(usr_rule, def_rule):
    '''
    Compare between two role string.
    '''
    for ii in range(4):
        if def_rule[ii] == '0':
            continue
        if usr_rule[ii] >= def_rule[ii]:
            return True

    return False


def auth_view(method):
    '''
    role for view.
    '''

    def wrapper(self, *args, **kwargs):
        '''
        wrapper.
        '''
        if ROLE_CFG['view'] == '':
            pass
        elif self.current_user:
            if is_prived(self.userinfo.role, ROLE_CFG['view']):
                return method(self, *args, **kwargs)
            else:
                kwd = {
                    'info': 'No role',
                }
                self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

        else:
            kwd = {
                'info': 'No role',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

        return method(self, *args, **kwargs)

    return wrapper


def auth_add(method):
    '''
    role for add.
    '''

    def wrapper(self, *args, **kwargs):
        '''
        wrapper.
        '''
        if self.current_user:
            if is_prived(self.userinfo.role, ROLE_CFG['add']):
                return method(self, *args, **kwargs)
            else:
                kwd = {
                    'info': 'No role',
                }
                self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

        else:
            kwd = {
                'info': 'No role',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

    return wrapper


def auth_edit(method):
    '''
    role for edit.
    '''

    def wrapper(self, *args, **kwargs):
        '''
        wrapper.
        '''
        if self.current_user:
            if is_prived(self.userinfo.role, ROLE_CFG['edit']):
                return method(self, *args, **kwargs)
            else:
                kwd = {
                    'info': 'No role',
                }
                self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

        else:
            kwd = {
                'info': 'No role',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

    return wrapper


def auth_delete(method):
    '''
    role for delete.
    '''

    def wrapper(self, *args, **kwargs):
        '''
        wrapper.
        '''
        if self.current_user:
            if is_prived(self.userinfo.role, ROLE_CFG['delete']):
                return method(self, *args, **kwargs)
            else:
                kwd = {
                    'info': 'No role',
                }
                self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

        else:
            kwd = {
                'info': 'No role',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

    return wrapper


def auth_admin(method):
    '''
    role for admin.
    '''

    def wrapper(self, *args, **kwargs):
        '''
        wrapper.
        '''

        if self.current_user:
            if is_prived(self.userinfo.role, ROLE_CFG['admin']):
                return method(self, *args, **kwargs)
            else:
                kwd = {
                    'info': 'No role',
                }
                self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)
        else:
            kwd = {
                'info': 'No role',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

    return wrapper


def auth_check(method):
    '''
    role for examine.
    '''

    def wrapper(self, *args, **kwargs):
        '''
        wrapper.
        '''
        if self.current_user:
            if is_prived(self.userinfo.role, ROLE_CFG['check']):
                return method(self, *args, **kwargs)
            else:
                kwd = {
                    'info': 'No role',
                }
                self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

        else:
            kwd = {
                'info': 'No role',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

    return wrapper


def permission(action=''):
    '''
    通用的鉴权装饰器。使用RBAC方式进行鉴权。
    带参数的函数装饰器，需要两层嵌套。参考：https://zhuanlan.zhihu.com/p/269012332
    '''

    def wrapper(func):
        def deco(self, *args, **kwargs):
            print('Need role: ', f'_per_{action}')

            if self.current_user:
                if self.userinfo.user_name == 'admin':
                    func(self, *args, **kwargs)
                elif self.userinfo.extinfo.get(f'_per_{action}', 0) == 1:
                    func(self, *args, **kwargs)
                else:
                    kwd = {"ok": False, "status": 404, "msg": "没有权限"}
                    return json.dump(kwd, self, ensure_ascii=False)
            else:
                kwd = {
                    'info': 'No role',
                }
                #
                # kwd = {
                #     "ok":False,
                #     "status":404,
                #     "msg":""
                # }
                # return json.dump(kwd, self,ensure_ascii=False)

                self.redirect('/user/login')

        return deco

    return wrapper


def app_can_edit(method):
    '''
    role for edit.
    '''

    def wrapper(self, *args, **kwargs):
        '''
        wrapper.
        '''
        if self.current_user:
            if self.userinfo.extinfo.get(f'_per_can_edit', 0) == 1:
                return method(self, *args, **kwargs)
            else:
                kwd = {
                    'info': 'No role',
                }
                self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)
        else:
            kwd = {
                'info': 'No role',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

    return wrapper
