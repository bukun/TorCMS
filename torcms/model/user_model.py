# -*- coding:utf-8 -*-

'''
Model for user.
'''

from torcms.core import tools
from torcms.model.core_tab import TabMember
from torcms.model.abc_model import Mabc


class MUser(Mabc):
    '''
    Model for user.
    '''

    @staticmethod
    def query_all(limit=50):
        '''
        Return some of the records. Not all.
        '''
        return TabMember.select().limit(limit)

    @staticmethod
    def get_by_uid(uid):
        '''
        Get the user's info by user ID.
        '''
        try:
            return TabMember.get(TabMember.uid == uid)
        except:
            return None

    @staticmethod
    def get_by_name(uname):
        '''
        Get user by user_name.
        '''
        try:
            return TabMember.get(user_name=uname)
        except:
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
        except:
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
        '''
        the_query = TabMember.select().where(TabMember.user_name == user_name)
        if the_query.count() == 0:
            return -1

        the_user = the_query.get()
        if the_user.user_pass == tools.md5(u_pass):
            return 1
        return 0

    @staticmethod
    def update_pass(user_id, newpass):
        '''
        Update the password of a user.
        '''

        out_dic = {'success': False, 'code': '00'}

        entry = TabMember.update(user_pass=tools.md5(newpass)).where(TabMember.uid == user_id)
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
            entry = TabMember.update(
                user_email=newemail,
                extinfo=cur_extinfo
            ).where(
                TabMember.uid == user_id
            )
            entry.execute()

            out_dic['success'] = True
        except:
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
        except:
            return False

    @staticmethod
    def update_role(u_name, newprivilege):
        '''
        Update the role of the usr.
        '''
        entry = TabMember.update(
            role=newprivilege
        ).where(TabMember.user_name == u_name)
        try:
            entry.execute()
            return True
        except:
            return False

    @staticmethod
    def update_time_login(u_name):
        '''
        Update the login time for user.
        '''
        entry = TabMember.update(
            time_login=tools.timestamp()
        ).where(
            TabMember.user_name == u_name
        )
        entry.execute()

    @staticmethod
    def create_user(post_data):
        '''
        Create the user.
        The code used if `False`.
        11: standsfor invalid username.
        21: standsfor invalide E-mail.
        91: standsfor unkown reson.
        '''
        out_dic = {'success': False, 'code': '00'}

        if not tools.check_username_valid(post_data['user_name']):
            out_dic['code'] = '11'
            return out_dic

        if not tools.check_email_valid(post_data['user_email']):
            out_dic['code'] = '21'
            return out_dic

        try:
            TabMember.create(uid=tools.get_uuid(),
                             user_name=post_data['user_name'],
                             user_pass=tools.md5(post_data['user_pass']),
                             user_email=post_data['user_email'],
                             # role=post_data.get('role', '1000'),
                             role='1000',  # ‘1000' as default role.
                             time_create=tools.timestamp(),
                             time_update=tools.timestamp(),
                             time_reset_passwd=tools.timestamp(),
                             time_login=tools.timestamp(),
                             time_email=tools.timestamp())

            out_dic['success'] = True
        except:
            out_dic['code'] = '91'
        return out_dic

    @staticmethod
    def get_by_keyword(par2):
        '''
        Get Member by keyword
        '''
        return TabMember.select().where(TabMember.user_name.contains(par2))

    @staticmethod
    def delete_by_user_name(user_name):
        '''
        Delete user in the database by `user_name`.
        '''
        try:
            del_count = TabMember.delete().where(TabMember.user_name == user_name)
            del_count.execute()
            return True
        except:
            return False

    @staticmethod
    def delete(user_id):
        '''
        Delele the  user in the database by `user_id`.
        '''
        try:
            del_count = TabMember.delete().where(TabMember.uid == user_id)
            del_count.execute()
            return True
        except:
            return False
