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

class PlanarFeatures(basemodel):
    '''
    面状要素库
    '''
    region = models.CharField(max_length=255, blank=True, null=True, verbose_name="所属地区")
    location_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="现代地名")
    historical_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="历史地名")
    set_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="设置时间")
    cancel_time = models.CharField(max_length=255, blank=True, null=True, verbose_name="取消时间")
    zoom = models.FloatField(blank=True, null=True, default=8, verbose_name="缩放级别")
    content = MDTextField(verbose_name="介绍", null=True, blank=True)
    location = gismodels.PolygonField(null=True,blank=True,verbose_name="位置")
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
            'zoom': self.zoom,
            'content': self.content,
            'is_en': self.is_en
        }
    class Meta(basemodel.Meta):
        db_table = 'planarfeatures'
        verbose_name = "面状要素库"
        verbose_name_plural = verbose_name

