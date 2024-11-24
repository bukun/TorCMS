from django.db import models
from django.contrib.auth.models import AbstractUser, Group
# from Hdepartment.models import Hdepartment

from base.models import statetype

from mptt.models import MPTTModel, TreeForeignKey






class roletype(models.IntegerChoices):
    type1 = 1, '后台角色管理'
    type2 = 2, '前台用户管理'
    type3 = 3, '经营组织管理'
    type4 = 4, '空间范围管理'

class fieldtype(models.IntegerChoices):
    type1 = 1, '土肥'
    type2 = 2, '植保'
    type3 = 3, '育种'
    type4 = 4, '农机'
    type5 = 5, '金融'
    type6 = 6, '植物营养'
    type7 = 7, '养殖'
    type8 = 8, '环保'
    type9 = 9, '推广营销'
    type10 =10 , '节水灌溉'
    type11 =11 , '农业生态'
    type12 =12 , '信息技术'
    type13 =13 , '其他'



class admingroup(MPTTModel,Group):
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
    #                            verbose_name='上级角色名称')
    parent=TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',verbose_name='上级角色名称')
    type = models.IntegerField(choices=roletype.choices, default=1, verbose_name='角色类型')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '角色管理'
        verbose_name_plural =verbose_name



class myuser(AbstractUser):
    mobile = models.CharField(blank=True, null=True, max_length=255, verbose_name="手机号")
    # 前台用户里 专家、农户、有“地址”这两项，经营主体用户没有（没有应该也可以加这一项）
    # 后台用户没有这两项
    location = models.CharField(blank=True, null=True, max_length=255, verbose_name="地区地址")
    detailed_address = models.CharField(blank=True, null=True, max_length=255, verbose_name="详细地址")

    # 后台用户没有这项
    avatar_img = models.ImageField(upload_to='MyUser/imgs/', max_length=255, null=True,
                                   blank=True, verbose_name="头像")

    # 专家农户政府都有都有这一项，启用或禁用，如果修改为禁用就用户不能使用帐号登录？是不是
    state = models.IntegerField(choices=statetype.choices, verbose_name="状态", default=1)

    # -----------------------------------------
    # 前台用户

    # 规模经营主体用户
    #  开通经营主体账号联系:18504667792，就只能后台给添加。
    # 综合起来让他叫 角色啊 是农户啊，还是属于什么经营主体的 吧  不用不用 他有个自带的groups
    # belong_jyztzz= models.ForeignKey(admingroup, on_delete=models.CASCADE, null=True, blank=True,
    #                                       related_name='background_user_belong_department',
    #                                       verbose_name='所属经营主体组织')
    #
    #
    # # 专家
    # # 专家，可以用户自己新建帐号
    # field = models.IntegerField(choices=fieldtype.choices, default=1, blank=True, null=True,
    #                          verbose_name="领域")
    # # claiming_subject = models.CharField(blank=True, null=True, max_length=255, verbose_name="认领主体")
    #
    # # 农户
    # # 农户，可以用户自己新建帐号  这几个添加到地块里，咋填？放在另一个表？
    # # IDNumber = models.CharField(blank=True, null=True, max_length=255, verbose_name="身份证号")
    # # bank = models.CharField(blank=True, null=True, max_length=255, verbose_name="开户行")
    # # cardnumber = models.CharField(blank=True, null=True, max_length=255, verbose_name="卡号")
    #
    #
    # # 政府人员
    # # 政府也是，不能自己添加，只能后台管理员添加
    # # 政府人员的外部部门，和内部智慧农业的部门数据不是一个
    # government_department = models.CharField(blank=True, null=True, max_length=255, verbose_name="政府人员部门")
    # # 政府人员的外部职务
    # government_duties = models.CharField(blank=True, null=True, max_length=255, verbose_name="政府人员职务")
    # professional_title = models.CharField(blank=True, null=True, max_length=255, verbose_name="职称")
    # address = models.CharField(blank=True, null=True, max_length=255, verbose_name="地址")

    # -----------------------------------------
    # 后台用户
    # 所属的内部部门，连接部门表
    # belong_department = models.ForeignKey(Hdepartment, on_delete=models.CASCADE, null=True, blank=True,
    #                                       related_name='background_user_belong_department',
    #                                       verbose_name='所属部门')


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name




# # 经营主体
# parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
#                            verbose_name='上级经营主体名称')
#
# # 用户 包括后台用户可以选择的：智慧农业总管理员、规模经营主体管理员、 隆源农业超级后台管理员，也没有几个，不用也行
# # 前台用户的角色：经营主体、农户、政府、专家
# # 地块的角色：各个省级、市级，然后根据这个权限来圈选地块的可以操作级别
# type = models.IntegerField(choices=RoleType.choices, default=1, verbose_name='角色类型')
