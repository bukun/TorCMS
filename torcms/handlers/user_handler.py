# -*- coding:utf-8 -*-

'''
Handler for user.
'''

import json

import tornado
import tornado.escape
import tornado.web
import wtforms.validators
from wtforms.fields import StringField
from wtforms.validators import DataRequired
from wtforms_tornado import Form

import config
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.core.tool.send_email import send_mail
from torcms.model.user_model import MUser
from torcms.core.tools import logger


class SumForm(Form):
    '''
    WTForm for user.
    '''
    user_name = StringField('user_name', validators=[DataRequired()])
    user_pass = StringField('user_pass', validators=[DataRequired()])
    user_email = StringField('user_email', validators=[DataRequired(), wtforms.validators.Email()])


class SumFormInfo(Form):
    '''
    WTForm for user.
    '''
    user_email = StringField('user_email', validators=[DataRequired(), wtforms.validators.Email()])


class SumFormPass(Form):
    '''
    WTForm for user password.
    '''
    user_pass = StringField('user_pass', validators=[DataRequired()])


class UserHandler(BaseHandler):
    '''
    Handler for user.
    '''

    def initialize(self, **kwargs):
        super(UserHandler, self).initialize()

    def get(self, *args, **kwargs):

        url_str = args[0]
        url_arr = self.parse_url(url_str)

        dict_get = {
            'regist': (
                lambda: self.redirect('/user/info')
            ) if self.get_current_user() else self.__to_register__,
            'login': self.__to_login__,
            'info': self.__to_show_info__,
            'logout': self.__logout__,
            'reset-password': self.__to_reset_password__,
            'changepass': self.__change_pass__,
            'changeinfo': self.__to_change_info__,
            'reset-passwd': self.gen_passwd,
            'changerole': self.__to_change_role__,
            'find': self.find,
            'delete_user': self.__delete_user__,
        }

        if len(url_arr) == 1:
            dict_get.get(url_arr[0])()
        elif len(url_arr) == 2:
            dict_get.get(url_arr[0])(url_arr[1])
        else:
            pass

    def post(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        # ToDo: change to dict.
        if url_str == 'regist':
            self.__register__()
        elif url_str == 'j_regist':
            self.json_register()
        elif url_str == 'j_changeinfo':
            self.json_changeinfo()
        elif url_str == 'j_changepass':
            self.json_changepass()
        elif url_str == 'login':
            self.login()
        elif url_str == 'changepass':
            self.__change_password__()
        elif url_arr[0] == 'changepass':
            self.p_changepassword()
        elif url_str == 'changeinfo':
            self.__change_info__()
        elif url_arr[0] == 'changeinfo':
            self.p_changeinfo()
        elif url_str == 'find':
            self.post_find()
        elif url_arr[0] == 'find':
            self.find(url_arr[1])
        elif url_str == 'reset-password':
            self.reset_password()
        elif url_arr[0] == 'changerole':
            self.__change_role__(url_arr[1])

    @tornado.web.authenticated
    def p_changepassword(self):
        '''
        Changing password.
        '''

        post_data = self.get_post_data()

        usercheck = MUser.check_user(self.userinfo.uid, post_data['rawpass'])
        if usercheck == 1:
            MUser.update_pass(self.userinfo.uid, post_data['user_pass'])
            output = {'changepass ': usercheck}
        else:
            output = {'changepass ': 0}
        return json.dump(output, self)

    @tornado.web.authenticated
    def p_changeinfo(self):
        '''
        Change Infor via Ajax.
        :return:
        '''

        post_data, def_dic = self.fetch_post_data()

        usercheck = MUser.check_user(self.userinfo.uid, post_data['rawpass'])
        if usercheck == 1:
            MUser.update_info(self.userinfo.uid, post_data['user_email'], extinfo=def_dic)
            output = {'changeinfo ': usercheck}
        else:
            output = {'changeinfo ': 0}
        return json.dump(output, self)

    def fetch_post_data(self):
        '''
        fetch post accessed data. post_data, and ext_dic.
        :return:
        '''
        post_data = {}
        ext_dic = {}
        for key in self.request.arguments:
            if key.startswith('def_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)[0]

        post_data['user_name'] = self.userinfo.user_name

        ext_dic = dict(ext_dic, **self.ext_post_data(postdata=post_data))
        print("*" * 50)
        print(ext_dic)
        return (post_data, ext_dic)

    def ext_post_data(self, **kwargs):
        '''
        The additional information.  for add(), or update().
        :param post_data:
        :return: directory.
        '''
        _ = kwargs
        return {}

    @tornado.web.authenticated
    def __change_password__(self):
        '''
        Change password
        '''
        post_data = self.get_post_data()

        usercheck_num = MUser.check_user(self.userinfo.uid, post_data['rawpass'])
        if usercheck_num == 1:
            MUser.update_pass(self.userinfo.uid, post_data['user_pass'])
            self.redirect('/user/info')
        else:
            kwd = {
                'info': '原密码输入错误，请重新输入',
                'link': '/user/changepass',
            }
            self.render('misc/html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo)

    @tornado.web.authenticated
    def __change_info__(self):
        '''
        Change the user info
        '''

        post_data, def_dic = self.fetch_post_data()

        usercheck_num = MUser.check_user(self.userinfo.uid, post_data['rawpass'])
        if usercheck_num == 1:
            MUser.update_info(self.userinfo.uid, post_data['user_email'], extinfo=def_dic)
            self.redirect(('/user/info'))
        else:
            kwd = {
                'info': '密码输入错误。',
                'link': '/user/changeinfo',
            }
            self.render('misc/html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo)

    @tornado.web.authenticated
    def __change_role__(self, xg_username):
        '''
        Change th user rule
        '''
        post_data = self.get_post_data()

        # if self.tmpl_router == "user":
        MUser.update_role(xg_username, post_data['role'])
        self.redirect('/user/info')
        # else:
        #     if MUser.update_role(xg_username, post_data['role']):
        #         output = {'del_category ': 1}
        #     else:
        #         output = {'del_category ': 0}
        #     return json.dump(output, self)

    @tornado.web.authenticated
    def __logout__(self):
        '''
        user logout.
        '''
        self.clear_all_cookies()
        self.redirect('/')

    @tornado.web.authenticated
    def __change_pass__(self):
        '''
        to change the password.
        '''

        self.render(self.wrap_tmpl('user/{sig}user_changepass.html'),
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def __to_change_info__(self):
        '''
        to change the user info.
        '''
        self.render(self.wrap_tmpl('user/{sig}user_changeinfo.html'),
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def __to_change_role__(self, xg_username):
        '''
        to change the user role
        '''
        self.render('user/user_changerole.html',
                    userinfo=MUser.get_by_name(xg_username))

    @tornado.web.authenticated
    def __to_find__(self, ):
        '''
        to find the user
        '''
        kwd = {
            'pager': '',
        }
        self.render(self.wrap_tmpl('user/{sig}user_find_list.html'),
                    cfg=config.CMS_CFG,
                    kwd=kwd,
                    view=MUser.get_by_keyword(""),
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def __to_show_info__(self):
        '''
        show the user info
        '''
        rec = MUser.get_by_uid(self.userinfo.uid)
        self.render(self.wrap_tmpl('user/{sig}user_info.html'),
                    userinfo=self.userinfo,
                    extinfo=rec.extinfo)

    def __to_reset_password__(self):
        '''
        to reset the password.
        '''
        self.render('user/user_reset_password.html',
                    userinfo=self.userinfo, )

    def __to_login__(self):
        '''
        to login.
        '''
        print('to losafd')
        next_url = self.get_argument("next", "/")
        if self.get_current_user():
            self.redirect(next_url)
        else:
            kwd = {
                'pager': '',
                'next_url': next_url,
            }
            self.render('user/user_login.html',
                        kwd=kwd,
                        userinfo=None)

    def __check_valid(self, post_data):
        '''
        To check if the user is succesfully created.
        Return the status code dict.
        '''
        user_create_status = {'success': False, 'code': '00'}

        if not tools.check_username_valid(post_data['user_name']):
            user_create_status['code'] = '11'
            return user_create_status
        elif not tools.check_email_valid(post_data['user_email']):
            user_create_status['code'] = '21'
            return user_create_status
        elif MUser.get_by_name(post_data['user_name']):
            user_create_status['code'] = '12'
            return user_create_status
        elif MUser.get_by_email(post_data['user_email']):
            user_create_status['code'] = '22'
            return user_create_status

        user_create_status['success'] = True
        return user_create_status

    def __check_valid_info(self, post_data):
        user_create_status = {'success': False, 'code': '00'}

        if not tools.check_email_valid(post_data['user_email']):
            user_create_status['code'] = '21'
            return user_create_status
        elif MUser.get_by_email(post_data['user_email']):
            user_create_status['code'] = '22'
            return user_create_status

        user_create_status['success'] = True
        return user_create_status

    def __check_valid_pass(self, _):
        # ToDo: todo.
        '''
        '''
        user_create_status = {'success': False, 'code': '00'}
        #    user_create_status['code'] = '31'
        #    return user_create_status

        user_create_status['success'] = True
        return user_create_status

    def __register__(self):
        '''
        regist the user.
        '''
        post_data = self.get_post_data()

        form = SumForm(self.request.arguments)
        ckname = MUser.get_by_name(post_data['user_name'])
        ckemail = MUser.get_by_email(post_data['user_email'])
        if ckname is None:
            pass
        else:
            kwd = {
                'info': '用户名已存在，请更换用户名。',
                'link': '/user/regist',
            }
            self.set_status(400)
            self.render('misc/html/404.html',
                        cfg=config.CMS_CFG,
                        kwd=kwd,
                        userinfo=None)
        if ckemail is None:
            pass
        else:
            kwd = {
                'info': '邮箱已经存在，请更换邮箱。',
                'link': '/user/regist',
            }
            self.set_status(400)
            self.render('misc/html/404.html',
                        cfg=config.CMS_CFG,
                        kwd=kwd,
                        userinfo=None)
        if form.validate():
            res_dic = MUser.create_user(post_data)
            if res_dic['success']:
                self.redirect('/user/login')
            else:
                kwd = {
                    'info': '注册不成功',
                    'link': '/user/regist',
                }
                self.set_status(400)
                self.render('misc/html/404.html',
                            cfg=config.CMS_CFG,
                            kwd=kwd,
                            userinfo=None)

        else:
            kwd = {
                'info': '注册不成功',
                'link': '/user/regist',
            }
            self.set_status(400)
            self.render('misc/html/404.html',
                        cfg=config.CMS_CFG,
                        kwd=kwd,
                        userinfo=None)

    def json_register(self):
        '''
        The first char of 'code' stands for the different field.
        '1' for user_name
        '2' for user_email
        '3' for user_pass
        '4' for user_role
        The seconde char of 'code' stands for different status.
        '1' for invalide
        '2' for already exists.
        '''
        # user_create_status = {'success': False, 'code': '00'}
        post_data = self.get_post_data()
        user_create_status = self.__check_valid(post_data)
        if not user_create_status['success']:
            return json.dump(user_create_status, self)

        form = SumForm(self.request.arguments)

        if form.validate():
            user_create_status = MUser.create_user(post_data)
            logger.info('user_register_status: {0}'.format(user_create_status))
            return json.dump(user_create_status, self)
        return json.dump(user_create_status, self)

    def json_changeinfo(self):
        '''
        The first char of 'code' stands for the different field.
        '1' for user_name
        '2' for user_email
        '3' for user_pass
        '4' for user_role
        The seconde char of 'code' stands for different status.
        '1' for invalide
        '2' for already exists.
        '''

        # user_create_status = {'success': False, 'code': '00'}
        post_data = self.get_post_data()

        is_user_passed = MUser.check_user(self.userinfo.uid, post_data['rawpass'])

        if is_user_passed == 1:

            user_create_status = self.__check_valid_info(post_data)
            if not user_create_status['success']:
                return json.dump(user_create_status, self)

            form_info = SumFormInfo(self.request.arguments)

            if form_info.validate():
                user_create_status = MUser.update_info(self.userinfo.uid, post_data['user_email'])
                return json.dump(user_create_status, self)
            return json.dump(user_create_status, self)
        return False

    def json_changepass(self):
        '''
        The first char of 'code' stands for the different field.
        '1' for user_name
        '2' for user_email
        '3' for user_pass
        '4' for user_role
        The seconde char of 'code' stands for different status.
        '1' for invalide
        '2' for already exists.
        '''

        # user_create_status = {'success': False, 'code': '00'} # Not used currently.
        post_data = self.get_post_data()

        check_usr_status = MUser.check_user(self.userinfo.uid, post_data['rawpass'])

        if check_usr_status == 1:

            user_create_status = self.__check_valid_pass(post_data)
            if not user_create_status['success']:
                return json.dump(user_create_status, self)

            form_pass = SumFormPass(self.request.arguments)

            if form_pass.validate():
                MUser.update_pass(self.userinfo.uid, post_data['user_pass'])
                return json.dump(user_create_status, self)

            return json.dump(user_create_status, self)

        return False

    def __to_register__(self):
        '''
        to register.
        '''
        kwd = {
            'pager': '',
        }
        self.render('user/user_regist.html',
                    cfg=config.CMS_CFG,
                    userinfo=None,
                    kwd=kwd)

    def login(self):
        '''
        user login.
        '''
        post_data = self.get_post_data()

        if 'next' in post_data:
            next_url = post_data['next']
        else:
            next_url = '/'

        u_name = post_data['user_name']
        u_pass = post_data['user_pass']

        result = MUser.check_user_by_name(u_name, u_pass)

        # Todo: the kwd should remove from the codes.
        if result == 1:
            self.set_secure_cookie("user", u_name)
            MUser.update_time_login(u_name)
            self.redirect(next_url)
        elif result == 0:
            self.set_status(401)

            self.render('user/user_relogin.html',
                        cfg=config.CMS_CFG,
                        kwd={
                            'info': '密码验证出错，请重新登陆。',
                            'link': '/user/login',
                        },
                        userinfo=self.userinfo)
        elif result == -1:
            self.set_status(401)
            self.render('misc/html/404.html',
                        cfg=config.CMS_CFG,
                        kwd={
                            'info': '没有这个用户',
                            'link': '/user/login',
                        },
                        userinfo=self.userinfo)
        else:
            self.set_status(305)
            self.redirect("{0}".format(next_url))

    def p_to_find(self, ):
        '''
        To find, pager.
        '''
        kwd = {
            'pager': '',

        }
        self.render('user/user_find_list.html',
                    kwd=kwd,
                    view=MUser.get_by_keyword(""),
                    cfg=config.CMS_CFG,
                    userinfo=self.userinfo)

    def find(self, keyword=None):
        '''
        find by keyword.
        '''
        if not keyword:
            self.__to_find__()
        kwd = {
            'pager': '',
            'title': '查找结果',
        }

        self.render(self.wrap_tmpl('user/{sig}user_find_list.html'),
                    kwd=kwd,
                    view=MUser.get_by_keyword(keyword),
                    cfg=config.CMS_CFG,
                    userinfo=self.userinfo)

    def __delete_user__(self, user_id):
        '''
        delete user by ID.
        '''
        if self.is_p:
            if MUser.delete(user_id):
                output = {
                    'del_category': 1
                }
            else:
                output = {
                    'del_category': 0,
                }

            return json.dump(output, self)

        else:
            is_deleted = MUser.delete(user_id)
            if is_deleted:
                self.redirect('/user/find')

    def post_find(self):
        '''
        Do find user.
        :return:
        '''
        keyword = self.get_argument('keyword')
        self.find(keyword)

    def reset_password(self):
        '''
        Do reset password
        :return:
        '''
        post_data = self.get_post_data()

        if 'email' in post_data:
            userinfo = MUser.get_by_email(post_data['email'])

            if tools.timestamp() - userinfo.time_reset_passwd < 70:
                self.set_status(400)
                kwd = {
                    'info': '两次重置密码时间应该大于1分钟',
                    'link': '/user/reset-password',
                }
                self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)
                return False

            if userinfo:
                timestamp = tools.timestamp()
                passwd = userinfo.user_pass
                username = userinfo.user_name
                hash_str = tools.md5(username + str(timestamp) + passwd)
                url_reset = '{0}/user/reset-passwd?u={1}&t={2}&p={3}'.format(
                    config.SITE_CFG['site_url'],
                    username,
                    timestamp,
                    hash_str)
                email_cnt = '''<div>请查看下面的信息，并<span style="color:red">谨慎操作</span>：</div>
            <div>您在"{0}"网站（{1}）申请了密码重置，如果确定要进行密码重置，请打开下面链接：</div>
            <div><a href={2}>{2}</a></div>
            <div>如果无法确定本信息的有效性，请忽略本邮件。</div>'''.format(config.SMTP_CFG['name'],
                                                       config.SITE_CFG['site_url'],
                                                       url_reset)

                if send_mail([userinfo.user_email], "{0}|密码重置".format(config.SMTP_CFG['name']),
                             email_cnt):
                    MUser.update_time_reset_passwd(username, timestamp)
                    self.set_status(200)
                    logger.info('password has been reset.')
                    return True

                self.set_status(400)
                return False
            self.set_status(400)
            return False
        self.set_status(400)
        return False

    def gen_passwd(self):
        '''
        reseting password
        '''
        post_data = self.get_post_data()

        userinfo = MUser.get_by_name(post_data['u'])

        sub_timestamp = int(post_data['t'])
        cur_timestamp = tools.timestamp()
        if cur_timestamp - sub_timestamp < 600 and cur_timestamp > sub_timestamp:
            pass
        else:
            kwd = {
                'info': '密码重置已超时！',
                'link': '/user/reset-password',
            }
            self.set_status(400)
            self.render('misc/html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo)

        hash_str = tools.md5(userinfo.user_name + post_data['t'] + userinfo.user_pass)
        if hash_str == post_data['p']:
            pass
        else:
            kwd = {
                'info': '密码重置验证出错！',
                'link': '/user/reset-password',
            }
            self.set_status(400)
            self.render('misc/html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo, )

        new_passwd = tools.get_uu8d()
        MUser.update_pass(userinfo.uid, new_passwd)
        kwd = {
            'user_name': userinfo.user_name,
            'new_pass': new_passwd,
        }
        self.render('user/user_show_pass.html',
                    cfg=config.CMS_CFG,
                    kwd=kwd,
                    userinfo=self.userinfo, )


class UserPartialHandler(UserHandler):
    '''
    Partially render for user handler.
    '''

    def initialize(self, **kwargs):
        super(UserPartialHandler, self).initialize()
        self.is_p = True
