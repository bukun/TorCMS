# -*- coding:utf-8 -*-
'''
For friends links.
'''
from torcms.model.abc_model import MHelper
from torcms.model.process_model import TabState, TabProcess, TabTransition, TabRequest, TabAction, TabRequestAction, \
    TabTransitionAction
from torcms.model.core_tab import TabMember, TabPost
from peewee import JOIN
from torcms.core import tools


class MTransitionAction:

    @staticmethod
    def create(transition_id, action_id):
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
    def query_all():
        return TabTransitionAction.select()


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
    def query_all():
        return TabProcess.select()


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
            return rec
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def query_all():
        return TabTransition.select()

    @staticmethod
    def query_by_proid(pro_id):
        return TabTransition.select().where(TabTransition.process == pro_id)

    @staticmethod
    def query_by_state(state):
        query = (
            TabTransition.select(TabTransition.uid)
            .join(TabState, JOIN.INNER)
            .where(TabState.name == state)
        )
        return query.dicts()


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
    def update_by_action(action_id, is_active, is_complete):

        try:

            TabRequestAction.update(
                is_active=is_active,
                is_complete=is_complete
            ).where(TabRequestAction.request == action_id)
            return True
        except Exception as err:
            print(repr(err))
            return False

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
            TabRequest.select(TabRequest.uid)
            .join(TabPost, JOIN.INNER)
            .switch(TabRequest)
            .join(TabMember, JOIN.INNER)
            .where((TabMember.user_name == user_name) & (TabPost.uid == post_id))
        )
        return query.get()


class MAction:

    @staticmethod
    def create(pro_id, action, action_arr):

        try:
            rec = MAction.query_by_name(action.get('name'))
            if rec.count() > 0:
                pass
            else:
                uid = tools.get_uuid()
                TabAction.create(
                    uid=uid,
                    process=pro_id,
                    name=action.get('name'),
                    action_type=action.get('action_type'),
                    description=action.get('description')
                )
                action_arr.append(uid)
            return action_arr
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
    def query_by_proid(pro_id):
        return TabAction.select().where(TabAction.process == pro_id)


class MState:
    '''
    For friends links.
    '''

    @staticmethod
    def get_counts():
        '''
        The count in table.
        '''
        # adding ``None`` to hide ``No value for argument 'database' in method call``
        return TabState.select().count(None)

    @staticmethod
    def query_all_parger(current_page_num, perPage):
        '''
        Return some of the records. Not all.
        '''
        return TabState.select().paginate(current_page_num, perPage)

    @staticmethod
    def query_by_pro_id(pro_id):
        '''
        Get a link by ID.
        '''
        return TabState.select().where(TabState.process == pro_id)

    @staticmethod
    def query_by_name(state_name):
        '''
        Get a link by ID.
        '''
        res = TabState.select().where(TabState.name == state_name)
        return res.uid

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
    def update_action(uid, post_data):
        '''
        Updat the link.
        '''
        raw_rec = TabState.get(TabState.uid == uid)
        entry = TabState.update(
            controller=post_data.get('controller', raw_rec.controller),
            action=post_data.get('action', raw_rec.action),
        ).where(TabState.uid == uid)
        try:
            entry.execute()
            return True
        except Exception as err:
            print(repr(err))
            return False

    @staticmethod
    def create(post_data, state_arr):
        '''
        Add record in permission.
        '''
        try:

            uid = tools.get_uuid()
            name = post_data.get('name')
            TabState.create(
                uid=uid,
                process=post_data.get('process'),
                name=name,
                state_type=post_data.get('state_type'),
                description=post_data.get('description')
            )

            state_arr[name] = uid
            return state_arr
        except Exception as err:
            print(repr(err))
            return False
