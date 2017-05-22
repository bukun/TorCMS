# -*- coding:utf-8 -*-

import peewee

from torcms.core.base_model import BaseModel
from config import DB_CFG

if DB_CFG['kind'] == 'p':
    from playhouse.postgres_ext import BinaryJSONField


class TabTag(BaseModel):
    uid = peewee.CharField(null=False, max_length=4, index=True,
                           unique=True, primary_key=True, help_text='', )
    slug = peewee.CharField(null=False, index=True, unique=True, max_length=36, help_text='', )
    name = peewee.CharField(null=False, max_length=255, help_text='', )
    order = peewee.IntegerField()
    count = peewee.IntegerField(default=0)
    kind = peewee.CharField(null=False, max_length=1,
                            default='z', help_text='4 - f for category. g -  for tags', )
    # 'xxxx' for unkonw, 'zzzz' for tag.
    pid = peewee.CharField(null=False, max_length=4, default='xxxx', help_text='parent id')
    tmpl = peewee.IntegerField(null=False, default='9', help_text='tmplate type')


class TabLink(BaseModel):
    uid = peewee.CharField(null=False, index=False, unique=True, primary_key=True, default='0000',
                           max_length=4, help_text='', )
    link = peewee.CharField(null=False, max_length=36, help_text='', )
    name = peewee.CharField(null=False, max_length=255, help_text='', )
    logo = peewee.CharField(null=False, max_length=255, help_text='', )
    order = peewee.IntegerField()


class TabPost(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True, primary_key=True, default='00000',
                           max_length=5, help_text='', )
    title = peewee.CharField(null=False, help_text='Title')
    keywords = peewee.CharField(null=False, default='', help_text='Keywords')
    date = peewee.DateTimeField(null=False, help_text='')
    time_create = peewee.IntegerField()
    user_name = peewee.CharField(null=False, default='', max_length=36, help_text='UserName', )
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()
    logo = peewee.CharField(default='')
    order = peewee.CharField(null=False, default='', max_length=8)
    valid = peewee.IntegerField(null=False, default=1, help_text='Whether the infor would show.')
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    kind = peewee.CharField(null=False, max_length=1,
                            default='1', help_text='Post type: 1 for doc, 2 for inor', )

    if DB_CFG['kind'] == 'p':
        extinfo = BinaryJSONField(default={})
    else:
        pass
    rating = peewee.FloatField(null=False, default=5)


class TabWiki(BaseModel):
    # slug for page, and '_12345678' for wiki.
    uid = peewee.CharField(null=False, index=True,
                           unique=True, primary_key=True, max_length=36, help_text='', )
    title = peewee.CharField(null=False, unique=True, index=True, help_text='Title')
    date = peewee.DateTimeField()
    time_create = peewee.IntegerField()
    user_name = peewee.CharField(null=False, max_length=36, help_text='UserName', )
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    kind = peewee.CharField(null=False, max_length=1,
                            default='1', help_text='1 for wiki, 2 for page.', )


class TabPostHist(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True,
                           help_text='', primary_key=True, max_length=36)
    title = peewee.CharField(null=False, max_length=255, help_text='', )
    post_id = peewee.CharField(null=False, max_length=5, help_text='', )
    user_name = peewee.CharField()
    cnt_md = peewee.TextField()
    time_update = peewee.IntegerField()
    logo = peewee.CharField()


class TabWikiHist(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True,
                           help_text='', primary_key=True, max_length=36)
    title = peewee.CharField(null=False, max_length=255, help_text='', )
    wiki_id = peewee.CharField(null=False, max_length=36, help_text='', )
    user_name = peewee.CharField()
    cnt_md = peewee.TextField()
    time_update = peewee.IntegerField()


