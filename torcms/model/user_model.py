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
    def __init__(self):
        super(MUser, self).__init__()

    @staticmethod
    def query_all(limit=50):
        '''
        Return some of the records. Not all.
        :param limit:
        :return:
        '''
        return TabMember.select().limit(limit)

    @staticmethod
    def get_by_uid(uid):
        try:
            return TabMember.get(TabMember.uid == uid)
        except:
            return None

    @staticmethod
    def get_by_name(uname):
        try:
            return TabMember.get(user_name=uname)
        except:
            return None

    @staticmethod
    def set_sendemail_time(uid):
        entry = TabMember.update(
            time_email=tools.timestamp(),
        ).where(TabMember.uid == uid)
        entry.execute()

    @staticmethod
    def get_by_email(useremail):
        try:
            return TabMember.get(user_email=useremail)
        except:
            return None

    @staticmethod
    def check_user(user_id, u_pass):
        tt = TabMember.select().where(TabMember.uid == user_id).count()
        if tt == 0:
            return -1
        a = TabMember.get(uid=user_id)
        if a.user_pass == tools.md5(u_pass):
            return 1
        return 0

    @staticmethod
    def check_user_by_name(user_id, u_pass):
        tt = TabMember.select().where(TabMember.user_name == user_id).count()
        if tt == 0:
            return -1
        a = TabMember.get(user_name=user_id)
        if a.user_pass == tools.md5(u_pass):
            return 1
        return 0

    @staticmethod
    def update_pass(user_id, newpass):

        out_dic = {'success': False, 'code': '00'}

        entry = TabMember.update(user_pass=tools.md5(newpass)).where(TabMember.uid == user_id)
        entry.execute()

        out_dic['success'] = True

        return out_dic

    @staticmethod
    def query_nologin():
        time_now = tools.timestamp()
        # num * month * hours * minite * second
        return TabMember.select().where(((time_now - TabMember.time_login) > 3 * 30 * 24 * 60 * 60) & (
            (time_now - TabMember.time_email) > 4 * 30 * 24 * 60 * 60))

    @staticmethod
    def update_info(user_id, newemail):

        out_dic = {'success': False, 'code': '00'}
        if tools.check_email_valid(newemail):
            pass
        else:
            out_dic['code'] = '21'
            return out_dic

        entry = TabMember.update(user_email=newemail).where(TabMember.uid == user_id)
        entry.execute()

        out_dic['success'] = True

        return out_dic

    @staticmethod
    def update_time_reset_passwd(uname, timeit):

        entry = TabMember.update(
            time_reset_passwd=timeit,
        ).where(TabMember.user_name == uname)
        try:

            entry.execute()
            return True
        except:
            return False

    @staticmethod
    def update_role(u_name, newprivilege):
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
        entry = TabMember.update(
            time_login=tools.timestamp()
        ).where(TabMember.user_name == u_name)
        entry.execute()

    @staticmethod
    def create_user(post_data):
        out_dic = {'success': False, 'code': '00'}

        if tools.check_username_valid(post_data['user_name']):
            pass
        else:
            out_dic['code'] = '11'
            return out_dic

        if tools.check_email_valid(post_data['user_email']):
            pass
        else:
            out_dic['code'] = '21'
            return out_dic

        if 'role' in post_data:
            role = post_data['role']
        else:
            role = '1000'

        TabMember.create(uid=tools.get_uuid(),
                         user_name=post_data['user_name'],
                         user_pass=tools.md5(post_data['user_pass']),
                         user_email=post_data['user_email'],
                         role=role,
                         time_create=tools.timestamp(),
                         time_update=tools.timestamp(),
                         time_reset_passwd=tools.timestamp(),
                         time_login=tools.timestamp(),
                         time_email=tools.timestamp())

        out_dic['success'] = True
        return out_dic

    @staticmethod
    def get_by_keyword(par2):
        return TabMember.select().where(TabMember.user_name.contains(par2))

    @staticmethod
    def delete_by_user_name(user_name):
        try:
            del_count = TabMember.delete().where(TabMember.user_name == user_name)
            del_count.execute()
            return True
        except:
            return False

    @staticmethod
    def delete(del_id):
        try:
            del_count = TabMember.delete().where(TabMember.uid == del_id)
            del_count.execute()
            return True
        except:
            return False
