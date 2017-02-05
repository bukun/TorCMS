# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.core_tab import g_Member
from torcms.model.abc_model import Mabc


class MUser(Mabc):
    def __init__(self):
        try:
            g_Member.create_table()
        except:
            pass

    @staticmethod
    def query_all(limit=50):
        '''
        Return some of the records. Not all.
        :param limit:
        :return:
        '''
        return g_Member.select().limit(limit)

    @staticmethod
    def get_by_uid(uid):
        try:
            return g_Member.get(g_Member.uid == uid)
        except:
            return None

    @staticmethod
    def get_by_name(uname):
        try:
            return g_Member.get(user_name=uname)
        except:
            return None

    @staticmethod
    def set_sendemail_time(uid):
        entry = g_Member.update(
            time_email=tools.timestamp(),
        ).where(g_Member.uid == uid)
        entry.execute()

    @staticmethod
    def get_by_email(useremail):
        try:
            return g_Member.get(user_email=useremail)
        except:
            return None

    @staticmethod
    def check_user(u_name, u_pass):
        tt = g_Member.select().where(g_Member.user_name == u_name).count()
        if tt == 0:
            return -1
        a = g_Member.get(user_name=u_name)
        if a.user_pass == tools.md5(u_pass):
            return 1
        return 0

    @staticmethod
    def update_pass(u_name, newpass):

        out_dic = {'success': False, 'code': '00'}

        entry = g_Member.update(user_pass=tools.md5(newpass)).where(g_Member.user_name == u_name)
        entry.execute()

        out_dic['success'] = True

        return out_dic

    @staticmethod
    def query_nologin():
        time_now = tools.timestamp()
        # num * month * hours * minite * second
        return g_Member.select().where(((time_now - g_Member.time_login) > 3 * 30 * 24 * 60 * 60) & (
            (time_now - g_Member.time_email) > 4 * 30 * 24 * 60 * 60))

    @staticmethod
    def update_info(u_name, newemail):

        out_dic = {'success': False, 'code': '00'}
        if tools.check_email_valid(newemail):
            pass
        else:
            out_dic['code'] = '21'
            return out_dic

        entry = g_Member.update(user_email=newemail).where(g_Member.user_name == u_name)
        entry.execute()

        out_dic['success'] = True

        return out_dic

    @staticmethod
    def update_time_reset_passwd(uname, timeit):
        entry = g_Member.update(
            time_reset_passwd=timeit,
        ).where(g_Member.user_name == uname)
        try:
            entry.execute()
            return True
        except:
            return False

    @staticmethod
    def update_role(u_name, newprivilege):
        entry = g_Member.update(
            role=newprivilege
        ).where(g_Member.user_name == u_name)
        try:
            entry.execute()
            return True
        except:
            return False

    @staticmethod
    def update_time_login(u_name):
        entry = g_Member.update(
            time_login=tools.timestamp()
        ).where(g_Member.user_name == u_name)
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

        g_Member.create(uid=tools.get_uuid(),
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
        return g_Member.select().where(g_Member.user_name.contains(par2))

    @staticmethod
    def delete_by_user_name(user_name):
        try:
            del_count = g_Member.delete().where(g_Member.user_name == user_name)
            del_count.execute()
            return True
        except:
            return False

    @staticmethod
    def delete(del_id):
        try:
            del_count = g_Member.delete().where(g_Member.uid == del_id)
            del_count.execute()
            return True
        except:
            return False
