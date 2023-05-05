'''
审核流程，参考：
https://segmentfault.com/a/1190000019161083
'''

import peewee
from torcms.core.base_model import BaseModel
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabMember, TabPost, TabRole
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
        null=False, index=True, unique=True, max_length=255, help_text='名称'
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
        null=False, index=True, unique=True, max_length=255, help_text='名称'
    )
    description = peewee.TextField()


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
        rec = MTransitionAction.query_by_trans_act(transition_id, action_id)
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
    def query_by_trans_act(trans_id, act_id):
        return TabTransitionAction.select().where(
            (TabTransitionAction.transition == trans_id) &
            (TabTransitionAction.action == act_id))

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
    def query_by_action_state(pro_id, state_id):
        query = (
            TabTransitionAction.select(TabTransitionAction.transition,
                                       TabTransitionAction.action)
            .join(TabTransition, JOIN.INNER)
            .where((TabTransition.process == pro_id) & (
                    TabTransition.current_state == state_id))
        )
        return query.dicts()

    @staticmethod
    def query_by_process(role_id):
        query = (
            TabTransitionAction.select(TabAction.uid, TabAction.name)
            .join(TabTransition, JOIN.INNER)
            .switch(TabTransition)
            .join(TabProcess, JOIN.INNER)
            .switch(TabTransitionAction)
            .join(TabAction)
            .where(TabTransition.process == role_id)
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
    def delete_by_trans_act(trans_id, act_id):
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
            TabTransition.select(TabTransition.current_state, TabTransition.next_state)
            .join(TabTransitionAction, JOIN.INNER)
            .where((TabTransitionAction.action == action_id) & (
                    TabTransition.process == pro_id))

        )
        return query

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
    def query_by_cur_next(pro_id, cur_state, next_state):
        return TabTransition.select().where(
            (TabTransition.process == pro_id) &
            (TabTransition.current_state == cur_state) &
            (TabTransition.next_state == next_state)
        )

    @staticmethod
    def query_by_proid_state(pro_id, state_id):
        return TabTransition.select().where(
            (TabTransition.process == pro_id) & (
                    TabTransition.current_state == state_id))

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
        entry = TabTransition.delete().where(
            (TabTransition.current_state == state_id) or (
                    TabTransition.next_state == state_id)
        )

        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

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
        return TabRequestAction.select().where(
            (TabRequestAction.request == request_id) & (
                    TabRequestAction.transition == trans_id))

    @staticmethod
    def query_by_request(req_uid):
        '''
        Get a link by ID.
        '''
        return TabRequestAction.select().where(TabRequestAction.request == req_uid)

    @staticmethod
    def query_by_action(act_id):
        return TabRequestAction.select().where(TabRequestAction.action == act_id)

    @staticmethod
    def query_by_action_request(act_id, request_id):
        return TabRequestAction.select().where(
            (TabRequestAction.action == act_id) & (
                    TabRequestAction.request == request_id))

    @staticmethod
    def query_by_postid(post_id):
        query = (
            TabRequestAction.select(TabTransition.process, TabTransition.current_state)
            .join(TabRequest, JOIN.INNER)
            .switch(TabRequestAction)
            .join(TabTransition, JOIN.INNER)
            .where((TabRequest.post == post_id) & (TabRequestAction.is_active == True))

        )
        return query.dicts()

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
    def create(pro_id, post_id, user_id):
        try:
            uid = tools.get_uuid()
            TabRequest.create(
                uid=uid,
                process=pro_id,
                post=post_id,
                user=user_id,
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
    def get_id_by_username(post_id, user_name):

        query = (
            TabRequest.select(TabRequest.uid, TabRequest.process)
            .join(TabPost, JOIN.INNER)
            .switch(TabRequest)
            .join(TabMember, JOIN.INNER)
            .where((TabMember.user_name == user_name) & (TabPost.uid == post_id))
        )
        if query.count() > 0:
            return query.get()
        else:
            return None


#
# class MStateAction:
#     @staticmethod
#     def create(state, action):
#
#         try:
#
#             uid = tools.get_uuid()
#             TabStateAction.create(
#                 uid=uid,
#                 state=state,
#                 action=action
#             )
#
#             return True
#         except Exception as err:
#             print(repr(err))
#             return False
#
#     @staticmethod
#     def query_by_state(state):
#         query = (
#             TabStateAction.select(TabAction.uid, TabAction.name, TabStateAction.state)
#             .join(TabAction, JOIN.INNER)
#             .where(TabStateAction.state == state)
#         )
#         return query.dicts()
#
#     @staticmethod
#     def query_all():
#         return TabStateAction.select()
#
#     @staticmethod
#     def delete_by_state(state_id):
#         entry = TabStateAction.delete().where(
#             TabStateAction.state == state_id
#         )
#         try:
#             entry.execute()
#             return True
#         except Exception as err:
#             print(repr(err))
#             return False
#

class MAction:

    @staticmethod
    def create(pro_id, action):
        rec = MAction.query_by_name(action.get('name'))
        if rec.count() > 0:
            return False
        else:
            try:
                uid = tools.get_uuid()
                TabAction.create(
                    uid=uid,
                    process=pro_id,
                    name=action.get('name'),
                    action_type=action.get('action_type'),
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
    def query_by_name(name):
        return TabAction.select().where(TabAction.name == name)

    @staticmethod
    def get_by_action_type(action_type):
        return TabAction.select().where(TabAction.action_type == action_type)

    @staticmethod
    def get_by_id(uid):
        return TabAction.select().where(TabAction.uid == uid)

    @staticmethod
    def query_by_proid(pro_id):
        return TabAction.select().where(TabAction.process == pro_id)

    @staticmethod
    def query_by_pro_actname(pro_id, act_name):
        return TabAction.select().where(
            (TabAction.process == pro_id) & (TabAction.name == act_name))

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
    def query_by_pro_statename(pro_id, name):
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
    def query_by_name(state_name):
        '''
        Get a link by ID.
        '''
        res = TabState.select().where(TabState.name == state_name)
        return res.get().uid

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
                state_type= post_data.get('state_type'),
                description= post_data.get('description', '')
            )

            return uid
        except Exception as err:
            print(repr(err))
            return False
