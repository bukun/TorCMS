# -*- coding:utf-8 -*-


from torcms.model.core_tab import TabStaff2Role


class MRole2Permission():
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
            (TabStaff2Role.role == role_id) & (TabStaff2Role.staff == staff_id))
        entry.execute()

    @staticmethod
    def add_or_update(staff_id, role_id):

        record = TabStaff2Role.select().where(
            (TabStaff2Role.staff == staff_id)
            & (TabStaff2Role.role == role_id)
        )

        if record.count() > 0:
            pass
        else:
            TabStaff2Role.create(
                role=role_id,
                staff=staff_id
            )
