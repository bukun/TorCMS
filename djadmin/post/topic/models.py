from django.db import models
from django.contrib.auth import get_user_model
from post.doc_label.models import DocLabel
from base.models import basemodel
from mptt.models import MPTTModel, TreeForeignKey

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField  # 此句是新增
from django.contrib.sites.models import Site
User = get_user_model()

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
    sites = models.ManyToManyField(Site,blank=True, related_name='topic', verbose_name='Site')
    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.',
                               blank=True, editable=False)

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'topic'
        verbose_name = "问答管理"
        verbose_name_plural = verbose_name

#
class Comment(MPTTModel,basemodel):  # 定义评论模型
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, related_name='comment', verbose_name='评论文章')

    content = RichTextUploadingField(verbose_name='评论内容',null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='comment',
                               verbose_name='评论者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,blank=True, null=True,related_name='children', verbose_name='父评论id')
    reply_to = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True,related_name='replyers')
    def __str__(self):
        return self.content

    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
