# Create your models here.
from django.db import models
# from base.models import basemodel

# Create your models here.


# -*- coding:utf-8 -*-
'''
Define the schema of Tables in TorCMS.
'''

# import models
# from playhouse.postgres_ext import BinaryJSONField

# from torcms.core.base_model import models.Model


class TabTag(models.Model):
    uid = models.CharField(
        null=False,
        max_length=4,
        # index=True,
        unique=True,
        primary_key=True,
        help_text='',
    )
    slug = models.CharField(
        null=False,
        # index=True,
        unique=True,
        max_length=36,
        help_text='',
    )
    name = models.CharField(null=False, max_length=255, help_text='')
    order = models.IntegerField()
    count = models.IntegerField(default=0)
    kind = models.CharField(
        null=False,
        max_length=1,
        default='z',
        help_text='4 - f for category. g -  for tags',
    )
    # 'xxxx' for unkonw, 'zzzz' for tag.
    pid = models.CharField(
        null=False, max_length=4, default='xxxx', help_text='parent id'
    )
    tmpl = models.IntegerField(null=False, default='9',  help_text='tmplate type')
    class Meta:
        db_table = 'tabtag'
        verbose_name = "Tags"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabLink(models.Model):
    uid = models.CharField(
        null=False,
        # index=False,
        unique=True,
        primary_key=True,
        default='0000',
        max_length=4,
        help_text='',
    )
    link = models.CharField(null=False, max_length=255, help_text='')
    name = models.CharField(null=False, max_length=255, help_text='')
    logo = models.CharField(null=False, max_length=255, help_text='')
    order = models.IntegerField()
    class Meta:
        db_table = 'tablink'
        verbose_name = "Links"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabPost(models.Model):
    uid = models.TextField(
        null=False,
        # index=True,
        unique=True,
        primary_key=True,
        default='00000',
        help_text='',
    )
    title = models.CharField(null=False,  max_length = 255,help_text='Title')
    keywords = models.CharField(null=False,  max_length = 255,default='', help_text='Keywords')
    date = models.DateTimeField(null=False,  max_length = 255,help_text='')
    time_create = models.IntegerField()
    user_name = models.CharField(
        null=False, default='', max_length=255, help_text='UserName'
    )
    time_update = models.IntegerField()
    view_count = models.IntegerField(default=0)

    access_1d = models.IntegerField(default=0, help_text='24小时内阅读量')
    access_7d = models.IntegerField(default=0, help_text='7*24小时内阅读量')
    access_30d = models.IntegerField(default=0, help_text='30*24小时内阅读量')

    logo = models.CharField(default='', max_length = 255,)
    order = models.CharField(null=False, default='', max_length=8)
    valid = models.IntegerField(
        null=False, default=1, help_text='Whether the infor would show.'
    )
    cnt_md = models.TextField()
    cnt_html = models.TextField()
    kind = models.CharField(null=False, max_length=1, default='1', help_text='app type')
    state = models.CharField(
        null=False, max_length=4, default='0000', help_text='state for post. 发布/审核状态.'
    )
    rating = models.FloatField(null=False, default=5, help_text='Rating of the post.')
    memo = models.TextField(null=False, default='', help_text='Memo')
    extinfo = models.JSONField(null=False, default={}, help_text='Extra data in JSON.')
    class Meta:
        db_table = 'tabpost'
        verbose_name = "Table Posts"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabWiki(models.Model):
    # slug for page, and '_12345678' for wiki.
    uid = models.CharField(
        null=False,
        # index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    title = models.CharField(
        null=False,
        unique=True,
        # index=True,
        help_text='Title',
        max_length=255,
    )
    date = models.DateTimeField()
    time_create = models.IntegerField()
    user_name = models.CharField(null=False, max_length=255, help_text='UserName')
    time_update = models.IntegerField()
    view_count = models.IntegerField()
    cnt_md = models.TextField()
    cnt_html = models.TextField()
    kind = models.CharField(
        null=False, max_length=1, default='1', help_text='1 for wiki, 2 for page.'
    )
    class Meta:
        db_table = 'tabwiki'
        verbose_name = "wiki"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabPostHist(models.Model):
    '''
    Table for post history.
    '''

    uid = models.CharField(
        null=False,
        # index=True,
        unique=True,
        help_text='',
        primary_key=True,
        max_length=36,
    )
    title = models.CharField(null=False, max_length=255, help_text='')
    post_id = models.TextField(null=False, help_text='')
    user_name = models.CharField( max_length = 255,)
    cnt_md = models.TextField()
    time_update = models.IntegerField()
    logo = models.CharField( max_length = 255,)
    class Meta:
        db_table = 'tabposthist'
        verbose_name = "PostHist"
        ordering = ['uid']
        verbose_name_plural = verbose_name

