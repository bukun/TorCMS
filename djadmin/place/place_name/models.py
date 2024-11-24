from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
User = get_user_model()
from django.forms import TextInput
from django import forms
class statetype(models.IntegerChoices):
    type1 = 0, '国内'
    type2 = 1, '国外'

class PlaceName(basemodel):
    '''
    地名库设计为县、乡及以上行政单元的存储库。
    侧重于古代地名的整编。
    数据库的设计包含有“历史地名”，“经度”，“纬度”，“设置时间”，“取消时间”，“现代地名”，“介绍”
    '''
    region = models.CharField(max_length=255, blank=True, null=True, verbose_name="所属地区")
    location_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="现代地名")
    historical_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="历史地名")
    set_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="设置时间")
    cancel_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="取消时间")
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")
    zoom = models.FloatField(blank=True, null=True, default=8, verbose_name="缩放级别")
    content = MDTextField(verbose_name="介绍", null=True, blank=True)
    location = gismodels.PointField(null=True,blank=True,verbose_name="位置",default=(Point(0, 0,srid=4326)))
    is_en = models.IntegerField(choices=statetype.choices, verbose_name="国内外", default=0)


    def __str__(self):
        return str(self.id)
    def to_dict(self):
        return {
            'id': self.id,
            'region': self.region,
            'location_name': self.location_name,
            'historical_name': self.historical_name,
            'set_time': self.set_time,
            'cancel_time': self.cancel_time,
            'lat': self.lat,
            'lon': self.lon,
            'zoom':self.zoom,
            'content': self.content,
            'is_en': self.is_en
        }
    class Meta(basemodel.Meta):
        db_table = 'place_name'
        verbose_name = "地名库"
        verbose_name_plural = verbose_name

