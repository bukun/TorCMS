# -*- coding:utf-8 -*-
'''
Define the schema of Tables in TorCMS.
'''

import peewee
from playhouse.postgres_ext import BinaryJSONField

from torcms.core.base_model import BaseModel


class TabTag(BaseModel):
    uid = peewee.CharField(
        null=False,
        max_length=4,
        index=True,
        unique=True,
        primary_key=True,
        help_text='',
    )

    slug = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        max_length=36,
        help_text='',
    )
    name = peewee.CharField(
        null=False,
        max_length=255,
        help_text='',
    )
    order = peewee.IntegerField()
    count = peewee.IntegerField(default=0)
    kind = peewee.CharField(
        null=False,
        max_length=1,
        default='z',
        help_text='4 - f for category. g -  for tags',
    )
    # 'xxxx' for unkonw, 'zzzz' for tag.
    pid = peewee.CharField(null=False,
                           max_length=4,
                           default='xxxx',
                           help_text='parent id')
    tmpl = peewee.IntegerField(null=False,
                               default='9',
                               help_text='tmplate type')


class TabLink(BaseModel):
    uid = peewee.CharField(
        null=False,
        index=False,
        unique=True,
        primary_key=True,
        default='0000',
        max_length=4,
        help_text='',
    )
    link = peewee.CharField(
        null=False,
        max_length=36,
        help_text='',
    )
    name = peewee.CharField(
        null=False,
        max_length=255,
        help_text='',
    )
    logo = peewee.CharField(
        null=False,
        max_length=255,
        help_text='',
    )
    order = peewee.IntegerField()


class TabPost(BaseModel):
    uid = peewee.TextField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        default='00000',
        help_text='',
    )
    title = peewee.CharField(null=False, help_text='Title')
    keywords = peewee.CharField(null=False, default='', help_text='Keywords')
    date = peewee.DateTimeField(null=False, help_text='')
    time_create = peewee.IntegerField()
    user_name = peewee.CharField(
        null=False,
        default='',
        max_length=36,
        help_text='UserName',
    )
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField(default=0)

    access_1d = peewee.IntegerField(default=0, help_text='24小时内阅读量')
    access_7d = peewee.IntegerField(default=0, help_text='7*24小时内阅读量')
    access_30d = peewee.IntegerField(default=0, help_text='30*24小时内阅读量')

    logo = peewee.CharField(default='')
    order = peewee.CharField(null=False, default='', max_length=8)
    valid = peewee.IntegerField(null=False,
                                default=1,
                                help_text='Whether the infor would show.')
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    kind = peewee.CharField(
        null=False,
        max_length=1,
        default='1',
        help_text='Post type. According to the user defined.',
    )
    state = peewee.CharField(null=False,
                             max_length=4,
                             default='0000',
                             help_text='state for post. 发布/审核状态.')
    rating = peewee.FloatField(null=False,
                               default=5,
                               help_text='Rating of the post.')
    memo = peewee.TextField(
        null=False,
        default='',
        help_text='Memo',
    )
    extinfo = BinaryJSONField(null=False,
                              default={},
                              help_text='Extra data in JSON.')


class TabWiki(BaseModel):
    # slug for page, and '_12345678' for wiki.
    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    title = peewee.CharField(null=False,
                             unique=True,
                             index=True,
                             help_text='Title')
    date = peewee.DateTimeField()
    time_create = peewee.IntegerField()
    user_name = peewee.CharField(
        null=False,
        max_length=36,
        help_text='UserName',
    )
    time_update = peewee.IntegerField()
    view_count = peewee.IntegerField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    kind = peewee.CharField(
        null=False,
        max_length=1,
        default='1',
        help_text='1 for wiki, 2 for page.',
    )


class TabPostHist(BaseModel):
    '''
    Table for post history.
    '''
    uid = peewee.CharField(null=False,
                           index=True,
                           unique=True,
                           help_text='',
                           primary_key=True,
                           max_length=36)
    title = peewee.CharField(
        null=False,
        max_length=255,
        help_text='',
    )
    post_id = peewee.TextField(
        null=False,
        help_text='',
    )
    user_name = peewee.CharField()
    cnt_md = peewee.TextField()
    time_update = peewee.IntegerField()
    logo = peewee.CharField()


