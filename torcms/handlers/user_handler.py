# -*- coding:utf-8 -*-

import json

import tornado
import tornado.escape
import tornado.web
import wtforms.validators
from wtforms.fields import StringField
from wtforms.validators import Required
from wtforms_tornado import Form

import config
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.core.tool.send_email import send_mail
from torcms.model.user_model import MUser
from torcms.core.tools import logger

class SumForm(Form):
    user_name = StringField('user_name', validators=[Required()])
    user_pass = StringField('user_pass', validators=[Required()])
    user_email = StringField('user_email', validators=[Required(), wtforms.validators.Email()])

class SumForm_info(Form):
    user_email = StringField('user_email', validators=[Required(), wtforms.validators.Email()])

class SumForm_pass(Form):
    user_pass = StringField('user_pass', validators=[Required()])


class UserHandler(BaseHandler):
    def initialize(self):
        super(UserHandler, self).initialize()
        self.muser = MUser()
        self.user_name = self.get_current_user()
        self.tmpl_dir = 'user'
        self.tmpl_router = 'info'

    def get(self, url_str):
        url_arr = self.parse_url(url_str)

        if url_str == 'regist':
            if self.get_current_user():
                self.redirect('/')
            else:
                self.__to_register__()
        elif url_str == 'login':
            self.to_login()
        elif url_str == 'info':
            self.show_info()
        elif url_str == 'logout':
            self.logout()
        elif url_str == 'reset-password':
            self.to_reset_password()
        elif url_str == 'changepass':
            self.changepass()

        elif url_str == 'changeinfo':
            self.change_info()
        elif url_str == 'reset-passwd':
            if self.gen_passwd():
                pass
            else:
                self.redirect(config.site_url)
        elif url_arr[0] == 'changerole':
            self.change_role(url_arr[1])
        elif url_str == 'find':
            if self.tmpl_router == "user":
                self.to_find()
            else:
                self.p_to_find()

        elif url_arr[0] == 'find':

            self.find(url_arr[1])
        elif url_arr[0] == 'delete_user':
            self.delete(url_arr[1])

    def post(self, url_str):
        url_arr = self.parse_url(url_str)

        if url_str == 'regist':
            self.register()
        elif url_str == 'j_regist':
            self.json_register()
        elif url_str == 'j_changeinfo':

            self.json_changeinfo()
        elif url_str == 'j_changepass':

            self.json_changepass()
        elif url_str == 'login':
            self.login()
        elif url_str == 'changepass':
            self.changepassword()
        elif url_arr[0] == 'changepass':
            self.p_changepassword()
        elif url_str == 'changeinfo':
            self.changeinfo()
        elif url_arr[0] == 'changeinfo':
            self.p_changeinfo()
        elif url_str == 'find':
            self.post_find()
        elif url_arr[0] == 'find':
            self.find(url_arr[1])
        elif url_str == 'reset-password':
            self.reset_password()
        elif url_arr[0] == 'changerole':
            self.changerole(url_arr[1])

    @tornado.web.authenticated
    def p_changepassword(self):

        post_data = self.get_post_data()


        uu = self.muser.check_user(self.user_name, post_data['rawpass'])
        if uu == 1:
            self.muser.update_pass(self.user_name, post_data['user_pass'])
            output = {
                'changepass ': uu,
            }
        else:
            output = {
                'changepass ': 0,
            }
        return json.dump(output, self)

    @tornado.web.authenticated
    def p_changeinfo(self):

        post_data = self.get_post_data()


        uu = self.muser.check_user(self.user_name, post_data['rawpass'])

        if uu == 1:
            self.muser.update_info(self.user_name, post_data['user_email'])
            output = {
                'changeinfo ': uu,
            }
        else:
            output = {
                'changeinfo ': 0,
            }
        return json.dump(output, self)

    @tornado.web.authenticated
    def changepassword(self):
        post_data = self.get_post_data()

        uu = self.muser.check_user(self.user_name, post_data['rawpass'])
        if uu == 1:
            self.muser.update_pass(self.user_name, post_data['user_pass'])
            self.redirect('/user/info')
        else:
            return False

    @tornado.web.authenticated
    def changeinfo(self):

        post_data = self.get_post_data()


        uu = self.muser.check_user(self.user_name, post_data['rawpass'])

        if uu == 1:
            self.muser.update_info(self.user_name, post_data['user_email'])
            self.redirect(('/user/info'))
        else:
            return False

    @tornado.web.authenticated
    def changerole(self, xg_username):
        post_data = self.get_post_data()

        if self.tmpl_router == "user":
            self.muser.update_role(xg_username, post_data['role'])
            self.redirect(('/user/info'))
        else:
            if self.muser.update_role(xg_username, post_data['role']):
                output = {
                    'del_category ': 1,
                }
            else:
                output = {
                    'del_category ': 0,
                }
            return json.dump(output, self)

    @tornado.web.authenticated
    def logout(self):
        self.clear_all_cookies()
        self.redirect('/')

    @tornado.web.authenticated
    def changepass(self):

        self.render('{1}/{0}/changepass.html'.format(self.tmpl_router,self.tmpl_dir),

                    userinfo=self.userinfo,

                    )

    @tornado.web.authenticated
    def change_info(self):
        self.render('{1}/{0}/changeinfo.html'.format(self.tmpl_router,self.tmpl_dir),
                    userinfo=self.userinfo,
                    )

    @tornado.web.authenticated
    def change_role(self, xg_username):
        self.render('{1}/{0}/changerole.html'.format(self.tmpl_router,self.tmpl_dir),
                    userinfo=self.muser.get_by_name(xg_username))

    @tornado.web.authenticated
    def show_info(self):
        self.render('{1}/{0}/info.html'.format(self.tmpl_router,self.tmpl_dir),
                    userinfo=self.userinfo,
                    )

    def to_reset_password(self):
        self.render('user/{0}/reset_password.html'.format(self.tmpl_router),
                    userinfo=self.userinfo, )

    def to_login(self):
        if self.get_current_user():
            self.redirect('/')
        else:
            kwd = {
                'pager': '',
            }
            self.render('user/{0}/login.html'.format(self.tmpl_router),
                        kwd=kwd,
                        userinfo=None,
                        )

    def __check_valid(self, post_data):
        user_create_status = {'success': False, 'code': '00'}

        if tools.check_username_valid(post_data['user_name']) == False:
            user_create_status['code'] = '11'
            return user_create_status
        elif tools.check_email_valid(post_data['user_email']) == False:
            user_create_status['code'] = '21'
            return user_create_status
        elif self.muser.get_by_name(post_data['user_name']):
            user_create_status['code'] = '12'
            return user_create_status
        elif self.muser.get_by_email(post_data['user_email']):
            user_create_status['code'] = '22'
            return user_create_status

        user_create_status['success'] = True
        print(user_create_status)
        return user_create_status

    def __check_valid_info(self, post_data):
        user_create_status = {'success': False, 'code': '00'}

        if tools.check_email_valid(post_data['user_email']) == False:
            user_create_status['code'] = '21'
            return user_create_status
        elif self.muser.get_by_email(post_data['user_email']):
            user_create_status['code'] = '22'
            return user_create_status

        user_create_status['success'] = True
        return user_create_status

    def __check_valid_pass(self, post_data):
        user_create_status = {'success': False, 'code': '00'}
        #if self.muser.check_user(self.user_name,post_data['user_pass'][0]) ==0:
        #    user_create_status['code'] = '31'
        #    return user_create_status


        user_create_status['success'] = True
        return user_create_status

    def register(self):
        post_data = self.get_post_data()


        form = SumForm(self.request.arguments)

        if form.validate():
            res_dic = self.muser.insert_data(post_data)
            if res_dic['success']:
                self.redirect('/user/login')
            else:
                kwd = {
                    'info': '注册不成功',
                }
                self.set_status(400)
                self.render('html/404.html',
                            cfg=config.cfg,
                            kwd=kwd,
                            userinfo=None, )

        else:
            kwd = {
                'info': '注册不成功',
            }
            self.set_status(400)
            self.render('html/404.html',
                        cfg=config.cfg,
                        kwd=kwd,
                        userinfo=None, )

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
        user_create_status = {'success': False, 'code': '00'}
        post_data = self.get_post_data()
        user_create_status = self.__check_valid(post_data)
        if user_create_status['success'] == False:
            return json.dump(user_create_status, self)

        print('user_register_status:', user_create_status)
        form = SumForm(self.request.arguments)

        if form.validate():
            user_create_status = self.muser.insert_data(post_data)
            print('user_register_status:', user_create_status)
            return json.dump(user_create_status, self)
        else:
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

        user_create_status = {'success': False, 'code': '00'}
        post_data = self.get_post_data()

        uu = self.muser.check_user(self.user_name, post_data['rawpass'])

        if uu == 1:

            user_create_status = self.__check_valid_info(post_data)
            if user_create_status['success'] == False:
                return json.dump(user_create_status, self)

            form_info = SumForm_info(self.request.arguments)


            if form_info.validate():
                user_create_status = self.muser.update_info(self.user_name, post_data['user_email'])
                return json.dump(user_create_status, self)
            else:
                return json.dump(user_create_status, self)



        else:
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


        user_create_status = {'success': False, 'code': '00'}
        post_data = self.get_post_data()

        uu = self.muser.check_user(self.user_name, post_data['rawpass'])

        if uu == 1:

            user_create_status = self.__check_valid_pass(post_data)
            if user_create_status['success'] == False:
                return json.dump(user_create_status, self)

            form_pass = SumForm_pass(self.request.arguments)


            if form_pass.validate():
                self.muser.update_pass(self.user_name, post_data['user_pass'])
                return json.dump(user_create_status, self)
            else:
                return json.dump(user_create_status, self)



        else:
            return False

    def __to_register__(self):
        kwd = {
            'pager': '',
        }
        self.render('user/{0}/regist.html'.format(self.tmpl_router),
                    cfg=config.cfg,
                    userinfo=None,
                    kwd=kwd)

    def login(self):
        post_data = self.get_post_data()

        if 'next' in post_data:
            next_url = post_data['next']
        else:
            next_url = '/'
        u_name = post_data['user_name']
        u_pass = post_data['user_pass']

        kwd = {
            'pager': '',
        }
        result = self.muser.check_user(u_name, u_pass)
        if result == 1:
            self.set_secure_cookie("user", u_name)
            self.muser.update_time_login(u_name)
            self.redirect("{0}".format(next_url))
        elif result == 0:
            self.set_status(401)
            kwd = {
                'info': '密码验证出错，请<a href="/user/login">重新登陆</a>。'
            }
            self.render('user/relogin.html',
                        cfg=config.cfg,
                        kwd=kwd,
                        userinfo=self.userinfo, )
        elif result == -1:
            self.set_status(401)
            kwd = {
                'info': '没有这个用户'
            }
            self.render('html/404.html',
                        cfg=config.cfg,
                        kwd=kwd,
                        userinfo=self.userinfo, )
        else:
            self.set_status(305)
            self.redirect("{0}".format(next_url))

    def to_find(self, ):
        kwd = {
            'pager': '',
        }
        self.render('user/{0}/find.html'.format(self.tmpl_router),
                    cfg=config.cfg,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    )

    def p_to_find(self, ):

        kwd = {
            'pager': '',

        }
        self.render('{1}/{0}/find_list.html'.format(self.tmpl_router,self.tmpl_dir),
                    kwd=kwd,
                    view=self.muser.get_by_keyword(""),
                    cfg=config.cfg,
                    userinfo=self.userinfo,
                    )

    def find(self, keyword):
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '查找结果',
        }
        if self.tmpl_router == "user":
            self.render('user/{0}/find_list.html'.format(self.tmpl_router),
                        kwd=kwd,
                        view=self.muser.get_by_keyword(keyword),
                        cfg=config.cfg,
                        userinfo=self.userinfo,
                        )
        else:
            result = self.muser.get_by_keyword(keyword)
            if result:
                output = {
                    'find': result
                }
            else:
                output = {
                    'find': 0,
                }

            return json.dump(output, self)

    def delete(self, del_id):

        if self.tmpl_router == "user":

            is_deleted = self.muser.delete(del_id)
            if is_deleted:
                self.redirect('/user/find')
            else:
                return False
        else:
            if self.muser.delete(del_id):
                output = {
                    'del_category': 1
                }
            else:
                output = {
                    'del_category': 0,
                }

            return json.dump(output, self)

    def post_find(self):
        keyword = self.get_argument('keyword')
        self.find(keyword)

    def reset_password(self):
        post_data = self.get_post_data()

        if 'email' in post_data:
            userinfo = self.muser.get_by_email(post_data['email'])

            if tools.timestamp() - userinfo.time_reset_passwd < 70:
                self.set_status(400)
                kwd = {
                    'info': '两次重置密码时间应该大于1分钟',
                }
                self.render('html/404.html', kwd=kwd, userinfo=self.userinfo)
                return False

            if userinfo:
                timestamp = tools.timestamp()
                passwd = userinfo.user_pass
                username = userinfo.user_name
                hash_str = tools.md5(username + str(timestamp) + passwd)
                url_reset = '{0}/user/reset-passwd?u={1}&t={2}&p={3}'.format(config.site_url, username, timestamp,
                                                                             hash_str)
                email_cnt = '''
            <div>请查看下面的信息，并<span style="color:red">谨慎操作</span>：</div>
            <div>您在"{0}"网站（{1}）申请了密码重置，如果确定要进行密码重置，请打开下面链接：</div>
            <div><a href={2}>{2}</a></div>
            <div>如果无法确定本信息的有效性，请忽略本邮件。</div>
            '''.format(config.smtp_cfg['name'], config.site_url, url_reset)

                if send_mail([userinfo.user_email], "{0}|密码重置".format(config.smtp_cfg['name']), email_cnt):
                    self.muser.update_time_reset_passwd(username, timestamp)
                    self.set_status(200)
                    logger.info('password has been reset.')
                    return True
                else:
                    self.set_status(400)
                    return False
            else:
                self.set_status(400)
                return False
        else:
            self.set_status(400)
            return False

    def gen_passwd(self):
        post_data = self.get_post_data()

        userinfo = self.muser.get_by_name(post_data['u'])

        sub_timestamp = int(post_data['t'])
        cur_timestamp = tools.timestamp()
        if cur_timestamp - sub_timestamp < 600 and cur_timestamp > sub_timestamp:
            pass
        else:
            kwd = {
                'info': '密码重置已超时！',
            }
            self.set_status(400)
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo)

        hash_str = tools.md5(userinfo.user_name + post_data['t'] + userinfo.user_pass)
        if hash_str == post_data['p']:
            pass
        else:
            kwd = {
                'info': '密码重置验证出错！',
            }
            self.set_status(400)
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo, )

        new_passwd = tools.get_uu8d()
        self.muser.update_pass(userinfo.user_name, new_passwd)
        kwd = {
            'user_name': userinfo.user_name,
            'new_pass': new_passwd,
        }
        self.render('user/{0}/show_pass.html'.format(self.tmpl_router),
                    cfg=config.cfg,
                    kwd=kwd,
                    userinfo=self.userinfo, )


class UserAjaxHandler(UserHandler):
    def initialize(self):
        super(UserAjaxHandler, self).initialize()
        self.muser = MUser()
        self.user_name = self.get_current_user()
        self.tmpl_dir = 'admin'
        self.tmpl_router = 'user_ajax'