class TabWikiHist(models.Model):
    '''
    Table for wiki history.
    '''

    uid = models.CharField(
        null=False,
        # index=True,
        unique=True,
        help_text='',
        primary_key=True,
        max_length=36,
    )
    title = models.CharField(null=False, max_length=255, help_text='')
    wiki_id = models.CharField(null=False, max_length=36, help_text='')
    user_name = models.CharField( max_length = 255,)
    cnt_md = models.TextField()
    time_update = models.IntegerField()
    class Meta:
        db_table = 'tabwikihist'
        verbose_name = "WikiHist"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabMember(models.Model):
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

    uid = models.CharField(
        null=False,
        # index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    user_name = models.CharField(
        null=False,
       #  index=True,
        unique=True, max_length=255, help_text='User Name'
    )
    user_email = models.CharField(
        null=False, unique=True, max_length=255, help_text='User Email'
    )
    user_pass = models.CharField(null=False, max_length=255, help_text='User Password')
    is_active = models.SmallIntegerField(null=False, help_text='', default=0)
    is_staff = models.SmallIntegerField(
        null=False, help_text='if 1 then could access backend', default=0
    )
    role = models.CharField(
        null=False, default='1000', help_text='Member Privilege', max_length=4
    )
    '''
    进行审核的权限，与 role 配合使用。
    role 声明是否有权限， authority 声明对哪些 post 有权限。
    post 权限类型由二进制的 '1', '10', '100', '1000', ... 声明 ，成员的 authority 则根据二进制相加的结果来声明多种 post 的审核权限
    ToDo: 设计有问题。应该将采用RBAC进行解耦。
    '''
    authority = models.CharField(
        null=False,
        default='0',
        help_text='Member authority for checking',
        max_length=8,
    )
    time_reset_passwd = models.IntegerField(null=False, default=0)
    time_login = models.IntegerField(null=False, default=0)
    time_create = models.IntegerField(null=False, default=0)
    time_update = models.IntegerField(null=False, default=0)
    time_email = models.IntegerField(
        null=False, default=0, help_text='Time auto send email.'
    )
    failed_times = models.IntegerField(
        null=False, default=0, help_text='record the times for trying login.'
    )
    time_failed = models.IntegerField(
        null=False, default=0, help_text='timestamp for login failed.'
    )
    extinfo = models.JSONField(null=False, default={}, help_text='Extra data in JSON.')
    class Meta:
        db_table = 'tabmember'
        verbose_name = "Member"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabEntity(models.Model):
    '''
    Table to store the entity information.
    '''

    uid = models.CharField(
        null=False,
        # index=True,
        unique=True,
        primary_key=True,
        max_length=36,
    )
    path = models.CharField(null=False, unique=True, max_length=255, help_text='')
    desc = models.CharField(null=False, default='', max_length=255, help_text='')
    time_create = models.IntegerField()
    kind = models.CharField(
        null=False, max_length=1, default='1', help_text='1 for image'
    )
    class Meta:
        db_table = 'tabentity'
        verbose_name = "Entity"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabPost2Tag(models.Model):
    '''
    Table of tag to the post.
    '''

    uid = models.CharField(
        null=False,
        # index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    par_id = models.CharField(
        null=False, default='', max_length=4, help_text='父类id，对于label，top_id为""'
    )
    tag_id = models.CharField(null=False, max_length=4, help_text='')
    post_id = models.TextField(null=False, help_text='')
    order = models.IntegerField()
    class Meta:
        db_table = 'tabpost2tag'
        verbose_name = "Post2Tag"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabReply(models.Model):
    '''
    Table of the reply to the post.
    '''

    uid = models.CharField(
        null=False,
        # index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    post_id = models.TextField(null=False, help_text='')  # index=True,
    user_id = models.CharField(null=False, max_length=36, help_text='')  # index=True,
    user_name = models.TextField()
    timestamp = models.IntegerField()
    date = models.DateTimeField()
    cnt_md = models.TextField()
    cnt_html = models.TextField()
    vote = models.IntegerField()
    category = models.CharField(null=False, default='0', max_length=255, help_text='0为评论，1为回复')
    extinfo = models.JSONField(null=False, default={}, help_text='Extra data in JSON.')
    class Meta:
        db_table = 'tabreply'
        verbose_name = "Reply"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabUser2Reply(models.Model):
    '''
    Table of the reply of the user.
    '''

    uid = models.CharField(
        null=False,
        # index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    reply_id = models.CharField(null=False, max_length=36, help_text='')  # index=True,
    user_id = models.CharField(null=False, max_length=36, help_text='')  #  index=True,
    timestamp = models.IntegerField()
    class Meta:
        db_table = 'tabuser2reply'
        verbose_name = "User2Reply"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabCollect(models.Model):
    '''
    用户收藏
    '''

    uid = models.CharField(
        max_length=36, null=False, unique=True, help_text='', primary_key=True
    )
    post_id = models.TextField(null=False, help_text='')
    user_id = models.CharField(
        null=False,
        # index=True,
        max_length=36,
        help_text='',
    )
    timestamp = models.IntegerField()
    class Meta:
        db_table = 'tabcollect'
        verbose_name = "Collect"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabEvaluation(models.Model):
    '''
    用户评价
    '''

    uid = models.CharField(
        max_length=36, null=False, unique=True, help_text='', primary_key=True
    )
    post_id = models.TextField(null=False, help_text='')
    user_id = models.CharField(null=False, max_length=36, help_text='')  # index=True,
    value = models.IntegerField()  # 用户评价， 1 或 0, 作为计数
    class Meta:
        db_table = 'tabevaluation'
        verbose_name = "Evaluation"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabRating(models.Model):
    '''
    Rating for App of each user.
    '''

    uid = models.CharField(
        max_length=36, null=False, unique=True, help_text='', primary_key=True
    )
    user_id = models.CharField(null=False, max_length=36, help_text='')  # index=True,
    post_id = models.TextField(null=False, help_text='')  # index=True,
    rating = models.FloatField(
        null=False,
    )
    timestamp = models.IntegerField(null=False)
    class Meta:
        db_table = 'tabrating'
        verbose_name = "Rating"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabUsage(models.Model):
    '''
    记录用户访问 Post 的概括情况。
    包括数目，最后的访问时间。
    '''

    uid = models.CharField(
        max_length=36, null=False, unique=True, help_text='', primary_key=True
    )
    post_id = models.TextField(null=False, help_text='')
    user_id = models.CharField(null=False, max_length=36, help_text='')  # index=True,
    count = models.IntegerField()
    tag_id = models.CharField(null=False, max_length=4, help_text='')
    kind = models.CharField(null=False, max_length=1)
    timestamp = models.IntegerField()
    class Meta:
        db_table = 'tabusage'
        verbose_name = "Usage"
        ordering = ['uid']
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['user_id'], name='tabusage_user_id'),
        ]


