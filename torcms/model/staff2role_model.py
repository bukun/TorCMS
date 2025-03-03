# -*- coding:utf-8 -*-

from peewee import JOIN

from torcms.model.core_tab import TabMember, TabRole, TabRole2Permission, TabStaff2Role

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
    def get_role_by_uid(staff_id):
        query = (
            TabStaff2Role.select(TabRole.uid, TabRole.name, TabRole.status, TabRole.pid)
            .join(TabRole, JOIN.INNER)
            .switch(TabStaff2Role)
            .join(TabMember, JOIN.INNER)
            .where(TabStaff2Role.staff == staff_id)
        )
        # query = TabStaff2Role.select(
        #     ).where(TabStaff2Role.staff == staff_id)

        if query.count() > 0:
            return query.dicts()
        else:
            return None

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
                TabStaff2Role.id,
                TabRole.uid,
                TabRole2Permission.permission_id,
                TabRole.name,
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
        record = TabStaff2Role.select().where(
            (TabStaff2Role.staff == staff_id) & (TabStaff2Role.role == role_id)
        )

        if record.count() > 0:
            pass

        else:
            TabStaff2Role.create(role=role_id, staff=staff_id)
