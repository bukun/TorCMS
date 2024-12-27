import markdown
from django.db import models
from django.contrib.auth import get_user_model
from data.categorys.models import categorys
from data.labels.models import labels
from base.models import basemodel
from mdeditor.fields import MDTextField
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site

User = get_user_model()


class dataset(basemodel):
    datasetid = models.CharField(blank=True, null=True, max_length=255, verbose_name='数据ID')
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    title_alternate = models.CharField(blank=True, max_length=255, verbose_name="别名")
    topicategory = models.CharField(blank=True, max_length=255, verbose_name="建议学科分类")
    language = models.CharField(blank=True, max_length=255, verbose_name="语言")
    type = models.CharField(blank=True, max_length=255, verbose_name="数据类型")
    format = models.CharField(blank=True, max_length=255, verbose_name="数据格式")
    links = models.CharField(blank=True, max_length=255, verbose_name="链接")
    time_begin = models.CharField(blank=True, max_length=255, verbose_name="开始时间")
    time_end = models.CharField(blank=True, max_length=255, verbose_name="结束时间")
    creator = models.CharField(blank=True, max_length=255, verbose_name="数据创建者")
    publisher = models.CharField(blank=True, max_length=255, verbose_name="数据发布者")
    contributor = models.CharField(blank=True, max_length=255, verbose_name="数据贡献者")
    organization = models.CharField(blank=True, max_length=255, verbose_name="组织机构")
    operateson = models.CharField(blank=True, max_length=255, verbose_name="元数据创建者")
    cnt_md = MDTextField(verbose_name="内容", null=True, blank=True)

    label = models.ManyToManyField(labels, related_name='dataset', verbose_name='标签', blank=True)
    category = models.ForeignKey(categorys, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='dataset', verbose_name='分类名称')
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True, related_name='dataset',
                             editable=False,
                             verbose_name='用户名')
    view_count = models.IntegerField(blank=True, null=True, default=0, verbose_name="浏览量", editable=False)
    logo = models.ImageField(upload_to='dataset/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    file = models.FileField(upload_to='dataset/files/', max_length=255, null=True, blank=True,
                            verbose_name="文件")

    sites = models.ManyToManyField(Site, blank=True, related_name='dataset', verbose_name='Site')
    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)

    def __str__(self):
        return self.title



    class Meta(basemodel.Meta):
        db_table = 'dataset'
        verbose_name = "数据"
        verbose_name_plural = verbose_name