class TabMember(BaseModel):
    '''
    role:  the index and value should not greater than 3.
    "0123"
    read,add,edit,delete,manage
    [0]: for wiki, and post editing.
    [1]: post create, and management.
    [2]: keep
    [3]: keep
    And, could be extended.
    The Value:
    0: for view
    1: for basic editing
    2: for management
    3:
    '''
    uid = peewee.CharField(null=False, index=True, unique=True,
                           primary_key=True, max_length=36, help_text='', )
    user_name = peewee.CharField(null=False, index=True,
                                 unique=True, max_length=16, help_text='User Name', )
    user_email = peewee.CharField(null=False, unique=True,
                                  max_length=255, help_text='User Email', )
    user_pass = peewee.CharField(null=False, max_length=255,
                                 help_text='User Password')
    role = peewee.CharField(null=False, default='1000',
                            help_text='Member Privilege', max_length='4')
    time_reset_passwd = peewee.IntegerField(null=False, default=0)
    time_login = peewee.IntegerField(null=False, default=0)
    time_create = peewee.IntegerField(null=False, default=0)
    time_update = peewee.IntegerField(null=False, default=0)
    time_email = peewee.IntegerField(null=False, default=0, help_text='Time auto send email.')


class TabEntity(BaseModel):
    uid = peewee.CharField(null=False, index=True,
                           unique=True, primary_key=True, max_length=36, )
    path = peewee.CharField(null=False, unique=True,
                            max_length=255, help_text='', )
    time_create = peewee.IntegerField()
    kind = peewee.CharField(null=False,
                            max_length=1,
                            default='1',
                            help_text='1 for image', )


class TabPost2Tag(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True,
                           primary_key=True, max_length=36, help_text='', )
    tag_id = peewee.CharField(null=False, max_length=4, help_text='', )
    post_id = peewee.CharField(null=False, max_length=5, help_text='', )
    order = peewee.IntegerField()


class TabReply(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True,
                           primary_key=True, max_length=36, help_text='', )
    post_id = peewee.CharField(null=False, index=True, max_length=5, help_text='', )
    user_id = peewee.CharField(null=False, index=True, max_length=36, help_text='', )
    user_name = peewee.TextField()
    timestamp = peewee.IntegerField()
    date = peewee.DateTimeField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    vote = peewee.IntegerField()


class TabUser2Reply(BaseModel):
    uid = peewee.CharField(null=False, index=True, unique=True,
                           primary_key=True, max_length=36, help_text='', )
    reply_id = peewee.CharField(null=False, index=True, max_length=36, help_text='', )
    user_id = peewee.CharField(null=False, index=True, max_length=36, help_text='', )
    timestamp = peewee.IntegerField()


class TabCollect(BaseModel):
    '''
    用户收藏
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    post_id = peewee.CharField(null=False, max_length=5, help_text='', )
    user_id = peewee.CharField(null=False, index=True, max_length=36, help_text='', )
    timestamp = peewee.IntegerField()


class TabEvaluation(BaseModel):
    '''
    用户评价
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    post_id = peewee.CharField(null=False, max_length=5, help_text='', )
    user_id = peewee.CharField(null=False, index=True, max_length=36, help_text='', )
    value = peewee.IntegerField()  # 用户评价， 1 或 0, 作为计数


class TabRating(BaseModel):
    '''
    Rating for App of each user.
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    user_id = peewee.CharField(null=False, index=True, max_length=36, help_text='', )
    post_id = peewee.CharField(null=False, index=True, max_length=5, help_text='', )
    rating = peewee.FloatField(null=False, )
    timestamp = peewee.IntegerField(null=False)


class TabUsage(BaseModel):
    '''
    Posts accessed by user.
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    post_id = peewee.CharField(null=False, max_length=5, help_text='', )
    user_id = peewee.CharField(null=False, index=True, max_length=36, help_text='', )
    count = peewee.IntegerField()
    tag_id = peewee.CharField(null=False, max_length=4, help_text='', )
    kind = peewee.CharField(null=False, max_length=1)
    timestamp = peewee.IntegerField()


class TabRel(BaseModel):
    '''
    相关应用
    我们认为，相关性，并非是对称操作
    '''
    uid = peewee.CharField(max_length=36, null=False, unique=True, help_text='', primary_key=True)
    post_f_id = peewee.CharField(null=False, max_length=5, help_text='', )
    post_t_id = peewee.CharField(null=False, max_length=5, help_text='', )
    count = peewee.IntegerField()
