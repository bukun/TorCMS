from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel, basecategory

User = get_user_model()


class igaiscategory(basemodel, basecategory):
    class Meta(basemodel.Meta):
        db_table = 'igaiscategory'
        verbose_name = "IGAIS分类"
        verbose_name_plural = verbose_name

class igaislabel(basemodel):
    name = models.CharField(blank=True, unique=True, null=False, max_length=255, verbose_name="标签名称")


    def __str__(self):
        return self.name

    class Meta(basemodel.Meta):
        db_table = 'igaislabel'
        verbose_name = "IGAIS标签"
        verbose_name_plural = verbose_name


class igaisdata(basemodel):

    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")

    label = models.ManyToManyField(igaislabel, related_name='igaisdata', verbose_name='标签', blank=True)
    category = models.ForeignKey(igaiscategory, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='igaisdata', verbose_name='分类名称')
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='igaisdata',editable=True,
                             verbose_name='用户名')
    view_count = models.IntegerField(blank=True, null=True, default=0, verbose_name="浏览量")
    logo = models.ImageField(upload_to='IgaisData/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    file = models.FileField(upload_to='IgaisData/files/', max_length=255, null=True, blank=True,
                            verbose_name="文件")

    cnt_md = models.TextField(verbose_name="内容",null=True)

    kind = models.CharField(blank=True, null=False, max_length=1, verbose_name="kind", default='9')
    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'igaisdata'
        verbose_name = "IGAIS数据"
        verbose_name_plural = verbose_name