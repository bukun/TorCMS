import markdown
from django.db import models
from base.models import basemodel, basecategory
from django.contrib.auth import get_user_model
from mdeditor.fields import MDTextField
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField, RichTextUploadingFormField  # 此句是新增

User = get_user_model()


class CrawlSource(basemodel):
    title = models.CharField(null=False, max_length=255, verbose_name="标题")
    url = models.URLField(verbose_name="网址")

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'crawlsource'
        verbose_name = "爬取数据来源"
        verbose_name_plural = verbose_name


class language(models.IntegerChoices):
    type1 = 1, '英文'
    type2 = 2, '中文'


class CrawlLabel(basemodel, basecategory):
    is_en = models.IntegerField(choices=language.choices, verbose_name="语言", default=1)

    class Meta(basemodel.Meta):
        db_table = 'crawllabel'
        verbose_name = "爬取文档标签"
        verbose_name_plural = verbose_name


class statetype(models.IntegerChoices):
    type1 = 0, '未处理'
    type2 = 1, '段落已处理'
    type3 = 2, '自动翻译'
    type4 = 3, '已校对'


class CrawlDocumentEN(basemodel):
    title = models.CharField(null=False, max_length=255, verbose_name="标题")
    cn_title = models.CharField(null=True, max_length=255, verbose_name="中文标题", blank=True)
    cnt_html = RichTextUploadingField(verbose_name="内容", null=True, blank=True, editable=False)
    cnt_md = MDTextField(verbose_name="爬取内容", null=True, blank=True)
    cnt_md_edit = MDTextField(verbose_name="处理后内容", null=True, blank=True)
    cnt_md_trans = MDTextField(verbose_name="内容翻译", null=True, blank=True)
    author = models.CharField(blank=True, null=True, verbose_name='作者', max_length=255)
    crawlurl = models.CharField(null=True, blank=True, max_length=255, verbose_name="源URL")
    source = models.ForeignKey(CrawlSource,
                               on_delete=models.CASCADE,
                               blank=True, null=True,
                               related_name='crawl_document_en', verbose_name='数据来源')
    label = models.ManyToManyField(CrawlLabel, related_name='crawl_document_en',
                                   verbose_name='数据分类', blank=True)

    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True, null=True)
    update_date = models.CharField(verbose_name='发布日期', null=True, blank=True, max_length=255)

    logo = models.ImageField(upload_to='crawl_document_en/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    file = models.FileField(upload_to='crawl_document_en/files/', max_length=255, null=True, blank=True,
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
        return str(self.id)

    def get_html_content(self):
        html_content = markdown.markdown(self.cnt_md_trans)
        return mark_safe(html_content)

    class Meta(basemodel.Meta):
        db_table = 'crawldocumenten'
        verbose_name = "爬取英文文档管理"
        verbose_name_plural = verbose_name


# 简单日志记录，用于主要记录节点信息
class RzLog(basemodel):
    sheet = models.CharField(verbose_name='表单名称', max_length=100, default='')
    user = models.CharField(verbose_name='操作人员', max_length=100, default='')
    # the_id = models.CharField(verbose_name='数据ID', max_length=255, default='')
    the_id = models.ForeignKey(CrawlDocumentEN, related_name='rzlog', on_delete=models.CASCADE, db_constraint=False,
                               verbose_name='数据ID')
    the_key = models.CharField(verbose_name='字段名称', max_length=255, default='')
    old_values = MDTextField(verbose_name='原数据', null=True, blank=True)
    new_values = MDTextField(verbose_name='新数据', null=True, blank=True)
    log_date = models.DateTimeField(verbose_name='修改时间', auto_now_add=True, null=True)
    note = models.TextField(verbose_name='备注信息', null=True, default='', blank=True)
    create_user = models.ForeignKey(User, related_name='create_user_rz', on_delete=models.CASCADE, db_constraint=False,
                                    verbose_name='创建人员')
    update_user = models.ForeignKey(User, related_name='update_user_rz', on_delete=models.CASCADE, db_constraint=False,
                                    verbose_name='修改人员')

    def __str__(self):
        return str(self.id)

    class Meta(basemodel.Meta):
        db_table = 'rzlog'
        verbose_name = "爬取英文文档日志记录管理"
        verbose_name_plural = verbose_name

class CrawlDocument(basemodel):
    title = models.CharField(null=False, max_length=255, verbose_name="标题")
    cnt_html = RichTextUploadingField(verbose_name="内容", null=True, blank=True, editable=False)
    cnt_md = MDTextField(verbose_name="爬取内容", null=True, blank=True)
    cnt_md_edit = MDTextField(verbose_name="处理后内容", null=True, blank=True)
    cnt_md_trans = MDTextField(verbose_name="内容翻译", null=True, blank=True)
    author = models.CharField(blank=True, null=True, verbose_name='作者', max_length=255)
    crawlurl = models.CharField(null=True, blank=True, max_length=255, verbose_name="源URL")
    source = models.ForeignKey(CrawlSource,
                               on_delete=models.CASCADE,
                               blank=True, null=True,
                               related_name='crawl_document', verbose_name='数据来源')
    label = models.ManyToManyField(CrawlLabel, related_name='crawl_document',
                                   verbose_name='数据分类', blank=True)

    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True, null=True)
    update_date = models.CharField(verbose_name='发布日期', null=True, blank=True, max_length=255)

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

