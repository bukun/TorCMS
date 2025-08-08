import datetime
import json
import re
import time
from datetime import datetime

import jwt
import tornado.web

from config import CMS_CFG
from torcms.core import privilege, tools
from torcms.core.base_handler import BaseHandler
from torcms.core.tools import logger
from torcms.model.role2permission_model import MRole2Permission
from torcms.model.role_model import MRole
from torcms.model.staff2role_model import MStaff2Role
from torcms.model.user_model import MUser


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


JWT_TOKEN_EXPIRE_SECONDS = 60 * CMS_CFG.get('expires_minutes', 15)  # token有效时间
JWT_TOKEN_SECRET_SALT = 'salt.2023.07.21'
JWT_TOKEN_ALGORITHM = 'HS256'  # HASH算法


class UserApi(BaseHandler):
    '''
    Handler for user.
    '''

    def initialize(self, **kwargs):
        super().initialize()
        self.is_p = False
        self.kind = 'u'

    def get(self, *args, **kwargs):
        url_str = args[0]
        url_arr = self.parse_url(url_str)

        dict_get = {
            'logout': self.__logout__,
            'vuelogout': self.__vue_logout__,
            'list': self.__user_list__,
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
            self.user_edit_role()
        elif url_arr[0] == '_delete':
            self.delete_user(url_arr[1]),

        elif url_arr[0] == 'batch_edit':
            self.batch_edit()
        elif url_arr[0] == 'batch_delete':
            self.batch_delete(url_arr[1])
        elif url_str == 'verify_jwt':
            self.verify_jwt_token()

    @privilege.permission(action='assign_role')
    def user_edit_role(self):
        '''
        Modify user infomation.
        '''

        post_data = json.loads(self.request.body)
        user_id = post_data['uid']
        if 'ext_role0' in post_data:
            pass
        else:
            return False

        the_roles_arr = []
        extinfo = {}
        def_roles_arr = ['ext_role{0}'.format(x) for x in range(10)]
        for key in def_roles_arr:
            if key not in post_data:
                continue
            if post_data[key] == '' or post_data[key] == '0':
                continue

            if post_data[key] in the_roles_arr:
                continue

            the_roles_arr.append(post_data[key])

        current_roles = MStaff2Role.query_by_staff(user_id).objects()
        for cur_role in current_roles:
            if cur_role.role not in the_roles_arr:
                MStaff2Role.remove_relation(user_id, cur_role.role)
                pers = MRole2Permission.query_by_role(cur_role.role)

                for per in pers:
                    MUser.remove_extinfo(user_id, f'_per_{per.permission}')

        for index, idx_catid in enumerate(the_roles_arr):
            roles = idx_catid.split(",")

            MStaff2Role.add_or_update(user_id, roles[-1])
            pers = MRole2Permission.query_by_role(roles[-1])
            for per in pers:
                extinfo['_per_' + str(per.permission)] = 0

        extinfo['roles'] = the_roles_arr

        out_dic = MUser.update_extinfo(user_id, extinfo)

        if not out_dic['success']:
            user_edit_role = {"ok": False, "status": 404, "msg": "更新失败"}
            return json.dump(user_edit_role, self, ensure_ascii=False)

        if self.userinfo.uid == user_id:
            MUser.update_permissions(post_data['user_name'])

        user_edit_role = {'ok': True, 'status': 0}
        return json.dump(user_edit_role, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def batch_edit(self):
        '''
        Update the link.
        '''

        post_data = json.loads(self.request.body)

        ids = post_data.get("ids", "").split(",")
        for uid in ids:
            user_id = uid
            userinfo = MUser.get_by_uid(user_id)
            if 'ext_role0' in post_data:
                pass
            else:
                return False

            the_roles_arr = []
            extinfo = {}
            def_roles_arr = ['ext_role{0}'.format(x) for x in range(10)]
            for key in def_roles_arr:
                if key not in post_data:
                    continue
                if post_data[key] == '' or post_data[key] == '0':
                    continue

                if post_data[key] in the_roles_arr:
                    continue

                the_roles_arr.append(post_data[key])

            current_roles = MStaff2Role.query_by_staff(user_id).objects()
            for cur_role in current_roles:
                if cur_role.role not in the_roles_arr:
                    MStaff2Role.remove_relation(user_id, cur_role.role)
                    pers = MRole2Permission.query_by_role(cur_role.role)

                    for per in pers:
                        MUser.remove_extinfo(user_id, f'_per_{per.permission}')

            for index, idx_catid in enumerate(the_roles_arr):
                roles = idx_catid.split(",")
                for role in roles:
                    MStaff2Role.add_or_update(user_id, role)
                    pers = MRole2Permission.query_by_role(role)
                    for per in pers:
                        extinfo[f'_per_{per.permission}'] = 0

            extinfo['roles'] = the_roles_arr

            out_dic = MUser.update_extinfo(user_id, extinfo)

            if not out_dic['success']:
                user_edit_role = {"ok": False, "status": 404, "msg": "更新失败"}
                continue

            if self.userinfo.uid == user_id:
                MUser.update_permissions(userinfo.user_name)

            user_edit_role = {'ok': True, 'status': 0}
        return json.dump(user_edit_role, self, ensure_ascii=False)

    def register(self):
        '''
        user regist.
        '''
        post_data = json.loads(self.request.body)

        user_check_status = check_regist_info(post_data)

        if not user_check_status['success']:
            if user_check_status['code'] == '12':
                msg = "用户名已存在"
            elif user_check_status['code'] == '22':
                msg = "邮箱已存在"
            elif user_check_status['code'] == '21':
                msg = "请输入正确的邮箱地址"
            elif user_check_status['code'] == '41':
                msg = "密码6-19位，需包含大小写字母"
            else:
                msg = '注册失败'
            user_check_status = {"ok": False, "status": 404, "msg": msg}
            return json.dump(user_check_status, self, ensure_ascii=False)

        user_create_status = MUser.create_user(post_data)
        if user_create_status['success']:
            the_roles_arr = []
            extinfo = {}
            def_roles_arr = ['ext_role{0}'.format(x) for x in range(10)]
            for key in def_roles_arr:
                if key not in post_data:
                    continue
                if post_data[key] == '' or post_data[key] == '0':
                    continue

                if post_data[key] in the_roles_arr:
                    continue

                the_roles_arr.append(post_data[key])

            for index, idx_catid in enumerate(the_roles_arr):
                roles = idx_catid.split(",")
                for role in roles:
                    MStaff2Role.add_or_update(user_create_status['uid'], role)
                    pers = MRole2Permission.query_by_role(role)
                    for per in pers:
                        extinfo['_per_' + str(per.permission)] = 0

            extinfo['roles'] = the_roles_arr

            MUser.update_extinfo(user_create_status['uid'], extinfo)

            user_create_status = {"ok": True, "status": 0, "msg": "注册成功"}
            logger.info('user_register_status: {0}'.format(user_create_status))
            return json.dump(user_create_status, self, ensure_ascii=False)

    @tornado.web.authenticated
    def __logout__(self):
        '''
        user logout.
        '''

        self.clear_all_cookies()
        self.set_secure_cookie(
            "user",
            '',
        )

        print('log out')

        output = {"ok": True, "status": 0, "msg": "注销登录成功"}
        self.redirect('/')

    @tornado.web.authenticated
    def __vue_logout__(self):
        '''
        user logout.
        '''

        self.clear_all_cookies()
        print('aa')
        self.set_secure_cookie(
            "user",
            '',
        )

        print('log out')

        output = {"ok": True, "status": 0, "msg": "注销登录成功"}
        return json.dump(output, self, ensure_ascii=False)

    @tornado.web.authenticated
    def __to_find__(self, cur_p=''):
        '''
        to find the user
        '''
        post_data = json.loads(self.request.body)
        type = post_data.get('type', '')
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

        infos = MUser.query_pager_by_slug(
            current_page_num=current_page_number, type=type
        )
        kwd = {'pager': '', 'current_page': current_page_number, 'type': type}

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
                'extinfo': rec.extinfo,
            }

            list.append(dic)

        out_dict = {'results': list}

        return json.dump(out_dict, self, ensure_ascii=False)

    def generate_jwt_token(self, user_name):
        """根据用户user_name生成token"""

        data = {
            'user_name': user_name,
            'exp': int(time.time()) + JWT_TOKEN_EXPIRE_SECONDS,
        }
        print("generate data:", data)
        try:
            jwtToken = jwt.encode(
                data, JWT_TOKEN_SECRET_SALT, algorithm=JWT_TOKEN_ALGORITHM
            )

        except:
            jwtToken = ''
        return jwtToken

    def verify_jwt_token(self, **kwargs):
        """验证用户token"""

        post_data = json.loads(self.request.body)

        user_name = post_data.get('user_name', '')
        token = post_data.get('token', '')
        data = {'user_name': user_name}

        try:
            payload = jwt.decode(
                token, JWT_TOKEN_SECRET_SALT, algorithms=[JWT_TOKEN_ALGORITHM]
            )

            print("data:", data)
            print("payload:", payload)
            exp = int(payload.pop('exp'))
            print("exp:", exp)
            print("time.time():", time.time())
            if time.time() > exp:
                print('已失效')

                return json.dump({'code': 1, 'state': False, 'info': 'expired'}, self)
            if data == payload:
                userinfo = MUser.get_by_name(user_name)
                user_pers = MStaff2Role.query_permissions(userinfo.uid)
                user_roles = MStaff2Role.get_role_by_uid(userinfo.uid)

                cur_user_per = []
                if user_pers:
                    for key in user_pers:
                        cur_user_per.append(key['permission'])

                cur_user_role = []
                if user_roles:
                    for role in user_roles:
                        cur_user_role.append({role['uid']: role['name']})

                self.set_status(200)
                user_info = {
                    'ok': True,
                    'code': 0,
                    'msg': 'Verification successful',
                    'status': 0,
                    'username': user_name,
                    'access_token': token,
                    'user_pers': cur_user_per,
                    'user_roles': cur_user_role,
                }
                print("验证成功:", payload)
                return json.dump(
                    {
                        'code': 0,
                        'state': True,
                        'info': 'Verification successful',
                        'userinfo': user_info,
                    },
                    self,
                )
            else:
                print("验证失败:", payload)
                return json.dump({'code': 1, 'state': False, 'info': 'expired'}, self)

        except jwt.exceptions.ExpiredSignatureError as ex:
            print('token签名过期:', ex)
            return json.dump(
                {'code': 1, 'state': False, 'info': 'Token signature expired'}, self
            )

        except jwt.PyJWTError as ex:
            print('token解析失败:', ex)
            return json.dump(
                {'code': 1, 'state': False, 'info': 'Token parsing failed'}, self
            )

    def login(self):
        '''
        user login.
        '''
        data = json.loads(self.request.body)

        u_name = data['user_name']
        u_pass = data['user_pass']
        login_method = data.get('login_method', 'amis')
        check_email = re.compile(r'^\w+@(\w+\.)+(com|cn|net)$')

        result = MUser.check_user_by_name(u_name, u_pass)

        # 根据用户名进行验证，如果不存在，则作为E-mail来获取用户名进行验证
        if result == -1 and check_email.search(u_name):
            user_x = MUser.get_by_email(u_name)
            if user_x:
                result = MUser.check_user_by_name(user_x.user_name, u_pass)

        if result == 1:
            userinfo = MUser.get_by_name(u_name)
            if login_method == 'amis':
                if u_name == 'admin':
                    pass
                elif userinfo.extinfo.get('_per_assign_role', 0) == 1:
                    pass
                else:
                    kwd = {"ok": False, "status": 404, "msg": "没有权限"}
                    return json.dump(kwd, self, ensure_ascii=False)

            self.set_secure_cookie(
                "user",
                u_name,
                expires_days=None,
                expires=time.time() + 60 * CMS_CFG.get('expires_minutes', 15),
            )

            now = datetime.now()
            self.set_secure_cookie(
                "amisToken",
                datetime.strftime(now, "%Y-%m-%d %H:%M:%S"),
                expires_days=None,
                expires=time.time() + 60 * CMS_CFG.get('expires_minutes', 15),
            )

            MUser.update_success_info(u_name)

            # jwt
            jwtToken = self.generate_jwt_token(u_name)

            user_pers = MStaff2Role.query_permissions(userinfo.uid)
            user_roles = MStaff2Role.get_role_by_uid(userinfo.uid)

            cur_user_per = []
            if user_pers:
                for key in user_pers:
                    cur_user_per.append(key['permission'])

            cur_user_role = []
            if user_roles:
                for role in user_roles:
                    cur_user_role.append({role['uid']: role['name']})

            self.set_status(200)
            user_login_status = {
                'ok': True,
                'code': '1',
                'msg': '登录成功',
                'status': 0,
                'username': u_name,
                'access_token': jwtToken,
                'user_pers': cur_user_per,
                'user_roles': cur_user_role,
            }
            return json.dump({'data': user_login_status, 'status': 0}, self)
        else:
            user_login_status = {
                "ok": False,
                "status": 404,
                "msg": "帐号或密码错误，登录失败",
            }
            return json.dump(user_login_status, self, ensure_ascii=False)

    def __user_list__(self):
        '''
        find by keyword.
        '''

        post_data = self.request.arguments  # {'page': [b'1'], 'perPage': [b'10']}

        page = int(post_data['page'][0].decode('utf-8'))
        perPage = int(post_data['perPage'][0].decode('utf-8'))
        if 'user_name' in post_data and post_data['user_name'] != '':
            find_name = str(post_data.get('user_name', '')[0].decode('utf-8'))
        else:
            find_name = ''

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

        recs = MUser.query_pager_by_slug(
            current_page_num, user_name=find_name, num=perPage
        )

        counts = MUser.count_of_certain()

        for rec in recs:
            dic = {
                'uid': rec.uid,
                'user_name': rec.user_name,
                'user_email': rec.user_email,
                'authority': rec.authority,
                'time_login': tools.format_time(rec.time_login),
                'time_create': tools.format_time(rec.time_create),
                'extinfo': rec.extinfo,
                'staff_roles': self.get_role_by_uid(rec.extinfo.get('roles', '')),
            }
            dics.append(dic)
        out_dict = {
            "ok": True,
            "status": 0,
            "msg": "ok",
            'data': {"count": counts, "rows": dics},
        }

        return json.dump(out_dict, self, ensure_ascii=False)

    def get_role_by_userid(self, user_id):
        roles = MStaff2Role.get_role_by_uid(user_id)

        role_arr = []
        if roles:
            for role in roles:
                role_arr.append(role['name'])

        return role_arr

    def get_role_by_uid(self, roles):
        role_arr = []
        if roles:
            for role in roles:
                if ',' in role:
                    role1_id = role.split(',')[0]
                    role_id = role.split(',')[-1]
                    role1_rec = MRole.get_by_uid(role1_id)
                    role_rec = MRole.get_by_uid(role_id)
                    if role_rec:
                        role_name = role_rec.name + ' [' + role1_rec.name + '] '
                    else:
                        role_name = ''
                else:
                    role_rec = MRole.get_by_uid(role)
                    if role_rec:
                        role_name = role_rec.name
                    else:
                        role_name = ''

                role_arr.append(role_name)

        return role_arr

    @privilege.permission(action='assign_role')
    def delete_user(self, user_id):
        '''
        delete user by ID.
        '''
        del_recs = MStaff2Role.query_by_staff(user_id)
        for del_rec in del_recs:
            MStaff2Role.remove_relation(del_rec.staff, del_rec.role)

        if MUser.delete(user_id):
            output = {"ok": True, "status": 0, "msg": "删除用户成功"}
        else:
            output = {"ok": False, "status": 404, "msg": "删除用户失败"}

        return json.dump(output, self, ensure_ascii=False)

    @privilege.permission(action='assign_group')
    @tornado.web.authenticated
    def batch_delete(self, del_id):
        '''
        Delete a link by id.
        '''

        del_uids = del_id.split(",")
        for user_id in del_uids:
            del_recs = MStaff2Role.query_by_staff(user_id)
            for del_rec in del_recs:
                MStaff2Role.remove_relation(del_rec.staff, del_rec.role)

            if MUser.delete(user_id):
                output = {"ok": True, "status": 0, "msg": "删除用户成功"}
            else:
                output = {"ok": False, "status": 404, "msg": "删除用户失败"}

        return json.dump(output, self, ensure_ascii=False)
