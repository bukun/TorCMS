# -*- coding:utf-8 -*-
'''
Model for user.
'''
import time

from config import CMS_CFG
from torcms.core import tools
from torcms.model.core_tab import TabStaff


class MStaff():
    '''
    Model for user.
    '''

    @staticmethod
    def query_all(limit=50):
        '''
        Return some of the records. Not all.
        '''
        return TabStaff.select().limit(limit)

    @staticmethod
    def get_by_uid(uid):
        '''
        Get the user's info by user ID.
        '''
        try:
            return TabStaff.get(TabStaff.uid == uid)
        except Exception as err:
            print(repr(err))
            return None

    @staticmethod
    def get_by_name(uname):
        '''
        Get user by name.
        '''
        try:
            return TabStaff.get(name=uname)
        except Exception as err:
            print(repr(err))
            return None

    @staticmethod
    def set_sendemail_time(uid):
        '''
        Set the time that send E-mail to user.
        '''
        entry = TabStaff.update(
            time_email=tools.timestamp(), ).where(TabStaff.uid == uid)
        entry.execute()

    @staticmethod
    def get_by_email(useremail):
        '''
        Get User info by user's email.
        '''
        try:
            return TabStaff.get(email=useremail)
        except Exception as err:
            print(repr(err))
            return None

    @staticmethod
    def check_user(user_id, u_pass):
        '''
        Checking the password by user's ID.
        '''
        user_count = TabStaff.select().where(TabStaff.uid == user_id).count()
        if user_count == 0:
            return -1
        the_user = TabStaff.get(uid=user_id)
        if the_user.passwd == tools.md5(u_pass):
            return 1
        return 0

    @staticmethod
    def check_user_by_name(name, u_pass):
        '''
        Checking the password by user's name.

        1: for success
        0: for failure
        2: for forbidden.
        -1: for no user
        '''
        the_query = TabStaff.select().where(TabStaff.name == name)
        if the_query.count() == 0:
            return -1

        the_user = the_query.get()
        failed_count = the_user.failed_times
        time_failed = the_user.time_failed
        c_tiemstamp = tools.timestamp()

        # 测试是否限制登录
        if c_tiemstamp - time_failed > 1 * 60 * 60:
            # 如果距离上次登录失败超过1小时，则重置
            # Set the failed times to 0.
            entry2 = TabStaff.update(failed_count=0).where(
                TabStaff.name == name)
            try:
                entry2.execute()
            except Exception as err:
                print(repr(err))
        elif failed_count > 4:
            return 2
        else:
            pass

        if the_user.passwd == tools.md5(u_pass):
            return 1
        return 0



    @staticmethod
    def update_pass(user_id, newpass):
        '''
        Update the password of a user.
        '''

        out_dic = {'success': False, 'code': '00'}

        entry = TabStaff.update(passwd=tools.md5(newpass)).where(
            TabStaff.uid == user_id)
        entry.execute()

        out_dic['success'] = True

        return out_dic

    @staticmethod
    def update_name(email, name):
        '''
        Update the name of a user.
        '''

        out_dic = {'success': False, 'code': '00'}

        entry = TabStaff.update(name=name).where(
            TabStaff.email == email)
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
        return TabStaff.select().where(
            ((time_now - TabStaff.time_login) > 7776000)
            & ((time_now - TabStaff.time_email) > 10368000))

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
        cur_info = MStaff.get_by_uid(user_id)
        cur_extinfo = cur_info.extinfo
        for key in extinfo:
            cur_extinfo[key] = extinfo[key]

        try:
            entry = TabStaff.update(
                email=newemail,
                extinfo=cur_extinfo).where(TabStaff.uid == user_id)
            entry.execute()

            out_dic['success'] = True
        except Exception as err:
            print(repr(err))
            out_dic['code'] = '91'

        return out_dic

    @staticmethod
    def update_time_reset_passwd(name, the_time):
        '''
        Update the time when user reset passwd.
        '''
        entry = TabStaff.update(time_reset_passwd=the_time, ).where(
            TabStaff.name == name)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def update_failed_info(name):
        '''
        Update the time when user reset passwd.
        '''

        # First: get the user.
        recs = TabStaff.select().where(TabStaff.name == name)

        if recs:
            rec = recs.get()
            old_time = rec.failed_count
        else:
            return False

        #  Second: upate failed times.
        entry = TabStaff.update(failed_count=old_time + 1).where(
            TabStaff.name == name)
        try:
            entry.execute()
            # return True
        except Exception as err:
            print(repr(err))
            return False

        # Third: Set timestamp that failed.
        entry2 = TabStaff.update(
            time_failed=tools.timestamp()
        ).where(
            TabStaff.name == name)
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
        entry = TabStaff.update(role=role, authority=authority).where(
            TabStaff.name == u_name)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def update_success_info(u_name):
        '''
        Update the login time for user.
        '''
        # First, record the time that logged in.
        entry = TabStaff.update(time_login=tools.timestamp()).where(
            TabStaff.name == u_name)
        entry.execute()

        # Second , set the failed times to 0.
        entry2 = TabStaff.update(failed_count=0).where(
            TabStaff.name == u_name)
        try:
            entry2.execute()
        except Exception as err:
            print(repr(err))
            return False
        return True

    @staticmethod
    def create_user(post_data, extinfo=None):
        '''
        Create the user.
        The code used if `False`.
        11: invalid username.
        21: invalide E-mail.
        31: E-mail exists..
        91: unkown reason.
        '''
        out_dic = {'success': False, 'code': '00'}

        if post_data['name'].startswith('_'):
            '''
            the name startwith with ``_``, ONLY used for inner, not for login.
            '''
            pass
        elif not tools.check_username_valid(post_data['name']):

            out_dic['code'] = '11'
            return out_dic

        if not tools.check_email_valid(post_data['email']):
            out_dic['code'] = '21'
            return out_dic

        if not tools.check_pass_valid(post_data['passwd']):
            out_dic['code'] = '41'
            return out_dic

        if MStaff.get_by_email(post_data['email']):
            out_dic['code'] = '31'
            return out_dic

        if extinfo is None:
            extinfo = {}

        try:
            TabStaff.create(
                uid=tools.get_uuid(),
                name=post_data['name'],
                passwd=tools.md5(post_data['passwd']),
                email=post_data['email'],
                time_create=tools.timestamp(),
                time_update=tools.timestamp(),
                time_reset_passwd=tools.timestamp(),
                time_login=tools.timestamp(),
                time_email=tools.timestamp(),
                extinfo=extinfo,
            )

            out_dic['success'] = True
        except Exception as err:
            print(repr(err))
            out_dic['code'] = '91'
        return out_dic

    @staticmethod
    def get_by_keyword(par2):
        '''
        Get Member by keyword
        '''

        return TabStaff.select().where(TabStaff.name.contains(par2))

    @staticmethod
    def get_by_Email(par2):
        '''
        Get Member by keyword
        '''
        return TabStaff.select().where(TabStaff.email.contains(par2))

    @staticmethod
    def delete_by_name(name):
        '''
        Delete user in the database by `name`.
        '''
        try:
            del_count = TabStaff.delete().where(
                TabStaff.name == name)
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
        try:
            del_count = TabStaff.delete().where(TabStaff.uid == user_id)
            del_count.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def total_number():
        '''
        Return the number of certian slug.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return TabStaff.select().count(None)

    @staticmethod
    def query_pager_by_slug(current_page_num=1, type=''):
        '''
        Query pager
        '''
        if type:

            return TabStaff.select().where(TabStaff.extinfo['ext_type'] == type).paginate(
                current_page_num, CMS_CFG['list_num'])
        else:
            return TabStaff.select().paginate(
                current_page_num, CMS_CFG['list_num'])

    @staticmethod
    def query_by_time(recent=90):
        '''
        Return some of the records. Not all.
        '''
        time_that = int(time.time()) - recent * 24 * 3600

        return TabStaff.select().where(
            TabStaff.time_create > time_that).order_by(
            TabStaff.time_create.desc())

    @staticmethod
    def query_pager_by_time(current_page_num=1):
        '''
        Query pager
        '''
        return TabStaff.select().where(TabStaff.time_create).paginate(
            current_page_num, CMS_CFG['list_num'])

    @staticmethod
    def count_of_certain(type=''):
        '''
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        if type:
            return TabStaff.select().where(TabStaff.extinfo['ext_type'] == type).count(None)
        else:
            return TabStaff.select().count(None)
