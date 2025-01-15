from mdeditor.fields import MDTextField
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel, basecategory

User = get_user_model()


class ZNEventCategory(basemodel, basecategory):
    class Meta(basemodel.Meta):
        db_table = 'zn_event_category'
        verbose_name = "中南事件分类"
        verbose_name_plural = verbose_name


class ZNEventLabel(basemodel):
    name = models.CharField(blank=True, unique=True, null=False, max_length=255, verbose_name="标签名称")

    def __str__(self):
        return self.name

    class Meta(basemodel.Meta):
        db_table = 'zn_event_labels'
        verbose_name = "中南事件标签信息"
        verbose_name_plural = verbose_name


class sub_type(models.IntegerChoices):
    type0 = 0, ''
    type1 = 1, 'epidemic'
    type2 = 2, 'animal'
    type3 = 3, 'insect'
    type4 = 4, 'drought'
    type5 = 5, 'wildfire'
    type6 = 6, 'mass_movement(dry)'
    type7 = 7, 'earthquake'
    type8 = 8, 'volcanic'
    type9 = 9, 'Landslide'
    type10 = 10, 'Flood'
    type11 = 11, 'Storm'
    type12 = 12, 'Fog'
    type13 = 13, 'Extreme'
    type14 = 14, 'temperatur'
    type15 = 15, 'Transport'
    type16 = 16, 'Industrial'
    type17 = 17, 'Miscellaneous'


class location(models.IntegerChoices):
    type0 = 0, ''
    type1 = 1, 'Africa'
    type2 = 2, 'Americas'
    type3 = 3, 'Asia'
    type4 = 4, 'Europe'
    type5 = 5, 'Oceania'


class ZNEvent(basemodel):
    datasetid = models.CharField(blank=True, null=True, max_length=255, verbose_name='数据ID')
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    cnt_md = MDTextField(verbose_name="内容", null=True, blank=True)
    cnt_html = models.TextField(blank=True, null=True, verbose_name="内容HTML")
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")
    url = models.CharField(null=True, blank=True, default='', verbose_name="URL", max_length=255)
    sub_type = models.IntegerField(choices=sub_type.choices, verbose_name="Sub type", default=0)
    location = models.IntegerField(choices=location.choices, verbose_name="Location", default=0)

    date = models.DateTimeField(verbose_name='创建日期', null=True, blank=True)
    category = models.ForeignKey(ZNEventCategory, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='zn_event', verbose_name='分类名称')
    label = models.ManyToManyField(ZNEventLabel, related_name='zn_event', verbose_name='标签', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='zn_event',
                             editable=False,
                             verbose_name='用户名')
    view_count = models.IntegerField(blank=True, null=True, default=0, verbose_name="浏览量", editable=False)
    logo = models.ImageField(upload_to='zn_event/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    file = models.FileField(upload_to='zn_event/files/', max_length=255, null=True, blank=True,
                            verbose_name="文件")

    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(ZNEvent, self).save(*args, **kwargs)

        self.cnt_html = self.get_html_content()

        super(ZNEvent, self).save(*args, **kwargs)

    class Meta(basemodel.Meta):
        db_table = 'zn_event'
        verbose_name = "中南事件信息"
        verbose_name_plural = verbose_name
