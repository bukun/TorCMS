'''
审核流程，参考：
https://segmentfault.com/a/1190000019161083
'''

import peewee
from torcms.core.base_model import BaseModel
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabMember, TabPost, TabRole, TabPermission
from peewee import JOIN
from torcms.core import tools


class TabProcess(BaseModel):
    '''
    流程
    '''

    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    name = peewee.CharField(
        null=False, index=True, unique=True, max_length=255, help_text='名称'
    )


class TabState(BaseModel):
    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    process = peewee.ForeignKeyField(TabProcess, backref='process', help_text='')
    name = peewee.CharField(
        null=False, index=True, max_length=255, help_text='名称'
    )
    state_type = peewee.CharField(
        null=False, index=True, unique=True, max_length=255, help_text='名称'
    )
    description = peewee.TextField()


class TabTransition(BaseModel):
    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    process = peewee.ForeignKeyField(TabProcess, backref='process', help_text='')
    current_state = peewee.ForeignKeyField(
        TabState, backref='current_state', help_text=''
    )
    next_state = peewee.ForeignKeyField(TabState, backref='next_state', help_text='')


class TabAction(BaseModel):
    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    process = peewee.ForeignKeyField(TabProcess, backref='process', help_text='')
    action_type = peewee.CharField(
        null=False, index=True, unique=True, max_length=255, help_text='名称'
    )
    name = peewee.CharField(
        null=False, index=True, max_length=255, help_text='名称'
    )
    description = peewee.TextField()


class TabPermissionAction(BaseModel):
    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    permission = peewee.ForeignKeyField(TabPermission, backref='permission', help_text='')
    action = peewee.ForeignKeyField(TabAction, backref='action', help_text='')


class TabTransitionAction(BaseModel):
    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    transition = peewee.ForeignKeyField(TabTransition, backref='transition', help_text='')
    action = peewee.ForeignKeyField(TabAction, backref='action', help_text='')


class TabRequest(BaseModel):
    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    process = peewee.ForeignKeyField(TabProcess, backref='process', help_text='')
    current_state = peewee.ForeignKeyField(TabState, backref='cur_state', help_text='')
    post = peewee.ForeignKeyField(TabPost, backref='post')
    user = peewee.ForeignKeyField(TabMember, backref='user')
    time_create = peewee.IntegerField()


class TabRequestAction(BaseModel):
    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    request = peewee.ForeignKeyField(TabRequest, backref='request', help_text='')
    action = peewee.ForeignKeyField(TabAction, backref='action', help_text='')
    transition = peewee.ForeignKeyField(
        TabTransition, backref='transition', help_text=''
    )
    is_active = peewee.BooleanField(null=False, default=False)
    is_complete = peewee.BooleanField(null=False, default=False)


