import markdown
from django.db import models
from django.contrib.auth import get_user_model
from zhongnan.zn_dataset_category.models import ZNDatasetCategory
from zhongnan.zn_dataset_label.models import ZNDatasetLabel
from base.models import basemodel
from mdeditor.fields import MDTextField
from django.utils.safestring import mark_safe

User = get_user_model()


class ZNDataset(basemodel):
    datasetid = models.CharField(blank=True, null=True, max_length=255, verbose_name='数据ID')
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    cnt_md = MDTextField(verbose_name="内容", null=True, blank=True)
    label = models.ManyToManyField(ZNDatasetLabel, related_name='zn_dataset', verbose_name='标签', blank=True)
    category = models.ForeignKey(ZNDatasetCategory, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='zn_dataset', verbose_name='分类名称')

    # -----------------------------------------------------------------------------------
    # 地图
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")
    zoom_current = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="初始缩放级别")
    zoom_min = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="最大缩放级别")
    zoom_max = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="最小缩放级别")
    layer_name = models.CharField(blank=True, null=True, default='', max_length=255, verbose_name="地图名称")
    url = models.CharField(null=True, blank=True, default='', verbose_name="地址")
    path = models.TextField(null=True, blank=True, default='', verbose_name="路径")
    host = models.CharField(blank=True, null=True, default='', max_length=255, verbose_name="host")
    name = models.CharField(blank=True, null=True, default='', max_length=255, verbose_name="名称")
    # -----------------------------------------------------------------------------------
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='zn_dataset',
                             editable=False,
                             verbose_name='用户名')
    view_count = models.IntegerField(blank=True, null=True, default=0, verbose_name="浏览量", editable=False)
    logo = models.ImageField(upload_to='zn_dataset/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    file = models.FileField(upload_to='zn_dataset/files/', max_length=255, null=True, blank=True,
                            verbose_name="文件")


    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)

    def __str__(self):
        return self.title
    def get_html_content(self):
        html_content = markdown.markdown(self.cnt_md)
        return mark_safe(html_content)
    class Meta(basemodel.Meta):
        db_table = 'zn_dataset'
        verbose_name = "中南数据信息"
        verbose_name_plural = verbose_name