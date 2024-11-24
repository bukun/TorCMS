from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from base.models import basemodel

User = get_user_model()


class Barndataset(basemodel):
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    logo = models.ImageField(upload_to='barn_dataset/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")

    cnt_md = models.TextField(verbose_name="内容", null=True)
    location = gismodels.PointField(null=True, blank=True, verbose_name="位置", default=(Point(0, 0, srid=4326)))

    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'Barndataset'
        verbose_name = "农业站照片"
        verbose_name_plural = verbose_name