class TabRel(models.Model):
    '''
    相关应用
    相关性，并非是对称操作
    '''

    uid = models.CharField(
        max_length=36, null=False, unique=True, help_text='', primary_key=True
    )
    post_f_id = models.TextField(null=False, help_text='')
    post_t_id = models.TextField(null=False, help_text='')
    count = models.IntegerField()
    class Meta:
        db_table = 'tabrel'
        verbose_name = "Rel"
        ordering = ['uid']
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['uid'], name='tabrel_uid'),
        ]


class TabCorrelation(models.Model):
    '''
    Post之间的相关性
    `kind为`相关性的类别：
    1: 同小类
    2: 同大类
    3: 同类 (kind)
    4: 全系统
    5: 与文档
    '''

    uid = models.CharField(
        max_length=36, null=False, unique=True, help_text='', primary_key=True
    )
    post_id = models.TextField(null=False, help_text='')
    rel_id = models.TextField(null=False, help_text='')
    kind = models.IntegerField()
    order = models.IntegerField()
    class Meta:
        db_table = 'tabcorrelation'
        verbose_name = "Correlation"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabEntity2User(models.Model):
    '''
    The table for the entity to user.
    '''

    uid = models.CharField(
        null=False, unique=True, primary_key=True, max_length=36  #  index=True,
    )
    entity_id = models.CharField(null=False, max_length=36, help_text='')
    user_id = models.CharField(
        null=False, max_length=36, help_text='用户ID,未登录表示为xxxx'  # index=True,
    )
    user_ip = models.CharField(null=False, help_text='用户端ip', max_length=36)
    timestamp = models.IntegerField(null=False)
    class Meta:
        db_table = 'tabentity2user'
        verbose_name = "Entity2User"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabLog(models.Model):
    '''
    用户访问行为记录
    '''

    uid = models.CharField(
        null=False, unique=True, primary_key=True, max_length=36 # , db_index=True,
    )
    current_url = models.CharField(null=False, max_length = 255, help_text='')
    refer_url = models.CharField(null=False, max_length = 255, help_text='')
    user_id = models.CharField(null=False, max_length=36, help_text='',  db_index=True)
    time_create = models.BigIntegerField()
    time_out = models.BigIntegerField()
    time = models.BigIntegerField()
    class Meta:
        db_table = 'tablog'
        verbose_name = "Log"
        ordering = ['uid']
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['user_id'], name='tablog_user_id'),
            # models.Index(fields=['uid'], name='pkey'),
        ]


