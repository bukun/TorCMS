from django.db import models
from base.models import basemodel, basecategory
from django.contrib.auth import get_user_model
from mdeditor.fields import MDTextField
from django.contrib.sites.models import Site
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField  # 此句是新增

User = get_user_model()


class DocumentCatagory(basemodel, basecategory):
    sites = models.ManyToManyField(Site, blank=True, related_name='doc_category', verbose_name='Site')

    class Meta(basemodel.Meta):
        db_table = 'doc_category'
        verbose_name = "文档分类"
        verbose_name_plural = verbose_name


class DocLabel(basemodel):
    name = models.CharField(blank=True, unique=True, null=False, max_length=255, verbose_name="标签名称")
    sites = models.ManyToManyField(Site, blank=True, related_name='doclabel', verbose_name='Site')

    def __str__(self):
        return self.name

    class Meta(basemodel.Meta):
        db_table = 'doclabel'
        verbose_name = "文档标签"
        verbose_name_plural = verbose_name


class Document(basemodel):
    title = models.CharField(null=False, max_length=255, verbose_name="标题")

    cnt_md = MDTextField(verbose_name="内容", null=True, blank=True)
    label = models.ManyToManyField(DocLabel, related_name='document',
                                   verbose_name='标签', blank=True)
    sites = models.ManyToManyField(Site, blank=True, related_name='document', verbose_name='Site')
    category = models.ForeignKey(DocumentCatagory,
                                 on_delete=models.CASCADE,
                                 blank=True, null=True,
                                 related_name='document', verbose_name='分类名称')
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, editable=False,
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

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'document'
        verbose_name = "文档管理"
        verbose_name_plural = verbose_name


class Topic(basemodel):
    title = models.CharField(null=False, max_length=255, verbose_name="标题")
    cnt_md = RichTextUploadingField(verbose_name="内容")
    label = models.ManyToManyField(DocLabel, related_name='topic', verbose_name='标签', blank=True)
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                             null=True, related_name='topic', verbose_name='用户名')

    logo = models.ImageField(upload_to='topic/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    file = models.FileField(upload_to='topic/files/', max_length=255, null=True, blank=True,
                            verbose_name="文件")

    memo = models.TextField(null=True, blank=True, default='', verbose_name='Memo')
    view_count = models.IntegerField(blank=True, null=True, default=0,
                                     verbose_name="浏览量", editable=False)
    sites = models.ManyToManyField(Site, blank=True, related_name='topic', verbose_name='Site')
    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.',
                               blank=True, editable=False)

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'topic'
        verbose_name = "问答管理"
        verbose_name_plural = verbose_name


#
class Comment(MPTTModel, basemodel):  # 定义评论模型
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, related_name='comment', verbose_name='评论文章')

    content = RichTextUploadingField(verbose_name='评论内容', null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='comment',
                             verbose_name='评论者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children',
                            verbose_name='父评论id')
    reply_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='replyers')

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'comment'
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name
