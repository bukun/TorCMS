import markdown
from django.db import models
from django.contrib.auth import get_user_model

from crawl.crawl_source.models import CrawlSource
from base.models import basemodel
from crawl.crawl_label.models import CrawlLabel
User = get_user_model()
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField  # 此句是新增
from mdeditor.fields import MDTextField
from django.utils.safestring import mark_safe
class statetype(models.IntegerChoices):
    type1 = 0, '未处理'
    type2 = 1, '段落已处理'
    type3 = 2, '自动翻译'
    type4 = 3, '已校对'
class CrawlDocument(basemodel):
    title = models.CharField(null=False, max_length=255, verbose_name="标题")
    cnt_html = RichTextUploadingField(verbose_name="内容", null=True, blank=True, editable=False)
    cnt_md = MDTextField(verbose_name="爬取内容", null=True, blank=True)
    cnt_md_edit = MDTextField(verbose_name="处理后内容", null=True, blank=True)
    cnt_md_trans = MDTextField(verbose_name="内容翻译", null=True, blank=True)
    author = models.CharField(blank=True, null=True, verbose_name='作者',max_length=255)
    crawlurl = models.CharField(null=True, blank=True, max_length=255, verbose_name="源URL")
    source = models.ForeignKey(CrawlSource,
                               on_delete=models.CASCADE,
                               blank=True, null=True,
                               related_name='crawl_document', verbose_name='数据来源')
    label = models.ManyToManyField(CrawlLabel, related_name='crawl_document',
                              verbose_name='数据分类', blank=True)

    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True, null=True)
    update_date = models.CharField(verbose_name='发布日期', null=True, blank=True,max_length=255)


    logo = models.ImageField(upload_to='crawl_document/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    file = models.FileField(upload_to='crawl_document/files/', max_length=255, null=True, blank=True,
                            verbose_name="文件")
    state = models.IntegerField(choices=statetype.choices, verbose_name="状态", default=0)
    valid = models.BooleanField(blank=False, null=True, verbose_name="是否发布", default=0)
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

    def __str__(self):
        return self.title

    def get_html_content(self):
        html_content = markdown.markdown(self.cnt_md_trans)
        return mark_safe(html_content)
    class Meta(basemodel.Meta):
        db_table = 'crawldocument'
        verbose_name = "爬取文档管理"
        verbose_name_plural = verbose_name