class TabWikiHist(BaseModel):
    '''
    Table for wiki history.
    '''
    uid = peewee.CharField(null=False,
                           index=True,
                           unique=True,
                           help_text='',
                           primary_key=True,
                           max_length=36)
    title = peewee.CharField(
        null=False,
        max_length=255,
        help_text='',
    )
    wiki_id = peewee.CharField(
        null=False,
        max_length=36,
        help_text='',
    )
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
    uid = peewee.CharField(null=False,
                           index=True,
                           unique=True,
                           primary_key=True,
                           max_length=36,
                           help_text='')
    user_name = peewee.CharField(null=False,
                                 index=True,
                                 unique=True,
                                 max_length=255,
                                 help_text='User Name')
    user_email = peewee.CharField(null=False,
                                  unique=True,
                                  max_length=255,
                                  help_text='User Email')
    user_pass = peewee.CharField(null=False,
                                 max_length=255,
                                 help_text='User Password')
    role = peewee.CharField(null=False,
                            default='1000',
                            help_text='Member Privilege',
                            max_length='4')
    '''
    进行审核的权限，与 role 配合使用。
    role 声明是否有权限，    authority 声明对哪些 post 有权限。
    post 权限类型由二进制的 '1', '10', '100', '1000', ... 声明 ，成员的 authority 则根据二进制相加的结果来声明多种 post 的审核权限
    '''
    authority = peewee.CharField(null=False,
                            default='0',
                            help_text='Member authority for checking',
                            max_length='8')
    time_reset_passwd = peewee.IntegerField(null=False, default=0)
    time_login = peewee.IntegerField(null=False, default=0)
    time_create = peewee.IntegerField(null=False, default=0)
    time_update = peewee.IntegerField(null=False, default=0)
    time_email = peewee.IntegerField(null=False,
                                     default=0,
                                     help_text='Time auto send email.')
    failed_times = peewee.IntegerField(null=False, default=0, help_text='record the times for trying login.')
    time_failed = peewee.IntegerField(null=False, default=0, help_text='timestamp for login failed.')
    extinfo = BinaryJSONField(null=False,
                              default={},
                              help_text='Extra data in JSON.')


class TabEntity(BaseModel):
    '''
    Table to store the entity information.
    '''
    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
    )
    path = peewee.CharField(
        null=False,
        unique=True,
        max_length=255,
        help_text='',
    )
    desc = peewee.CharField(null=False,
                            default='',
                            max_length=255,
                            help_text='')
    time_create = peewee.IntegerField()
    kind = peewee.CharField(
        null=False,
        max_length=1,
        default='1',
        help_text='1 for image',
    )


class TabPost2Tag(BaseModel):
    '''
    Table of tag to the post.
    '''
    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    par_id = peewee.CharField(null=False,
                              default='',
                              max_length=4,
                              help_text='父类id，对于label，top_id为""')
    tag_id = peewee.CharField(
        null=False,
        max_length=4,
        help_text='',
    )
    post_id = peewee.TextField(
        null=False,
        help_text='',
    )
    order = peewee.IntegerField()


class TabReply(BaseModel):
    '''
    Table of the reply to the post.
    '''
    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    post_id = peewee.TextField(
        null=False,
        index=True,
        help_text='',
    )
    user_id = peewee.CharField(
        null=False,
        index=True,
        max_length=36,
        help_text='',
    )
    user_name = peewee.TextField()
    timestamp = peewee.IntegerField()
    date = peewee.DateTimeField()
    cnt_md = peewee.TextField()
    cnt_html = peewee.TextField()
    vote = peewee.IntegerField()
    category = peewee.CharField(
        null=False,
        default='0',
        help_text='0为评论，1为回复',
    )
    extinfo = BinaryJSONField(null=False,
                              default={},
                              help_text='Extra data in JSON.')

