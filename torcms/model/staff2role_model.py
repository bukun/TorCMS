# -*- coding:utf-8 -*-

from peewee import JOIN
from torcms.model.core_tab import TabStaff2Role, TabRole, TabRole2Permission, TabMember


# from torcms.model.user_model import MUser


class MStaff2Role:
    @staticmethod
    def query_all():
        '''
        Return some of the records. Not all.
        '''
        return TabStaff2Role.select()

    @staticmethod
    def query_by_staff(staff_id):
        '''
        Query records by staff.
        '''
        return TabStaff2Role.select().where(TabStaff2Role.staff == staff_id)

    @staticmethod
    def query_permissions(staff_id):
        '''
        Query records by staff.
        '''
        # return TabStaff2Role.select().where(TabStaff2Role.staff == staff_id)

        # query = (User
        #          .select(User.username, fn.COUNT(Favorite.id).alias('count'))
        #          .join(Tweet, JOIN.LEFT_OUTER)  # Joins user -> tweet.
        #          .join(Favorite, JOIN.LEFT_OUTER)  # Joins tweet -> favorite.
        #          .group_by(User.username))

        query = (
            TabStaff2Role.select(
                TabStaff2Role.id, TabRole.uid, TabRole2Permission.permission_id
            )
            .join(TabRole, JOIN.LEFT_OUTER)
            .join(TabRole2Permission, JOIN.LEFT_OUTER)
            .where(TabStaff2Role.staff == staff_id)
        )
        return query.dicts()

    @staticmethod
    def check_permissions(staff_id, action):
        '''
        Query records by staff.
        '''
        # return TabStaff2Role.select().where(TabStaff2Role.staff == staff_id)

        # query = (User
        #          .select(User.username, fn.COUNT(Favorite.id).alias('count'))
        #          .join(Tweet, JOIN.LEFT_OUTER)  # Joins user -> tweet.
        #          .join(Favorite, JOIN.LEFT_OUTER)  # Joins tweet -> favorite.
        #          .group_by(User.username))
        userinfo = TabMember.get(uid=staff_id)
        if userinfo.is_staff:
            pass
        else:
            return False

        query = (
            TabStaff2Role.select(
                TabStaff2Role.id, TabRole.uid, TabRole2Permission.permission_id
            )
            .join(TabRole, JOIN.LEFT_OUTER)
            .join(TabRole2Permission, JOIN.LEFT_OUTER)
            .where(
                (TabStaff2Role.staff == staff_id)
                & (TabRole2Permission.permission_id == action)
            )
        )
        if query and query.count() > 0:
            return True
        return False

    @staticmethod
    def query_by_role(role_id):
        '''
        Query records by role.
        '''
        return TabStaff2Role.select().where(TabStaff2Role.role == role_id)

    @staticmethod
    def remove_relation(staff_id, role_id):
        '''
        Delete the record of Staff 2 Role.
        '''
        entry = TabStaff2Role.delete().where(
            (TabStaff2Role.role == role_id) & (TabStaff2Role.staff == staff_id)
        )
        entry.execute()

    @staticmethod
    def add_or_update(staff_id, role_id):
        print('aa')
        record = TabStaff2Role.select().where(
            (TabStaff2Role.staff == staff_id) & (TabStaff2Role.role == role_id)
        )
        print('bb')

        if record.count() > 0:
            print('cc')
            pass

        else:
            print('dd')
            TabStaff2Role.create(role=role_id, staff=staff_id)


if __name__ == '__main__':
    # uid = 'a99c7bfd-c4b5-11ed-bd91-f58b67e41619'
    userinfo = TabMember.get(user_name='user_1role5')
    print(userinfo.user_name)
    print(userinfo.extinfo)
    uid = userinfo.uid
    uu = MStaff2Role.query_permissions(uid)
    for x in uu:
        print(x)
        # print(x.id, x.tabuser.uid , dir(x))

    tt = MStaff2Role.check_permissions(uid, '1can_add')
    tt = MStaff2Role.check_permissions(uid, '1can_af')
    print(tt)
