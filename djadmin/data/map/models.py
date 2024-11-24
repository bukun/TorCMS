from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from data.dataset.models import dataset
from django.contrib.sites.models import Site
User = get_user_model()


class map(basemodel):
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    data = models.ForeignKey(dataset, on_delete=models.CASCADE, blank=True, null=True,
                             related_name='dataset', verbose_name='数据')

    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")
    zoom_current = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="初始缩放级别")
    zoom_min = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="最大缩放级别")
    zoom_max = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="最小缩放级别")
    sites = models.ManyToManyField(Site,blank=True, related_name='map', verbose_name='Site')
    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)


    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'map'
        verbose_name = "地图"
        verbose_name_plural = verbose_name
