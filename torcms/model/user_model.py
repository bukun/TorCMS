# -*- coding:utf-8 -*-
'''
Model for user.
'''
import time

from config import CMS_CFG
from torcms.core import tools
from torcms.model.core_tab import TabMember
from torcms.model.staff2role_model import MStaff2Role
from torcms.model.abc_model import MHelper


class MUser:
    '''
    Model for user.
    '''

    @staticmethod
    def query_all(limit=50):
        '''
        Return some of the records. Not all.
        '''
        return TabMember.select().order_by(TabMember.time_create.desc()).limit(limit)

    @staticmethod
    def get_by_uid(uid):
        '''
        Get the user's info by user ID.
        '''
        try:
            return TabMember.get(TabMember.uid == uid)
        except Exception as err:
            print(repr(err))
            return None

    @staticmethod
    def get_by_name(uname):
        '''
        Get user by user_name.
        '''
        try:
            return TabMember.get(user_name=uname)
        except Exception as err:
            print(repr(err))
            return None

    @staticmethod
    def set_sendemail_time(uid):
        '''
        Set the time that send E-mail to user.
        '''
        entry = TabMember.update(
            time_email=tools.timestamp(),
        ).where(TabMember.uid == uid)
        entry.execute()

    @staticmethod
    def get_by_email(useremail):
        '''
        Get User info by user's email.
        '''
        try:
            return TabMember.get(user_email=useremail)
        except Exception as err:
            print(repr(err))
            return None

    @staticmethod
    def check_user(user_id, u_pass):
        '''
        Checking the password by user's ID.
        '''
        user_count = TabMember.select().where(TabMember.uid == user_id).count()
        if user_count == 0:
            return -1
        the_user = TabMember.get(uid=user_id)
        if the_user.user_pass == tools.md5(u_pass):
            return 1
        return 0

    @staticmethod
    def check_user_by_name(user_name, u_pass):
        '''
        Checking the password by user's name.

        1: for success
        0: for failure
        2: for forbidden.
        -1: for no user
        '''
        the_query = TabMember.select().where(TabMember.user_name == user_name)
        if the_query.count() == 0:
            return -1

        the_user = the_query.get()
        failed_times = the_user.failed_times
        time_failed = the_user.time_failed
        c_tiemstamp = tools.timestamp()

        # 测试是否限制登录
        if c_tiemstamp - time_failed > 1 * 60 * 60:
            # 如果距离上次登录失败超过1小时，则重置
            # Set the failed times to 0.
            entry2 = TabMember.update(failed_times=0).where(
                TabMember.user_name == user_name
            )
            try:
                entry2.execute()
            except Exception as err:
                print(repr(err))
        elif failed_times > 4:
            return 2
        else:
            pass

        if the_user.user_pass == tools.md5(u_pass):
            return 1
        return 0

    # @staticmethod
    # def check_user_by_email(user_email, u_pass):
    #     '''
    #     Checking the password by user's email.
    #     '''
    #
    #     the_query = TabMember.select().where(
    #         TabMember.user_email == user_email)
    #     if the_query.count() == 0:
    #         return -1
    #
    #     the_user = the_query.get()
    #     if the_user.user_pass == tools.md5(u_pass):
    #         return 1
    #     return 0

    @staticmethod
    def update_pass(user_id, newpass):
        '''
        Update the password of a user.
        '''

        out_dic = {'success': False, 'code': '00'}

        entry = TabMember.update(user_pass=tools.md5(newpass)).where(
            TabMember.uid == user_id
        )
        entry.execute()

        out_dic['success'] = True

        return out_dic

    @staticmethod
    def update_user_name(user_email, user_name):
        '''
        Update the user_name of a user.
        '''

        out_dic = {'success': False, 'code': '00'}

        entry = TabMember.update(user_name=user_name).where(
            TabMember.user_email == user_email
        )
        entry.execute()

        out_dic['success'] = True

        return out_dic

    @staticmethod
    def query_nologin():
        '''
        Query the users who do not login recently (90 days).
        and not send email (120 days).
        time_model: num * month * hours * minite * second
        time_login: 3 * 30 * 24 * 60 * 60
        time_email: 4 * 30 * 24 * 60 * 60
        '''
        time_now = tools.timestamp()
        return TabMember.select().where(
            ((time_now - TabMember.time_login) > 7776000)
            & ((time_now - TabMember.time_email) > 10368000)
        )

    @staticmethod
    def update_info(user_id, newemail, extinfo=None):
        '''
        Update the user info by user_id.
        21: standsfor invalide E-mail.
        91: standsfor unkown reson.
        '''

        if extinfo is None:
            extinfo = {}

        out_dic = {'success': False, 'code': '00'}
        if not tools.check_email_valid(newemail):
            out_dic['code'] = '21'
            return out_dic
        cur_info = MUser.get_by_uid(user_id)
        cur_extinfo = cur_info.extinfo
        for key in extinfo:
            cur_extinfo[key] = extinfo[key]

        try:
            entry = TabMember.update(user_email=newemail, extinfo=cur_extinfo).where(
                TabMember.uid == user_id
            )
            entry.execute()
            out_dic['success'] = True
        except Exception as err:
            print(repr(err))
            out_dic['code'] = '91'

        return out_dic

    @staticmethod
    def update_extinfo(user_id, extinfo):

        out_dic = {'success': False, 'code': '00'}
        print("-" * 50)
        print(extinfo)
        cur_info = MUser.get_by_uid(user_id)
        cur_extinfo = cur_info.extinfo
        for key in extinfo:
            cur_extinfo[key] = extinfo[key]

        try:
            entry = TabMember.update(extinfo=cur_extinfo).where(
                TabMember.uid == user_id
            )
            entry.execute()
            out_dic['success'] = True
        except Exception as err:
            print(repr(err))
            out_dic['code'] = '91'

        return out_dic

    @staticmethod
    def update_time_reset_passwd(user_name, the_time):
        '''
        Update the time when user reset passwd.
        '''
        entry = TabMember.update(
            time_reset_passwd=the_time,
        ).where(TabMember.user_name == user_name)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def update_failed_info(user_name):
        '''
        Update the time when user reset passwd.
        '''

        # First: get the user.
        recs = TabMember.select().where(TabMember.user_name == user_name)

        if recs:
            rec = recs.get()
            old_time = rec.failed_times
        else:
            return False

        #  Second: upate failed times.
        entry = TabMember.update(failed_times=old_time + 1).where(
            TabMember.user_name == user_name
        )
        try:
            entry.execute()
            # return True
        except Exception as err:
            print(repr(err))
            return False

        # Third: Set timestamp that failed.
        entry2 = TabMember.update(time_failed=tools.timestamp()).where(
            TabMember.user_name == user_name
        )
        try:
            entry2.execute()

        except Exception as err:
            print(repr(err))
            return False
        return True

    @staticmethod
    def update_role(u_name, postdata):
        '''
        Update the role of the usr.
        '''
        role = postdata['role']
        authority = postdata.get('authority', '0')
        entry = TabMember.update(role=role, authority=authority).where(
            TabMember.user_name == u_name
        )
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def update_permissions(u_name):
        '''
        更新用户权限
        '''
        userinfo = MUser.get_by_name(u_name)
        cur_extinfo = userinfo.extinfo

        # 已有权限置 0
        for key in cur_extinfo:
            if key.startswith('_per_'):
                cur_extinfo[key] = 0
        perms = MStaff2Role.query_permissions(userinfo.uid)
        # 重新分配权限
        for key in perms:
            print("-" * 50)
            print(key)
            print(key['permission'])
            cur_extinfo[f"_per_{key['permission']}"] = 1

        entry = TabMember.update(extinfo=cur_extinfo).where(
            TabMember.uid == userinfo.uid
        )
        entry.execute()

    @staticmethod
    def update_success_info(u_name):
        '''
        Update the login time for user.
        '''
        # Update permisson

        # cur_info = MUser.get_by_uid(user_id)
        # cur_extinfo = cur_info.extinfo
        # for key in extinfo:
        #     cur_extinfo[key] = extinfo[key]

        MUser.update_permissions(u_name)

        # First, record the time that logged in.
        entry = TabMember.update(time_login=tools.timestamp()).where(
            TabMember.user_name == u_name
        )
        entry.execute()

        # Second , set the failed times to 0.
        entry2 = TabMember.update(failed_times=0).where(TabMember.user_name == u_name)
        try:
            entry2.execute()
        except Exception as err:
            print(repr(err))
            return False
        return True

    @staticmethod
    def create_user(post_data, extinfo=None):
        '''
        post_data = {
        'user_name': 'tester',
        'user_pass': 'Gg12345678',
        'user_email': 'tester@qq.com',
        'role': '3300'
        }
        Create the user.
        The code used if `False`.
        11: invalid username.
        21: invalide E-mail.
        31: E-mail exists..
        91: unkown reason.
        '''
        out_dic = {'success': False, 'code': '00'}

        if post_data['user_name'].startswith('_'):
            '''
            the user_name startwith with ``_``, ONLY used for inner, not for login.
            '''
            pass
        elif not tools.check_username_valid(post_data['user_name']):

            out_dic['code'] = '11'
            return out_dic

        if not tools.check_email_valid(post_data['user_email']):
            out_dic['code'] = '21'
            return out_dic

        if not tools.check_pass_valid(post_data['user_pass']):
            out_dic['code'] = '41'
            return out_dic

        if MUser.get_by_email(post_data['user_email']):
            out_dic['code'] = '31'
            out_dic['uid'] = MUser.get_by_email(post_data['user_email']).uid
            return out_dic

        if extinfo is None:
            extinfo = {}

        try:
            uid = tools.get_uuid()
            TabMember.create(
                uid=uid,
                user_name=post_data['user_name'],
                user_pass=tools.md5(post_data['user_pass']),
                user_email=post_data['user_email'],
                role=post_data.get('role', '1000'),  # ‘1000' as default role.
                is_active=post_data.get('is_active', 0),
                is_staff=post_data.get('is_staff', 0),
                time_create=tools.timestamp(),
                time_update=tools.timestamp(),
                time_reset_passwd=tools.timestamp(),
                time_login=tools.timestamp(),
                time_email=tools.timestamp(),
                extinfo=extinfo,
            )

            out_dic['success'] = True
            out_dic['uid'] = uid

        except Exception as err:
            print(repr(err))
            out_dic['code'] = '91'
        return out_dic

    @staticmethod
    def get_by_keyword(par2):
        '''
        Get Member by keyword
        '''

        return TabMember.select().where(TabMember.user_name.contains(par2))

    @staticmethod
    def get_by_Email(par2):
        '''
        Get Member by keyword
        '''
        return TabMember.select().where(TabMember.user_email.contains(par2))

    @staticmethod
    def delete_by_user_name(user_name):
        '''
        Delete user in the database by `user_name`.
        '''
        try:
            del_count = TabMember.delete().where(TabMember.user_name == user_name)
            del_count.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def delete(user_id):
        '''
        Delele the  user in the database by `user_id`.
        '''

        staff_recs = MStaff2Role.query_by_staff(user_id)
        for staff_rec in staff_recs:
            MStaff2Role.remove_relation(user_id, staff_rec.role)

        return MHelper.delete(TabMember, user_id)

    @staticmethod
    def total_number():
        '''
        Return the number of certian slug.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return TabMember.select().count(None)

    @staticmethod
    def query_pager_by_slug(current_page_num=1, type='', num=CMS_CFG['list_num']):
        '''
        Query pager
        '''
        if type:

            return (
                TabMember.select()
                .where(TabMember.extinfo['ext_type'] == type)
                .order_by(TabMember.time_create.desc())
                .paginate(current_page_num, num)
            )
        else:
            return TabMember.select().paginate(current_page_num, num)

    @staticmethod
    def query_by_time(recent=90):
        '''
        Return some of the records. Not all.
        '''
        time_that = int(time.time()) - recent * 24 * 3600

        return (
            TabMember.select()
            .where(TabMember.time_create > time_that)
            .order_by(TabMember.time_create.desc())
        )

    @staticmethod
    def query_pager_by_time(current_page_num=1):
        '''
        Query pager
        '''
        return (
            TabMember.select()
            .where(TabMember.time_create)
            .paginate(current_page_num, CMS_CFG['list_num'])
        )

    @staticmethod
    def count_of_certain(type=''):
        ''' '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        if type:
            return (
                TabMember.select()
                .where(TabMember.extinfo['ext_type'] == type)
                .count(None)
            )
        else:
            return TabMember.select().count(None)

    @staticmethod
    def has_perm(user_id, kind='', action=''):
        '''
        检查在APP中是否有某权限
        '''
        userinfo = MUser.get_by_uid(user_id)
        if userinfo and userinfo.is_stuff():
            pass
        else:
            return False

        return False

    @staticmethod
    def has_perms(user_id, kind='', actions=[]):
        '''
        检查在APP中是否有某一些权限
        '''
        userinfo = MUser.get_by_uid(user_id)
        if userinfo and userinfo.is_stuff():
            pass
        else:
            return False

        return False

    @staticmethod
    def assign_role(user_id, role_id):
        userinfo = MUser.get_by_uid(user_id)
        if userinfo and userinfo.is_stuff():
            MStaff2Role.add_or_update(user_id, role_id)
        else:
            return False

        return False


if __name__ == '__main__':
    post_data = {
        'user_name': 'xx_tester',
        'user_pass': 'Gg12345678',
        'user_email': 'tester@qq.com',
        'role': '3300',
    }
    info = MUser.create_user(post_data, extinfo={})
    print(info)

    info = MUser.get_by_name(post_data['user_name'])
    print(info)
    print(info.is_staff)
    print(info.role)

    print(f'Delete: {info.user_name}')
    MUser.delete(info.uid)
