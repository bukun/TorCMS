from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from base.models import basemodel

User = get_user_model()


class Barndevice(basemodel):
    name = models.CharField(blank=True, null=False, max_length=255, verbose_name="设备名称")
    deviceid = models.CharField(blank=True, null=False, max_length=255, verbose_name="设备id")
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")

    cnt_md = models.TextField(verbose_name="内容", null=True)
    location = gismodels.PointField(null=True, blank=True, verbose_name="位置", default=(Point(0, 0, srid=4326)))
    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)

    def __str__(self):
        return self.name

    class Meta(basemodel.Meta):
        db_table = 'Barndevice'
        verbose_name = "农业站设备"
        verbose_name_plural = verbose_name