class MTransitionAction:

    @staticmethod
    def create(transition_id, action_id):
        rec = MTransitionAction.get_by_trans_act(transition_id, action_id)
        if rec.count() > 0:
            return False
        else:

            try:
                uid = tools.get_uuid()
                TabTransitionAction.create(
                    uid=uid,
                    transition=transition_id,
                    action=action_id
                )
                return uid
            except Exception as err:
                print(repr(err))
                return False

    @staticmethod
    def update(transition_id, action_id):

        entry = TabTransitionAction.update(
            transition=transition_id

        ).where(TabTransitionAction.action == action_id)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def get_by_trans_act(trans_id, act_id):
        return TabTransitionAction.select().where(
            (TabTransitionAction.transition == trans_id) &
            (TabTransitionAction.action == act_id))

    @staticmethod
    def get_by_trans(trans_id):
        return TabTransitionAction.select().where(TabTransitionAction.transition == trans_id)

    @staticmethod
    def get_by_uid(uid):
        '''
        Get a link by ID.
        '''
        return TabTransitionAction.select().where(TabTransitionAction.uid == uid)

    @staticmethod
    def query_by_actid(act_id):
        return TabTransitionAction.select().where(TabTransitionAction.action == act_id)

    @staticmethod
    def query_all():
        return TabTransitionAction.select()

    @staticmethod
    def query_by_pro_state(pro_id, state_id):
        query = (
            TabTransitionAction.select(
                TabTransitionAction.transition, TabTransitionAction.action)
            .join(TabTransition, JOIN.INNER)
            .where((TabTransition.process == pro_id) & (
                    TabTransition.current_state == state_id))
        )
        return query.dicts()

    @staticmethod
    def query_by_process(pro_id):
        query = (
            TabTransitionAction.select(TabAction.uid, TabAction.name, TabTransitionAction.transition)
            .join(TabTransition, JOIN.INNER)
            .switch(TabTransition)
            .join(TabProcess, JOIN.INNER)
            .switch(TabTransitionAction)
            .join(TabAction)
            .where(TabTransition.process == pro_id)
        )
        return query.dicts()

    @staticmethod
    def delete_by_actid(action_id):
        entry = TabTransitionAction.delete().where(
            TabTransitionAction.action == action_id
        )
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def delete_by_trans(trans_id):
        entry = TabTransitionAction.delete().where(
            TabTransitionAction.transition == trans_id
        )

        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def remove_relation(trans_id, act_id):
        entry = TabTransitionAction.delete().where(
            (TabTransitionAction.transition == trans_id) & (
                    TabTransitionAction.action == act_id)
        )

        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False


