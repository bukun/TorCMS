'''
审核流程，参考：
https://segmentfault.com/a/1190000019161083
'''

import peewee

from torcms.core.base_model import BaseModel
from torcms.model.core_tab import TabPost, TabMember

from config import CMS_CFG
from torcms.core import tools
from torcms.model.abc_model import MHelper
from torcms.model.core_tab import TabLog


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


class MProcess:
    def __init__(self):
        try:
            TabProcess.create_table()
        except Exception as err:
            print(repr(err))

    def create(self, id, name):
        TabProcess.create(uid=id, name=name)

    def create_or_update(self, id, name):
        tt = TabProcess.select().where(TabProcess.uid == id)
        print(tt.count())
        if tt.count():
            pass
        else:
            pass
            # self.create(id, name)


class MState:
    def __init__(self):
        try:
            TabState.create_table()
        except Exception as err:
            print(repr(err))


    def create(self, info):
        uid = tools.get_uuid()
        '''
        process = peewee.ForeignKeyField(TabProcess, backref='process', help_text='')
        name = peewee.CharField(null=False, index=True, unique=True, max_length=255, help_text='名称')
        state_type = peewee.CharField(null=False, index=True, unique=True, max_length=255, help_text='名称')
        description = peewee.TextField()
        '''
        TabState.create(
            uid=uid,
            process='1',
            name=info['name'],
            state_type=info['state_type'],
            description='',
        )

    def create_or_update(self, info):
        tt = TabState.select().where(TabState.state_type == info['state_type'])
        if tt.count() > 0:
            print('got')
            pass
        else:
            self.create(info)

    def query_all(self):
        return TabState.select()


if __name__ == '__main__':
    uu = MState()
    tt = MProcess()
    tt.create_or_update('1', 'Post')

    state_arr = [
        ['started', '开始'],
        ['denied', '回退'],
        ['complated', '完成'],
        ['cancceled', '取消'],
    ]

    for statinfo in state_arr:
        info = {'state_type': statinfo[0], 'name': statinfo[1]}
        uu.create_or_update(info)
    all_state = uu.query_all().dicts()
    [print(x) for x in all_state]
