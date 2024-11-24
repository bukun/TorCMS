from django.db import models
from django.contrib.auth import get_user_model
from post.doc_category.models import DocumentCatagory
from post.doc_label.models import DocLabel
from base.models import basemodel
import markdown
User = get_user_model()
from django.utils.safestring import mark_safe
from mdeditor.fields import MDTextField
from django.contrib.sites.models import Site
class Document(basemodel):
    title = models.CharField(null=False, max_length=255, verbose_name="标题")

    cnt_md = MDTextField(verbose_name="内容", null=True, blank=True)
    label = models.ManyToManyField(DocLabel, related_name='document',
                                   verbose_name='标签', blank=True)
    category = models.ForeignKey(DocumentCatagory,
                                 on_delete=models.CASCADE,
                                 blank=True, null=True,
                                 related_name='document', verbose_name='分类名称')
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,editable=False,
                             null=True, related_name='documents', verbose_name='用户名')

    kind = models.CharField(null=False, max_length=1, default='1', verbose_name='kind')

    logo = models.ImageField(upload_to='document/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    file = models.FileField(upload_to='document/files/', max_length=255, null=True, blank=True,
                            verbose_name="文件")

    valid = models.BooleanField(blank=False, null=True, verbose_name="信息是否显示", default=1)
    memo = models.TextField(null=True, blank=True, default='', verbose_name='Memo')
    view_count = models.IntegerField(blank=True, null=True, default=0,
                                     verbose_name="浏览量", editable=False)
    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.',
                               blank=True, editable=False)
    access_1d = models.IntegerField(blank=True, null=True, default=0,
                                    verbose_name='24小时内阅读量', editable=False)
    access_7d = models.IntegerField(blank=True, null=True, default=0,
                                    verbose_name='7*24小时内阅读量', editable=False)
    access_30d = models.IntegerField(blank=True, null=True, default=0,
                                     verbose_name='30*24小时内阅读量', editable=False)
    sites = models.ManyToManyField(Site, blank=True,related_name='document', verbose_name='Site')

    def __str__(self):
        return self.title
    def get_html_content(self):
        html_content = markdown.markdown(self.cnt_md)
        return mark_safe(html_content)

    class Meta(basemodel.Meta):
        db_table = 'document'
        verbose_name = "文档管理"
        verbose_name_plural = verbose_name
