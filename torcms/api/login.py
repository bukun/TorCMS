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
from datetime import datetime
from config import CMS_CFG
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.core.tool.send_email import send_mail
from torcms.core.tools import logger
from torcms.model.user_model import MUser
from torcms.model.staff2role_model import MStaff2Role


def check_regist_info(post_data):
    '''
    check data for user regist.
    Return the status code dict.

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

    if not tools.check_username_valid(post_data['user_name']):
        user_create_status['code'] = '11'
    elif not tools.check_email_valid(post_data['user_email']):
        user_create_status['code'] = '21'
    elif not tools.check_pass_valid(post_data['user_pass']):
        user_create_status['code'] = '41'
    elif MUser.get_by_name(post_data['user_name']):
        user_create_status['code'] = '12'
    elif MUser.get_by_email(post_data['user_email']):
        user_create_status['code'] = '22'
    else:
        user_create_status['success'] = True
    return user_create_status


def check_modify_info(post_data):
    '''
    check data for user infomation modification.
    '''
    user_create_status = {'success': False, 'code': '00'}

    if not tools.check_email_valid(post_data['user_email']):
        user_create_status['code'] = '21'
    elif MUser.get_by_email(post_data['user_email']):
        user_create_status['code'] = '22'
    else:
        user_create_status['success'] = True
    return user_create_status


def check_valid_pass(postdata):
    '''
     对用户密码进行有效性检查。
    '''
    _ = postdata
    user_create_status = {'success': False, 'code': '00'}
    if not tools.check_pass_valid(postdata['user_pass']):
        user_create_status['code'] = '41'
    else:
        user_create_status['success'] = True
    return user_create_status


class SumForm(Form):
    '''
    WTForm for user.
    '''
    user_name = StringField('user_name',
                            validators=[DataRequired()],
                            default='')
    user_pass = StringField('user_pass',
                            validators=[DataRequired()],
                            default='')
    user_email = StringField(
        'user_email',
        validators=[DataRequired(), wtforms.validators.Email()],
        default='')


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

            'info':
                self.__to_show_info__,
            'j_info':
                self.json_info,
            'logout':
                self.__logout__,

            'reset-passwd':
                self.gen_passwd,

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

        if url_str == 'regist':
            self.register()
        elif url_str == 'login':
            self.login()
        elif url_arr[0] == '_edit':
            # 修改用户角色
            self.user_edit_role(url_arr[1])
        elif url_arr[0] == '_delete':
            self.delete_user(url_arr[1]),
        elif url_arr[0] == 'changerole':
            self.__change_role__(url_arr[1])

    def user_edit_role(self, uid):
        '''
        Modify user infomation.
        '''

        post_data = json.loads(self.request.body)
        roles = post_data['ext_role'].split(",")

        for role in roles:
            MStaff2Role.add_or_update(post_data['uid'], role)
        user_edit_role = {
            'success': 'true'
        }
        return json.dump(user_edit_role, self)

    def register(self):
        '''
        user regist.
        '''
        post_data = json.loads(self.request.body)

        user_create_status = check_regist_info(post_data)

        if not user_create_status['success']:
            return json.dump(user_create_status, self)

        user_create_status = MUser.create_user(post_data)

        logger.info('user_register_status: {0}'.format(user_create_status))
        return json.dump(user_create_status, self)

    @tornado.web.authenticated
    def p_changepassword(self):
        '''
        Changing password.
        '''

        post_data = json.loads(self.request.body)

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
    def __change_role__(self, xg_username):
        '''
        Change th user rule
        '''
        post_data = json.loads(self.request.body)

        # 审核权限
        authority = '0'
        for i in self.get_arguments('authority'):
            authority = bin(int(authority, 2) + int(i, 2))[2:]
        post_data['authority'] = authority

        MUser.update_role(xg_username, post_data)

        output = {'changerole': '1'}
        return json.dump(output, self)

    @tornado.web.authenticated
    def __logout__(self):
        '''
        user logout.
        '''
        self.clear_all_cookies()
        print('log out')
        self.redirect('/')

    @tornado.web.authenticated
    def __to_find__(self, cur_p=''):
        '''
        to find the user
        '''
        post_data = json.loads(self.request.body)
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

    @tornado.web.authenticated
    def __to_show_info__(self, userid=''):
        '''
        show the user info
        '''
        if userid:
            rec = MUser.get_by_uid(userid)
        else:
            rec = MUser.get_by_uid(self.userinfo.uid)

        dic = [
            {

                "uid": rec.uid,
                "user_name": rec.user_name,
                'user_email': rec.user_email,
                'role': rec.role,
                'authority': rec.authority,
                'time_login': tools.format_time(rec.time_login),
                'time_create': tools.format_time(rec.time_create),
                'extinfo': rec.extinfo
            }

        ]

        out_dict = {
            'title': '用户信息',
            'userinfo_table': dic
        }

        return json.dump(out_dict, self, ensure_ascii=False)

    def json_batchchangerole(self):
        '''
        Batch Modify Permission
        '''

        post_data = json.loads(self.request.body)

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

        u_name = data['user_name']
        u_pass = data['user_pass']

        check_email = re.compile(r'^\w+@(\w+\.)+(com|cn|net)$')

        result = MUser.check_user_by_name(u_name, u_pass)
        # 根据用户名进行验证，如果不存在，则作为E-mail来获取用户名进行验证
        if result == -1 and check_email.search(u_name):
            user_x = MUser.get_by_email(u_name)
            if user_x:
                result = MUser.check_user_by_name(user_x.user_name, u_pass)

        # Todo: the `kwd` should remove from the codes.
        if result == 1:
            self.set_secure_cookie(
                "user",
                u_name,
                expires_days=None,
                expires=time.time() + 60 * CMS_CFG.get('expires_minutes', 15)
            )

            now = datetime.now()
            self.set_secure_cookie(
                "amisToken",

                datetime.strftime(now, "%Y-%m-%d %H:%M:%S"),
                expires_days=None,
                expires=time.time() + 60 * CMS_CFG.get('expires_minutes', 15)
            )

            MUser.update_success_info(u_name)

            self.set_status(200)
            user_login_status = {'success': True, 'code': '1', 'info': 'Login successful',
                                 'status': 0, 'username': u_name}
            return json.dump({'data': user_login_status, 'status': 0}, self)

    def __user_list__(self):
        '''
        find by keyword.
        '''

        post_data = self.request.arguments  # {'page': [b'1'], 'perPage': [b'10']}
        page = int(str(post_data['page'][0])[2:-1])
        perPage = int(str(post_data['perPage'][0])[2:-1])

        def get_pager_idx():
            '''
            Get the pager index.
            '''

            current_page_number = 1
            if page == '':
                current_page_number = 1
            else:
                try:
                    current_page_number = int(page)
                except TypeError:
                    current_page_number = 1
                except Exception as err:
                    print(err.args)
                    print(str(err))
                    print(repr(err))

            current_page_number = 1 if current_page_number < 1 else current_page_number
            return current_page_number

        dics = []
        current_page_num = get_pager_idx()
        recs = MUser.query_pager_by_slug(current_page_num, num=perPage)
        counts = MUser.count_of_certain()
        for rec in recs:
            dic = {

                "uid": rec.uid,
                "user_name": rec.user_name,
                'user_email': rec.user_email,
                'role': rec.role,
                'authority': rec.authority,
                'time_login': rec.time_login,
                'time_create': rec.time_create,
                'extinfo': rec.extinfo
            }
            dics.append(dic)
        out_dict = {
            "ok": True,
            "status": 0,
            "msg": "ok",
            'data': {"count": counts,
                     "rows": dics
                     }
        }

        return json.dump(out_dict, self, ensure_ascii=False)

    def delete_user(self, user_id):
        '''
        delete user by ID.
        '''

        if MUser.delete(user_id):
            output = {'del_user': 1}
        else:
            output = {
                'del_user': 0,
            }

        return json.dump(output, self)

    def reset_password(self):
        '''
        Do reset password
        :return: None
        '''
        post_data = json.loads(self.request.body)

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
        post_data = json.loads(self.request.body)

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
        post_data = json.loads(self.request.body)
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