class TabUser2Reply(BaseModel):
    '''
    Table of the reply of the user.
    '''

    uid = peewee.CharField(
        null=False,
        index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    reply_id = peewee.CharField(
        null=False,
        index=True,
        max_length=36,
        help_text='',
    )
    user_id = peewee.CharField(
        null=False,
        index=True,
        max_length=36,
        help_text='',
    )
    timestamp = peewee.IntegerField()


class TabCollect(BaseModel):
    '''
    用户收藏
    '''
    uid = peewee.CharField(max_length=36,
                           null=False,
                           unique=True,
                           help_text='',
                           primary_key=True)
    post_id = peewee.TextField(
        null=False,
        help_text='',
    )
    user_id = peewee.CharField(
        null=False,
        index=True,
        max_length=36,
        help_text='',
    )
    timestamp = peewee.IntegerField()


class TabEvaluation(BaseModel):
    '''
    用户评价
    '''
    uid = peewee.CharField(max_length=36,
                           null=False,
                           unique=True,
                           help_text='',
                           primary_key=True)
    post_id = peewee.TextField(
        null=False,
        help_text='',
    )
    user_id = peewee.CharField(
        null=False,
        index=True,
        max_length=36,
        help_text='',
    )
    value = peewee.IntegerField()  # 用户评价， 1 或 0, 作为计数


class TabRating(BaseModel):
    '''
    Rating for App of each user.
    '''
    uid = peewee.CharField(max_length=36,
                           null=False,
                           unique=True,
                           help_text='',
                           primary_key=True)
    user_id = peewee.CharField(
        null=False,
        index=True,
        max_length=36,
        help_text='',
    )
    post_id = peewee.TextField(
        null=False,
        index=True,
        help_text='',
    )
    rating = peewee.FloatField(null=False, )
    timestamp = peewee.IntegerField(null=False)


class TabUsage(BaseModel):
    '''
    记录用户访问 Post 的概括情况。
    包括数目，最后的访问时间。
    '''
    uid = peewee.CharField(max_length=36,
                           null=False,
                           unique=True,
                           help_text='',
                           primary_key=True)
    post_id = peewee.TextField(
        null=False,
        help_text='',
    )
    user_id = peewee.CharField(
        null=False,
        index=True,
        max_length=36,
        help_text='',
    )
    count = peewee.IntegerField()
    tag_id = peewee.CharField(
        null=False,
        max_length=4,
        help_text='',
    )
    kind = peewee.CharField(null=False, max_length=1)
    timestamp = peewee.IntegerField()


class TabRel(BaseModel):
    '''
    相关应用
    相关性，并非是对称操作
    '''
    uid = peewee.CharField(max_length=36,
                           null=False,
                           unique=True,
                           help_text='',
                           primary_key=True)
    post_f_id = peewee.TextField(
        null=False,
        help_text='',
    )
    post_t_id = peewee.TextField(
        null=False,
        help_text='',
    )
    count = peewee.IntegerField()


class TabCorrelation(BaseModel):
    '''
    Post之间的相关性
    `kind为`相关性的类别：
    1: 同小类
    2: 同大类
    3: 同类 (kind)
    4: 全系统
    5: 与文档
    '''
    uid = peewee.CharField(max_length=36,
                           null=False,
                           unique=True,
                           help_text='',
                           primary_key=True)
    post_id = peewee.TextField(
        null=False,
        help_text='',
    )
    rel_id = peewee.TextField(
        null=False,
        help_text='',
    )
    kind = peewee.IntegerField()
    order = peewee.IntegerField()


class TabEntity2User(BaseModel):
    '''
    The table for the entity to user.
    '''
    uid = peewee.CharField(null=False,
                           index=True,
                           unique=True,
                           primary_key=True,
                           max_length=36)
    entity_id = peewee.CharField(null=False, max_length=36, help_text='')
    user_id = peewee.CharField(null=False,
                               index=True,
                               max_length=36,
                               help_text='用户ID,未登录表示为xxxx')
    user_ip = peewee.CharField(null=False, help_text='用户端ip')
    timestamp = peewee.IntegerField(null=False)


class TabLog(BaseModel):
    '''
    用户访问行为记录
    '''
    uid = peewee.CharField(null=False,
                           index=True,
                           unique=True,
                           primary_key=True,
                           max_length=36)
    current_url = peewee.CharField(
        null=False,
        help_text='',
    )
    refer_url = peewee.CharField(
        null=False,
        help_text='',
    )
    user_id = peewee.CharField(null=False,
                               index=True,
                               max_length=36,
                               help_text='')
    time_create = peewee.BigIntegerField()
    time_out = peewee.BigIntegerField()
    time = peewee.BigIntegerField()


class TabReplyid(BaseModel):
    '''
    用户评论回复。
    '''
    uid = peewee.CharField(null=False,
                           index=False,
                           unique=True,
                           primary_key=True,
                           max_length=36,
                           help_text='')
    reply0 = peewee.CharField(null=False, max_length=36, help_text='')
    reply1 = peewee.CharField(null=False, max_length=36, help_text='')
    time_create = peewee.IntegerField()


class TabReferrer(BaseModel):
    '''
    创建 访问来源 记录表
    '''
    uid = peewee.CharField(null=False,
                           index=False,
                           unique=True,
                           primary_key=True,
                           default='00000',
                           help_text='')
    media = peewee.CharField(null=False, help_text='来源')
    terminal = peewee.CharField(null=False, help_text='终端')
    userip = peewee.CharField(null=False, unique=True, help_text='用户端ip')
    # usercity = peewee.CharField(null=False, help_text='用户端城市', )
    kind = peewee.CharField(null=False,
                            max_length=1,
                            default='1',
                            help_text='')
    time_create = peewee.IntegerField()
    time_update = peewee.IntegerField()
