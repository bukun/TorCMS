from django.db import models
from base.models import basemodel, basecategory
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
# from django.contrib.admin.models import LogEntry
from django.contrib.sites.models import Site

User = get_user_model()


class ResourceCatagory(basemodel, basecategory):
    sites = models.ManyToManyField(Site, blank=True, related_name='resource_category', verbose_name='Site')

    class Meta(basemodel.Meta):
        db_table = 'resource_category'
        verbose_name = "软件资源分类管理"
        verbose_name_plural = verbose_name


class OSchoices(models.IntegerChoices):
    type1 = 1, '跨平台'
    type2 = 2, 'GNU/Linux/Unix'
    type3 = 3, 'Windows'
    type4 = 4, 'MacOS X'
    type5 = 5, '其他'


class language(models.IntegerChoices):
    type1 = 1, 'Python'
    type2 = 2, 'C/C++'
    type3 = 3, 'Java'
    type4 = 4, 'PHP'
    type5 = 5, 'C#'
    type6 = 6, 'JavaScript'
    type7 = 7, '其他'


class shouquan(models.IntegerChoices):
    type1 = 1, 'GNU GPL'
    type2 = 2, 'GNU LGPL'
    type3 = 3, 'MIT'
    type4 = 4, 'Public Domain'
    type5 = 5, 'BSDish'
    type6 = 6, 'Apache License'
    type8 = 8, '其他'


class status(models.IntegerChoices):
    type0 = 0, ''
    type1 = 1, 'Inactive'
    type2 = 2, 'OSGeo Project'
    type3 = 3, 'Archived'
    type4 = 4, 'Debian Package'


def set_current_user():
    return get_user_model().objects.first()


class ResourceLabel(basemodel):
    name = models.CharField(blank=True, unique=True, null=False, max_length=255, verbose_name="标签名称")
    sites = models.ManyToManyField(Site, blank=True, related_name='resource_label', verbose_name='Site')

    def __str__(self):
        return self.name

    class Meta(basemodel.Meta):
        db_table = 'resource_label'
        verbose_name = "专题资源标签"
        verbose_name_plural = verbose_name


class Resource(basemodel):
    title = models.CharField(null=False, unique=True, max_length=255, verbose_name="标题")
    version = models.CharField(blank=True, null=True, max_length=255, verbose_name="最新版本")
    url = models.CharField(blank=True, null=True, max_length=255, verbose_name="链接")
    release_time = models.CharField(blank=True, null=True, max_length=255, verbose_name="资源发布时间")
    cnt_md = RichTextUploadingField(verbose_name="内容", blank=True, null=True)
    label = models.ManyToManyField(ResourceLabel, related_name='resource', verbose_name='标签', blank=True)
    category = models.ForeignKey(ResourceCatagory, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='resource', verbose_name='分类名称')
    os = models.IntegerField(choices=OSchoices.choices, verbose_name="操作系统", default=1)
    language = models.IntegerField(choices=language.choices, verbose_name="编程语言", default=1)
    shouquan = models.IntegerField(choices=shouquan.choices, verbose_name="授权方式", default=1)

    status = models.IntegerField(choices=status.choices, verbose_name="状态", default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='resource',
                             editable=False,
                             verbose_name='用户名')
    view_count = models.IntegerField(blank=True, null=True, default=0, verbose_name="浏览量", editable=False)
    logo = models.ImageField(upload_to='resource/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    file = models.FileField(upload_to='resource/files/', max_length=255, null=True, blank=True,
                            verbose_name="文件")

    sites = models.ManyToManyField(Site, blank=True, related_name='resource', verbose_name='Site')
    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)

    def __str__(self):
        return str(self.id)

    class Meta(basemodel.Meta):
        db_table = 'resource_dataset'
        verbose_name = "软件资源"
        verbose_name_plural = verbose_name