class MProcess:

    @staticmethod
    def create(name):
        try:
            uid = tools.get_uuid()
            TabProcess.create(uid=uid, name=name)
            return uid
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def get_by_name(name):
        '''
        Get a link by name.
        '''
        return TabProcess.select().where(TabProcess.name == name)

    @staticmethod
    def get_by_uid(uid):
        '''
        Get a link by ID.
        '''
        return TabProcess.select().where(TabProcess.uid == uid)

    @staticmethod
    def query_all():
        return TabProcess.select()

    @staticmethod
    def query_all_parger(current_page_num, perPage):
        return MHelper.query_all_parger(TabProcess, current_page_num, perPage)

    @staticmethod
    def get_counts():
        '''
        The count in table.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return MHelper.get_counts(TabProcess)

    @staticmethod
    def update(uid, post_data):
        '''
        Updat the link.
        '''
        raw_rec = TabProcess.get(TabProcess.uid == uid)
        entry = TabProcess.update(
            name=post_data.get('name', raw_rec.name)

        ).where(TabProcess.uid == uid)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def delete_by_uid(uid):
        entry = TabProcess.delete().where(
            TabProcess.uid == uid
        )
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False


class MTransition:

    @staticmethod
    def create(pro_id, cur_state, next_state):
        try:
            uid = tools.get_uuid()
            rec = TabTransition.create(
                uid=uid,
                process=pro_id,
                current_state=cur_state,
                next_state=next_state
            )
            return rec.uid
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def query_all():
        return TabTransition.select()

    @staticmethod
    def query_by_action(action_id, pro_id):
        query = (
            TabTransition.select(TabTransition.uid, TabTransition.current_state, TabTransition.next_state)
            .join(TabTransitionAction, JOIN.INNER)
            .where((TabTransitionAction.action == action_id) & (
                    TabTransition.process == pro_id))

        )
        if query.count() > 0:
            return query
        else:
            return None

    @staticmethod
    def query_by_proid(pro_id):
        return TabTransition.select().where(TabTransition.process == pro_id)

    @staticmethod
    def get_by_uid(uid):
        '''
        Get a link by ID.
        '''
        return TabTransition.select().where(TabTransition.uid == uid)

    @staticmethod
    def get_by_cur_next(pro_id, cur_state, next_state):
        return TabTransition.select().where(
            (TabTransition.process == pro_id) &
            (TabTransition.current_state == cur_state) &
            (TabTransition.next_state == next_state)
        )

    @staticmethod
    def query_by_proid_state(pro_id, state_id):
        return TabTransition.select().where(
            (TabTransition.process == pro_id) &
            (TabTransition.current_state == state_id))

    @staticmethod
    def query_by_state(state):
        query = (
            TabTransition.select(TabTransition.uid)
            .join(TabState, JOIN.INNER)
            .where(TabState.name == state)
        )
        return query.dicts()

    @staticmethod
    def delete_by_state(state_id):
        recs1 = TabTransition.select().where(TabTransition.next_state == state_id
                                             )
        recs2 = TabTransition.select().where(TabTransition.current_state == state_id)
        for rec in recs1:

            tran_acts = MTransitionAction.get_by_trans(rec.uid)

            for tract in tran_acts:
                try:
                    MPermissionAction.delete_by_action(tract.action)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass

                try:
                    MRequestAction.delete_by_trans(rec.uid)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass

                try:
                    MTransitionAction.delete_by_trans(tract.transition)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass

                try:
                    MAction.delete(tract.action)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass

            entry = TabTransition.delete().where(TabTransition.uid == rec.uid)
            try:
                entry.execute()
                pass
            except Exception as err:
                print(repr(err))
                pass
        for rec in recs2:

            tran_acts = MTransitionAction.get_by_trans(rec.uid)

            for tract in tran_acts:
                try:
                    MPermissionAction.delete_by_action(tract.action)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass

                try:
                    MRequestAction.delete_by_trans(rec.uid)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass

                try:
                    MTransitionAction.delete_by_trans(tract.transition)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass

                try:
                    MAction.delete(tract.action)
                    pass
                except Exception as err:
                    print(repr(err))
                    pass

            entry = TabTransition.delete().where(TabTransition.uid == rec.uid)
            try:
                entry.execute()
                pass
            except Exception as err:
                print(repr(err))
                pass

        # try:
        MRequest.delete_by_state(state_id)
        # pass
        # except Exception as err:
        #     print(repr(err))
        #     pass

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''
        return MHelper.delete(TabTransition, uid)

    @staticmethod
    def query_all_parger(current_page_num, perPage):
        return MHelper.query_all_parger(TabTransition, current_page_num, perPage)

    @staticmethod
    def get_counts():
        '''
        The count in table.
        '''
        return MHelper.get_counts(TabTransition)


class MRequestAction:

    @staticmethod
    def create(request_id, action_id, transition_id):

        try:

            uid = tools.get_uuid()
            TabRequestAction.create(
                uid=uid,
                request=request_id,
                action=action_id,
                transition=transition_id,
                is_active=True,
                is_complete=False
            )
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def query_all():
        return TabRequestAction.select()

    @staticmethod
    def update_by_request(request_id):

        entry = TabRequestAction.update(
            is_active=False
        ).where(TabRequestAction.request == request_id)

        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def update_by_action(action_id, request_id):

        entry = TabRequestAction.update(
            is_active=False,
            is_complete=True
        ).where((TabRequestAction.request == request_id) & (
                TabRequestAction.action == action_id))

        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def update_by_action_reqs(action_id, request_id):

        entry = TabRequestAction.update(
            is_active=False
        ).where((TabRequestAction.request == request_id) & (
                TabRequestAction.action != action_id))

        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def query_by_request_trans(request_id, trans_id):
        rec = TabRequestAction.select().where(
            (TabRequestAction.request == request_id) &
            (TabRequestAction.transition == trans_id))
        if rec.count() > 0:
            return rec.get()
        else:
            return None

    @staticmethod
    def get_by_action_request(act_id, request_id):
        rec = TabRequestAction.select().where(
            (TabRequestAction.action == act_id) &
            (TabRequestAction.request == request_id))
        if rec.count() > 0:
            return rec.get()
        else:
            return None

    @staticmethod
    def delete_by_actid(action_id):
        entry = TabRequestAction.delete().where(
            TabRequestAction.action == action_id
        )
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def delete_by_trans(trans_id):
        entry = TabRequestAction.delete().where(
            TabRequestAction.transition == trans_id
        )

        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False


class MRequest:

    @staticmethod
    def create(pro_id, post_id, user_id, cur_state_id):
        try:
            uid = tools.get_uuid()
            TabRequest.create(
                uid=uid,
                process=pro_id,
                post=post_id,
                user=user_id,
                current_state=cur_state_id,
                time_create=tools.timestamp()
            )
            return uid
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def query_all():
        return TabRequest.select()

    @staticmethod
    def query_by_postid(post_id):
        recs = TabRequest.select().where(TabRequest.post == post_id).order_by(TabRequest.time_create.desc())
        if recs.count() > 0:
            return recs.get()
        else:
            return None

    @staticmethod
    def get_by_pro_state(pro_id, state_id):

        query = (
            TabRequest.select()

            .where((TabRequest.process == pro_id) & (TabRequest.current_state == state_id))
        )
        if query.count() > 0:
            return query.get()
        else:
            return None

    @staticmethod
    def get_by_pro(pro_id):

        query = TabRequest.select().where(TabRequest.process == pro_id).order_by(TabRequest.time_create.desc())

        if query.count() > 0:
            return query
        else:
            return None

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''
        return MHelper.delete(TabRequest, uid)

    @staticmethod
    def delete_by_state(state_id):
        entry = TabRequest.delete().where(
            TabRequest.current_state == state_id
        )

        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False


class MPermissionAction:
    @staticmethod
    def create(per, action):

        try:
            uid = tools.get_uuid()
            TabPermissionAction.create(
                uid=uid,
                permission=per,
                action=action
            )
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def query_by_permission(permission_id):
        query = (
            TabPermissionAction.select(TabAction.uid, TabAction.name, TabPermissionAction.permission)
            .join(TabAction, JOIN.INNER)
            .where(TabPermissionAction.permission == permission_id)
        )
        return query.dicts()

    @staticmethod
    def query_per_by_action(act_id):
        query = (
            TabPermissionAction.select(TabPermission.uid, TabPermission.name)
            .join(TabPermission, JOIN.INNER)
            .switch(TabPermissionAction)
            .join(TabAction, JOIN.INNER)
            .where(TabPermissionAction.action == act_id)
        )
        return query.dicts()

    @staticmethod
    def query_by_action(act_id):

        return TabPermissionAction.select().where(TabPermissionAction.action == act_id)

    @staticmethod
    def query_all():
        return TabPermissionAction.select()

    @staticmethod
    def remove_relation(act_id, per_id):
        '''
        Delete the record of Role 2 Permission.
        '''
        entry = TabPermissionAction.delete().where(
            (TabPermissionAction.action == act_id)
            & (TabPermissionAction.permission == per_id)
        )
        entry.execute()

    @staticmethod
    def delete_by_action(act_id):
        entry = TabPermissionAction.delete().where(
            TabPermissionAction.action == act_id
        )
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False


class MAction:

    @staticmethod
    def create(pro_id, action):

        try:
            uid = tools.get_uuid()
            TabAction.create(
                uid=uid,
                process=pro_id,
                name=action.get('name'),
                action_type=action.get('action_type') + '_' + pro_id,
                description=action.get('description')
            )

            return uid
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def update(uid, post_data):
        '''
        Updat the link.
        '''
        raw_rec = TabAction.get(TabAction.uid == uid)
        entry = TabAction.update(
            process=post_data.get('process', raw_rec.process),
            name=post_data.get('name', raw_rec.name),
            action_type=post_data.get('action_type', raw_rec.action_type),
            description=post_data.get('description', raw_rec.description)

        ).where(TabAction.uid == uid)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def query_by_trans(trans_id):
        query = (
            TabAction.select()
            .join(TabTransitionAction, JOIN.INNER)
            .where(TabTransitionAction.transition == trans_id)
        )
        return query.dicts()

    @staticmethod
    def update_process(process, uid):
        '''
        Updat the link.
        '''

        entry = TabAction.update(
            process=process

        ).where(TabAction.uid == uid)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def query_all():
        return TabAction.select()

    @staticmethod
    def get_by_name(name):
        return TabAction.select().where(TabAction.name == name)

    @staticmethod
    def get_by_action_type(action_type):
        rec = TabAction.select().where(TabAction.action_type == action_type)
        if rec.count() > 0:
            return rec.get()
        else:
            return None

    @staticmethod
    def get_by_id(uid):
        return TabAction.select().where(TabAction.uid == uid)

    @staticmethod
    def query_by_proid(pro_id):
        return TabAction.select().where(TabAction.process == pro_id)

    @staticmethod
    def get_by_pro_actname(pro_id, act_name):
        return TabAction.select().where(
            (TabAction.process == pro_id) & (TabAction.name == act_name))

    @staticmethod
    def get_by_pro_act(pro_id, act_id):
        return TabAction.select().where(
            (TabAction.process == pro_id) & (TabAction.uid == act_id))

    @staticmethod
    def get_counts():
        '''
        The count in table.
        '''

        return MHelper.get_counts(TabAction)

    @staticmethod
    def query_all_parger(current_page_num, perPage):
        '''
        Return some of the records. Not all.
        '''
        return MHelper.query_all_parger(TabAction, current_page_num, perPage)

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''
        return MHelper.delete(TabAction, uid)


class MState:
    '''
    For friends links.
    '''

    @staticmethod
    def get_counts():
        '''
        The count in table.
        '''

        return MHelper.get_counts(TabState)

    @staticmethod
    def query_all_parger(current_page_num, perPage):
        '''
        Return some of the records. Not all.
        '''
        return MHelper.query_all_parger(TabState, current_page_num, perPage)

    @staticmethod
    def query_by_pro_id(pro_id):
        '''
        Get a link by ID.
        '''
        return TabState.select().where(TabState.process == pro_id)

    @staticmethod
    def get_by_pro_statename(pro_id, name):
        '''
        Get a link by ID.
        '''
        return TabState.select().where(
            (TabState.process == pro_id) & (TabState.name == name))

    @staticmethod
    def get_by_uid(uid):
        '''
        Get a link by ID.
        '''
        return TabState.select().where(TabState.uid == uid)

    @staticmethod
    def get_by_name(state_name):
        '''
        Get a link by ID.
        '''
        res = TabState.select().where(TabState.name == state_name)
        return res

    @staticmethod
    def get_by_state_type(state_type):
        '''
        Get a link by ID.
        '''
        res = TabState.select().where(TabState.state_type == state_type)
        if res.count() > 0:
            return res.get()
        else:
            return None

    @staticmethod
    def query_all():
        '''
        Get a link by ID.
        '''
        return TabState.select()

    @staticmethod
    def delete(uid):
        '''
        Delete by uid
        '''
        return MHelper.delete(TabState, uid)

    @staticmethod
    def update(uid, post_data):
        '''
        Updat the link.
        '''
        raw_rec = TabState.get(TabState.uid == uid)
        entry = TabState.update(
            process=post_data.get('process', raw_rec.process),
            name=post_data.get('name', raw_rec.name),
            state_type=post_data.get('state_type', raw_rec.state_type),
            description=post_data.get('description', raw_rec.description)

        ).where(TabState.uid == uid)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def update_process(uid, post_data):
        '''
        Updat the link.
        '''
        raw_rec = TabState.get(TabState.uid == uid)
        entry = TabState.update(
            process=post_data.get('process', raw_rec.process),
        ).where(TabState.uid == uid)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def create(post_data):
        '''
        Add record in permission.
        '''

        try:

            uid = tools.get_uuid()

            TabState.create(
                uid=uid,
                process=post_data.get('process'),
                name=post_data.get('name'),
                state_type=str(post_data.get('state_type')) + '_' + str(post_data.get('process')),
                description=post_data.get('description', '')
            )

            return uid
        except Exception as err:
            print(repr(err))
            return False
