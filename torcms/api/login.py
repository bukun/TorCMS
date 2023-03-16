import datetime
import json
import re
import time

import tornado.web
import wtforms.validators
from wtforms.fields import StringField
from wtforms.validators import DataRequired
from wtforms_tornado import Form
# ToDo: 需要进行切换、测试
# from tornado_wtforms.form import TornadoForm as Form

import config
from config import CMS_CFG
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.core.tool.send_email import send_mail
from torcms.core.tools import logger
from torcms.model.user_model import MUser
from flask import Flask, request, jsonify, make_response


class UserApi(BaseHandler):
    '''
    Handler for user.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.is_p = False

    def get(self, *args, **kwargs):

        url_str = args[0]
        url_arr = self.parse_url(url_str)

        dict_get = {
            'regist': (lambda: self.redirect('/user/info'))
            if self.get_current_user() else self.__to_register__,
            'j_regist':
                self.j_register,
            'login':
                self.__to_login__,
            'info':
                self.__to_show_info__,
            'j_info':
                self.json_info,
            'logout':
                self.__logout__,
            'reset-password':
                self.__to_reset_password__,
            'changepass':
                self.__change_pass__,
            'changeinfo':
                self.__to_change_info__,
            'reset-passwd':
                self.gen_passwd,
            'changerole':
                self.__to_change_role__,
            'find':
                self.find,
            'delete_user':
                self.__delete_user__,
            'list':
                self.__user_list__,
            'pass_strength':
                self.pass_strength,
        }

        if len(url_arr) == 1:
            dict_get.get(url_arr[0])()
        elif len(url_arr) == 2:
            dict_get.get(url_arr[0])(url_arr[1])
        elif len(url_arr) == 3:
            self.__to_find__(url_arr[2])
        else:
            pass

    def post(self, *args, **kwargs):
        '''
        用户操作。
        '''
        _ = kwargs
        url_str = args[0]
        url_arr = self.parse_url(url_str)
        print('Post')

        if url_str == 'regist':
            self.__register__()
        elif url_str == 'login':
            self.login()
        elif url_arr[0] == 'changerole':
            self.__change_role__(url_arr[1])

    @tornado.web.authenticated
    def p_changepassword(self):
        '''
        Changing password.
        '''

        post_data = self.get_request_arguments()

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
        '''

        post_data, def_dic = self.fetch_post_data()

        usercheck = MUser.check_user(self.userinfo.uid, post_data['rawpass'])
        if usercheck == 1:
            MUser.update_info(self.userinfo.uid,
                              post_data['user_email'],
                              extinfo=def_dic)
            output = {'changeinfo ': usercheck}
        else:
            output = {'changeinfo ': 0}
        return json.dump(output, self)

    def fetch_post_data(self):
        '''
        fetch post accessed data. post_data, and ext_dic.
        '''
        post_data = {}
        ext_dic = {}
        for key in self.request.arguments:
            if key.startswith('def_') or key.startswith('ext_'):
                ext_dic[key] = self.get_argument(key, default='')

            else:
                post_data[key] = self.get_arguments(key)[0]

        post_data['user_name'] = self.userinfo.user_name

        ext_dic = dict(ext_dic, **self.ext_post_data(postdata=post_data))

        return (post_data, ext_dic)

    def fetch_user_data(self):
        '''
        fetch post accessed data. post_data, and ext_dic.
        '''
        post_data = {}
        ext_dic = {}
        for key in self.request.arguments:
            if key.startswith('ext_'):
                ext_dic[key] = self.get_argument(key, default='')

            else:
                post_data[key] = self.get_arguments(key)[0]

        ext_dic = dict(ext_dic, **self.ext_post_data(postdata=post_data))

        return (post_data, ext_dic)

    def ext_post_data(self, **kwargs):
        '''
        The additional information.  for add(), or update().
        '''
        _ = kwargs
        return {}

    @tornado.web.authenticated
    def __change_password__(self):
        '''
        Change password
        '''
        post_data = self.get_request_arguments()

        usercheck_num = MUser.check_user(self.userinfo.uid,
                                         post_data['rawpass'])

        if not tools.check_pass_valid(post_data['user_pass']):
            kwd = {
                'info': '密码过于简单，至少包含1个大写字母，1个小写字母和1个数字。',
                'link': '/user/regist',
            }
            self.set_status(400)
            self.render('misc/html/404.html',
                        cfg=config.CMS_CFG,
                        kwd=kwd,
                        userinfo=None)

        else:
            pass

        if usercheck_num == 1:
            MUser.update_pass(self.userinfo.uid, post_data['user_pass'])
            self.redirect('/user/info')
        else:
            kwd = {
                'info': '原密码输入错误，请重新输入',
                'link': '/user/changepass',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

    @tornado.web.authenticated
    def __change_info__(self):
        '''
        Change the user info
        '''

        post_data, def_dic = self.fetch_post_data()

        usercheck_num = MUser.check_user(self.userinfo.uid,
                                         post_data['rawpass'])
        if usercheck_num == 1:
            MUser.update_info(self.userinfo.uid,
                              post_data['user_email'],
                              extinfo=def_dic)
            self.redirect(('/user/info'))
        else:
            kwd = {
                'info': '密码输入错误。',
                'link': '/user/changeinfo',
            }
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

    @tornado.web.authenticated
    def __change_role__(self, xg_username):
        '''
        Change th user rule
        '''
        post_data = self.get_request_arguments()

        # 审核权限
        authority = '0'
        for i in self.get_arguments('authority'):
            authority = bin(int(authority, 2) + int(i, 2))[2:]
        post_data['authority'] = authority

        MUser.update_role(xg_username, post_data)
        if self.is_p:
            output = {'changerole': '1'}
            return json.dump(output, self)
        else:
            self.redirect('/user/info')

    @tornado.web.authenticated
    def __logout__(self):
        '''
        user logout.
        '''
        self.clear_all_cookies()
        print('log out')
        self.redirect('/')

    @tornado.web.authenticated
    def __change_pass__(self):
        '''
        to change the password.
        '''

        if self.is_p:
            tmpl = 'admin/user/puser_changepass.html'
        else:
            tmpl = 'user/user_changepass.html'
        self.render(tmpl,
                    userinfo=self.userinfo,
                    kwd={})

    @tornado.web.authenticated
    def __to_change_info__(self):
        '''
        to change the user info.
        '''
        if self.is_p:
            tmpl = 'admin/user/puser_changeinfo.html'
        else:
            tmpl = 'user/user_changeinfo.html'
        self.render(tmpl,
                    userinfo=self.userinfo,
                    kwd={})

    @tornado.web.authenticated
    def __to_change_role__(self, xg_username):
        '''
        to change the user role
        '''
        try:
            if config.post_cfg:
                post_authority = config.post_cfg
            else:
                post_authority = {}
        except:
            post_authority = {}
        self.render('user/user_changerole.html',
                    userinfo=MUser.get_by_name(xg_username),
                    post_authority=post_authority,
                    kwd={})

    @tornado.web.authenticated
    def __to_find__(self, cur_p=''):
        '''
        to find the user
        '''
        post_data = self.get_request_arguments()
        type = post_data.get('type', '')
        isjson = post_data.get('isjson', False)
        current_page_number = 1
        if cur_p == '':
            current_page_number = 1
        else:
            try:
                current_page_number = int(cur_p)
            except TypeError:
                current_page_number = 1
            except Exception as err:
                print(err.args)
                print(str(err))
                print(repr(err))

        current_page_number = 1 if current_page_number < 1 else current_page_number

        infos = MUser.query_pager_by_slug(current_page_num=current_page_number, type=type)
        kwd = {'pager': '',
               'current_page': current_page_number,
               'type': type
               }
        if isjson:
            list = []
            for rec in infos:
                dic = {
                    'uid': rec.uid,
                    'user_name': rec.user_name,
                    'user_email': rec.user_email,
                    'role': rec.role,
                    'authority': rec.authority,
                    'time_login': rec.time_login,
                    'time_create': rec.time_create,
                    'extinfo': rec.extinfo
                }

                list.append(dic)

            out_dict = {
                'results': list
            }

            return json.dump(out_dict, self, ensure_ascii=False)
        elif self.is_p:
            tmpl = 'admin/user/puser_find_list.html'
        else:
            tmpl = 'user/user_find_list.html'
        self.render(tmpl,
                    cfg=config.CMS_CFG,
                    infos=infos,
                    kwd=kwd,
                    view=MUser.get_by_keyword(""),
                    userinfo=self.userinfo)

    @tornado.web.authenticated
    def __to_show_info__(self, userid=''):
        '''
        show the user info
        '''
        if userid:
            rec = MUser.get_by_uid(userid)
        else:
            rec = MUser.get_by_uid(self.userinfo.uid)
        kwd = {}

        post_data = self.get_request_arguments()
        isjson = post_data.get('isjson', False)
        if isjson:
            dic = {
                'uid': rec.uid,
                'user_name': rec.user_name,
                'user_email': rec.user_email,
                'role': rec.role,
                'authority': rec.authority,
                'time_login': rec.time_login,
                'time_create': rec.time_create,
                'extinfo': rec.extinfo
            }

            out_dict = {
                'results': dic
            }

            return json.dump(out_dict, self, ensure_ascii=False)
        elif self.is_p:
            tmpl = 'admin/user/puser_info.html'
        else:
            tmpl = 'user/user_info.html'

        self.render(tmpl,
                    userinfo=rec,
                    extinfo=rec.extinfo,
                    kwd=kwd)

    def __to_reset_password__(self):
        '''
        to reset the password.
        '''
        self.render('user/user_reset_password.html',
                    userinfo=self.userinfo,
                    kwd={})

    def __to_login__(self):
        '''
        to login.
        '''
        next_url = self.get_argument("next", "/")

        if self.get_current_user():
            self.redirect(next_url)
        else:
            kwd = {
                'pager': '',
                'next_url': next_url,
                'ad': False,
                'pass_encrypt': CMS_CFG.get('pass_encrypt', ',')
            }
            self.render('user/user_login.html', kwd=kwd, userinfo=None)

    def json_batchchangerole(self):
        '''
        Batch Modify Permission
        '''

        post_data = self.get_request_arguments()

        name_list = post_data.get("check_value", '')

        username_list = json.loads(name_list)
        if username_list == []:
            output = {'changerole': '2', 'err_info': 'Please select a user.'}
            return json.dump(output, self)
        # 审核权限
        authority = '0'
        for i in self.get_arguments('authority'):
            authority = bin(int(authority, 2) + int(i, 2))[2:]
        post_data['authority'] = authority
        for xg_username in username_list:
            MUser.update_role(xg_username, post_data)
        if self.is_p:
            output = {'changerole': '1'}
            return json.dump(output, self)
        else:
            self.redirect('/user/info')

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

    def j_register(self):
        '''
        to register.
        '''
        kwd = {
            'pager': '',
        }
        self.render('admin/user/puser_regist.html',
                    cfg=config.CMS_CFG,
                    userinfo=None,
                    kwd=kwd)

    def parseint(self, stringss):
        return int(''.join([x for x in stringss if x.isdigit()]))

    def fromCharCOde(self, passstr, *b):
        return chr(passstr % 65536) + "".join([chr(i % 65536) for i in b])

    def login(self):
        '''
        user login.
        '''
        data = json.loads(self.request.body)
        print("=" * 50)
        print(data)
        print("=" * 50)


        u_name = data['username']
        # u_pass = post_data['user_pass']
        encryption = data.get('encryption', '0')

        self.set_secure_cookie(
            "user",
            u_name,
            expires_days=None,
            expires=time.time() + 60 * CMS_CFG.get('expires_minutes', 15)
        )
        # resp.set_cookie("amisToken", , max_age=3600)
        from datetime import datetime
        now = datetime.now()
        self.set_secure_cookie(
            "amisToken",

            datetime.strftime(now, "%Y-%m-%d %H:%M:%S"),
            expires_days=None,
            expires=time.time() + 60 * CMS_CFG.get('expires_minutes', 15)
        )

        self.set_status(200)
        user_login_status = {'success': True, 'code': '1', 'info': 'Login successful',
        'status': 0,
                             'username': u_name}
        return json.dump( {'data': user_login_status, 'status': 0} , self)

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

    def find(self, keyword=None, cur_p=''):
        '''
        find by keyword.
        '''
        if not keyword:
            self.__to_find__(cur_p)

        kwd = {
            'pager': '',
            'title': '查找结果',
        }

        if self.is_p:
            tmpl = 'admin/user/puser_find_list.html'
        else:
            tmpl = 'user/user_find_list.html'

        self.render(tmpl,
                    kwd=kwd,
                    view=MUser.get_by_keyword(keyword),
                    cfg=config.CMS_CFG,
                    userinfo=self.userinfo)

    def __user_list__(self):
        '''
        find by keyword.
        '''

        month_arr = []
        count_arr = []
        num_arr = []

        jan_arr = []
        feb_arr = []
        mar_arr = []
        apr_arr = []
        may_arr = []
        jun_arr = []
        jul_arr = []
        aug_arr = []
        sep_arr = []
        oct_arr = []
        nov_arr = []
        dec_arr = []

        current_month = datetime.datetime.now().month

        # 获取当年，1月到当前月份注册信息
        recs = MUser.query_by_time(current_month * 30)

        for rec in recs:
            current_mon = time.strftime("%m", time.localtime(rec.time_create))
            if current_mon == '01':
                jan_arr.append(rec)
            elif current_mon == '02':
                feb_arr.append(rec)
            elif current_mon == '03':
                mar_arr.append(rec)
            elif current_mon == '04':
                apr_arr.append(rec)
            elif current_mon == '05':
                may_arr.append(rec)
            elif current_mon == '06':
                jun_arr.append(rec)
            elif current_mon == '07':
                jul_arr.append(rec)
            elif current_mon == '08':
                aug_arr.append(rec)
            elif current_mon == '09':
                sep_arr.append(rec)
            elif current_mon == '10':
                oct_arr.append(rec)
            elif current_mon == '11':
                nov_arr.append(rec)
            elif current_mon == '12':
                dec_arr.append(rec)
            count_arr.append(len(jan_arr))
            count_arr.append(len(feb_arr))
            count_arr.append(len(mar_arr))
            count_arr.append(len(apr_arr))
            count_arr.append(len(may_arr))
            count_arr.append(len(jun_arr))
            count_arr.append(len(jul_arr))
            count_arr.append(len(aug_arr))
            count_arr.append(len(sep_arr))
            count_arr.append(len(oct_arr))
            count_arr.append(len(nov_arr))
            count_arr.append(len(dec_arr))

            for mon in range(0, current_month):
                month_arr.append(mon + 1)
                num_arr.append(count_arr[mon])

            kwd = {
                'pager': '',
                'title': '查找结果',
                'user_count': MUser.total_number(),
                'month_arr': month_arr,
                'num_arr': num_arr,
            }

            self.render('user/user_list.html',
                        recs=recs,
                        kwd=kwd,
                        view=MUser.query_by_time(),
                        cfg=config.CMS_CFG,
                        userinfo=self.userinfo)

    def __delete_user__(self, user_id):
        '''
        delete user by ID.
        '''
        if self.is_p:
            if MUser.delete(user_id):
                output = {'del_category': 1}
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
        '''
        keyword = self.get_argument('keyword', default='')
        self.find(keyword)

    def reset_password(self):
        '''
        Do reset password
        :return: None
        '''
        post_data = self.get_request_arguments()

        if 'email' in post_data:
            userinfo = MUser.get_by_email(post_data['email'])

            if tools.timestamp() - userinfo.time_reset_passwd < 70:
                self.set_status(400)
                kwd = {
                    'info': '两次重置密码时间应该大于1分钟',
                    'link': '/user/reset-password',
                }
                self.render('misc/html/404.html',
                            kwd=kwd,
                            userinfo=self.userinfo)
                return False

            if userinfo:
                timestamp = tools.timestamp()
                passwd = userinfo.user_pass
                username = userinfo.user_name
                hash_str = tools.md5(username + str(timestamp) + passwd)
                url_reset = '{0}/user/reset-passwd?u={1}&t={2}&p={3}'.format(
                    config.SITE_CFG['site_url'], username, timestamp, hash_str)
                email_cnt = '''<div>请查看下面的信息，并<span style="color:red">谨慎操作</span>：</div>
                <div>您在"{0}"网站（{1}）申请了密码重置，如果确定要进行密码重置，请打开下面链接：</div>
                <div><a href={2}>{2}</a></div>
                <div>如果无法确定本信息的有效性，请忽略本邮件。</div>'''.format(
                    config.SMTP_CFG['name'], config.SITE_CFG['site_url'],
                    url_reset)

                if send_mail([userinfo.user_email],
                             "{0}|密码重置".format(config.SMTP_CFG['name']),
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
        post_data = self.get_request_arguments()

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
            self.render('misc/html/404.html', kwd=kwd, userinfo=self.userinfo)

        hash_str = tools.md5(userinfo.user_name + post_data['t'] +
                             userinfo.user_pass)
        if hash_str == post_data['p']:
            pass
        else:
            kwd = {
                'info': '密码重置验证出错！',
                'link': '/user/reset-password',
            }
            self.set_status(400)
            self.render(
                'misc/html/404.html',
                kwd=kwd,
                userinfo=self.userinfo,
            )

        new_passwd = tools.get_uu8d()
        MUser.update_pass(userinfo.uid, new_passwd)
        kwd = {
            'user_name': userinfo.user_name,
            'new_pass': new_passwd,
        }
        self.render(
            'user/user_show_pass.html',
            cfg=config.CMS_CFG,
            kwd=kwd,
            userinfo=self.userinfo,
        )

    @tornado.web.authenticated
    def json_info(self):
        '''
        show the user info
        '''
        post_data = self.get_request_arguments()
        user_name = post_data.get('user_name', '')
        rec = MUser.get_by_uid(self.userinfo.uid)
        # rec = MUser.get_by_name(user_name)

        userinfo = {
            'user_name': rec.user_name,
            'user_email': rec.user_email,
            'role': rec.role,
            'extinfo': rec.extinfo,

        }
        return json.dump(userinfo, self, ensure_ascii=False)

    def pass_strength(self, pwd):
        '''
        实现密码强度计算函数:
        1. 实现函数 passworld_strength 返回 0-10 的数值，表示强度，数值越高，密码强度越强
        2. 密码长度在 6 位及以上，强度 +1，
           在 8 位及以上，强度 +2，
           在 12 位及以上，强度 +4
        3. 有大写字母，强度 +2
        4. 除字母外，还包含数字，强度 +2
        5. 有除字母、数字以外字符，强度 +2
        '''

        intensity = 0
        if len(pwd) >= 12:
            intensity += 4
        elif 8 <= len(pwd) < 12:
            intensity += 2
        elif 6 <= len(pwd) < 8:
            intensity += 1
        pwdlist = list(pwd)
        for i in range(len(pwd)):
            if 'A' <= pwdlist[i] <= 'Z':
                intensity += 2
                break
        for i in range(len(pwd)):
            if 'A' <= pwdlist[i] <= 'Z' or 'a' <= pwdlist[i] <= 'z':
                for j in range(len(pwd)):
                    if '0' <= pwdlist[j] <= '9':
                        intensity += 2
                        break
            break
        for i in range(len(pwd)):
            if ('null' <= pwdlist[i] < '0') or ('9' < pwdlist[i] <= '@') or ('Z' < pwdlist[i] <= '`') or (
                    'z' < pwdlist[i] <= '~'):
                intensity += 2
                break

        pass_strength_status = {'intensity': intensity}
        return json.dump(pass_strength_status, self)