class TabReplyid(models.Model):
    '''
    用户评论回复。
    '''

    uid = models.CharField(
        null=False,
        # index=False,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    reply0 = models.CharField(null=False, max_length=36, help_text='')
    reply1 = models.CharField(null=False, max_length=36, help_text='')
    time_create = models.IntegerField()
    class Meta:
        db_table = 'tabreplyid'
        verbose_name = "Replyid"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabReferrer(models.Model):
    '''
    创建 访问来源 记录表
    '''

    uid = models.CharField(
        null=False,
        # index=False,
        unique=True,
        primary_key=True,
        default='00000',
        help_text='',
        max_length=255,
    )
    media = models.CharField(null=False,  max_length = 255,help_text='来源')
    terminal = models.CharField(null=False,  max_length = 255,help_text='终端')
    userip = models.CharField(null=False, unique=True,  max_length = 255,help_text='用户端ip')
    # usercity = models.CharField(null=False, help_text='用户端城市', )
    kind = models.CharField(null=False, max_length=1, default='1', help_text='')
    time_create = models.IntegerField()
    time_update = models.IntegerField()
    class Meta:
        db_table = 'tabreferrer'
        verbose_name = "Referrer"
        ordering = ['uid']
        verbose_name_plural = verbose_name


# 以下准备实现RBAC，
# 参考： https://blog.csdn.net/fksfdh/article/details/106204317

# 此表去掉， 使用 TabUser表即可。
class TabStaff(models.Model):
    '''
    后台人员表，名称使用 Staff.
    '''
    uid = models.CharField(null=False, # index=True,
                           unique=True, primary_key=True, max_length=36, help_text='')
    name = models.CharField(null=False, # index=True,
                            unique=True, max_length=255, help_text='User Name')
    email = models.CharField(null=False, unique=True, max_length=255, help_text='User Email')
    passwd = models.CharField(null=False, max_length=255, help_text='User Password')
    time_reset_passwd = models.IntegerField(null=False, default=0)
    time_login = models.IntegerField(null=False, default=0)
    time_create = models.IntegerField(null=False, default=0)
    time_update = models.IntegerField(null=False, default=0)
    time_email = models.IntegerField(null=False, default=0, help_text='Time auto send email.')
    failed_count = models.IntegerField(null=False, default=0, help_text='record the times for trying login.')
    time_failed = models.IntegerField(null=False, default=0, help_text='timestamp for login failed.')
    extinfo = models.JSONField(null=False, default={}, help_text='Extra data in JSON.')
    class Meta:
        db_table = 'tabstaff'
        verbose_name = "Staff"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabRole(models.Model):
    '''
    后台人员分组表，或角色表
    角色和组两个概念可能会让人混淆，在这里做个区分：角色赋予的是主体，主体可以是用户，也可以是组；角色是权限的集合；组是用户的集合
    '''

    uid = models.CharField(
        null=False,
        # index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    name = models.CharField(
        null=False, # index=True,
        unique=True, max_length=255, help_text='分组名称'
    )
    status = models.IntegerField(null=False, default=0, help_text='角色状态.0=禁用,1=启用')
    pid = models.CharField(null=False, max_length=36, help_text='parent id')
    time_create = models.IntegerField(null=False, default=0)
    time_update = models.IntegerField(null=False, default=0)
    class Meta:
        db_table = 'tabrole'
        verbose_name = "Role"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabPermission(models.Model):
    '''
    后台人员权限表
    action, 缺省的值如下：
    * assign_group:分组
    * assign_role:赋权限
    * can_view:查看
    * can_add:添加
    * can_edit:编辑
    * can_delete:删除
    * can_review:复查
    * can_verify:审核
    '''

    uid = models.CharField(
        null=False,
        # index=True,
        unique=True,
        primary_key=True,
        max_length=36,
        help_text='',
    )
    name = models.CharField(
        null=False, # index=True,
        unique=True, max_length=255, help_text='权限名称'
    )
    action = models.CharField(null=False, max_length=255, help_text='允许动作,字符串编码')
    controller = models.CharField(null=False, max_length=255, help_text='控制器')
    class Meta:
        db_table = 'tabpermission'
        verbose_name = "Permission"
        ordering = ['uid']
        verbose_name_plural = verbose_name


class TabStaff2Role(models.Model):
    '''
    人员、角色关联表
    '''

    staff = models.ForeignKey(TabMember,  help_text='后台人员id', on_delete=models.CASCADE)
    role = models.ForeignKey(TabRole,  help_text='后台角色id', on_delete=models.CASCADE)
    class Meta:
        db_table = 'tabstaff2role'
        verbose_name = "Staff2Role"
        ordering = ['role']
        verbose_name_plural = verbose_name


class TabRole2Permission(models.Model):
    '''
    角色、权限关联表
    '''
    
    

    role = models.ForeignKey(TabRole,  help_text='后台角色id',on_delete=models.CASCADE)
    permission = models.ForeignKey(
        TabPermission,  help_text='后台权限id', on_delete=models.CASCADE
    )
    kind = models.CharField(null=False, max_length=1, default='1', help_text='app type')
    class Meta:
        db_table = 'tabrole2permission'
        verbose_name = "Role2Permission"
        ordering = ['kind']
        verbose_name_plural = verbose_name


if __name__ == '__main__':
    from pprint import pprint

    user = TabMember()
    # print(user.dirty_fields)
    for x in user.dirty_fields:
        print('=' * 40)
        print(x)
        print(x.name, x.field_type, x.index)
        pprint(dir(x))
