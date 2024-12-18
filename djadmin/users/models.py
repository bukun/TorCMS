import random
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from mptt.models import MPTTModel, TreeForeignKey



class roletype(models.IntegerChoices):
    type1 = 1, '后台角色管理'
    type2 = 2, '前台用户管理'
    type4 = 4, '空间范围管理'
    type5 = 5, 'Jupyter用户'


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

    location = models.CharField(blank=True, null=True, max_length=255, verbose_name="地区地址")
    detailed_address = models.CharField(blank=True, null=True, max_length=255, verbose_name="详细地址")

    # 后台用户没有这项
    avatar_img = models.ImageField(upload_to='MyUser/imgs/', max_length=255, null=True,
                                   blank=True, verbose_name="头像")

    jupyter_url = models.CharField(blank=True, null=True, max_length=255, verbose_name="服务器")
    jupyter_port = models.IntegerField(blank=True, null=True, verbose_name="端口")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        super(myuser, self).save(*args, **kwargs)

        while True:
            random_number = random.randint(10000, 65535)
            try:
                existing_object = myuser.objects.get(jupyter_port=random_number)
            except myuser.DoesNotExist:
                self.jupyter_port = random_number
                break
        super(myuser, self).save(*args, **kwargs)
