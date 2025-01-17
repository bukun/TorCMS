from django.db import models
from base.models import basemodel, basecategory
from mdeditor.fields import MDTextField
from public_model.literature_author.models import LiteratureAuthor,LiteratureDate
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

User = get_user_model()


class LiteratureCatagory(basemodel, basecategory):
    sites = models.ManyToManyField(Site, blank=True, related_name='literature_category', verbose_name='Site')

    class Meta(basemodel.Meta):
        db_table = 'literature_category'
        verbose_name = "文献分类"
        verbose_name_plural = verbose_name


class LiteratureLabel(basemodel):
    name = models.CharField(blank=True, unique=True, null=False, max_length=255, verbose_name="标签名称")
    sites = models.ManyToManyField(Site, blank=True, related_name='literature_labels', verbose_name='Site')

    def __str__(self):
        return self.name

    class Meta(basemodel.Meta):
        db_table = 'literature_labels'
        verbose_name = "文献标签"
        verbose_name_plural = verbose_name


class Literature(basemodel):
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    theme = models.CharField(blank=True, null=False, max_length=255, verbose_name="主题")
    type = models.CharField(blank=True, null=False, max_length=255, verbose_name="类型")
    cnt_md = MDTextField(verbose_name="简介", null=True, blank=True)
    category = models.ForeignKey(LiteratureCatagory, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='literature_data', verbose_name='分类名称')
    logo = models.ImageField(upload_to='literature/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    file = models.FileField(upload_to='literature/files/', null=True, blank=True, verbose_name="文件")
    pub_date = models.ForeignKey(LiteratureDate, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='literature_data', verbose_name='发布日期')
    author = models.ManyToManyField(LiteratureAuthor, blank=True, related_name='literature_data', verbose_name='作者')
    label = models.ManyToManyField(LiteratureLabel, related_name='literature_data', verbose_name='标签', blank=True)

    sites = models.ManyToManyField(Site, blank=True, related_name='literature', verbose_name='Site')

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'literature'
        verbose_name = "文献数据"
        verbose_name_plural = verbose_name
