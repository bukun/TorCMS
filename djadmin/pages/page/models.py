import markdown
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from ckeditor_uploader.fields import RichTextUploadingField
from mdeditor.fields import MDTextField
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site

User = get_user_model()


class ThePage(basemodel):
    title = models.CharField(blank=True, unique=True,
                             null=False, max_length=255, verbose_name="标题")
    slug = models.CharField(blank=True, unique=True,
                            null=False, max_length=255, verbose_name="slug")
    cnt_md = RichTextUploadingField(verbose_name="内容")
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                             null=True, related_name='page',
                             editable=False,
                             verbose_name='作者')
    sites = models.ManyToManyField(Site,blank=True,
                                   related_name='page',
                                   verbose_name='Site')


    def __str__(self):
        return self.title

    def get_html_content(self):
        html_content = markdown.markdown(self.cnt_md)
        return mark_safe(html_content)

    class Meta(basemodel.Meta):
        db_table = 'page'
        verbose_name = "单页"
        verbose_name_plural = verbose_name
