from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel

User = get_user_model()

class ThematicMaps(basemodel):

    layer = models.CharField(blank=True, null=False, max_length=255, verbose_name="图层")
    label = models.CharField(blank=True, null=False, max_length=255, verbose_name="标签")
    icon = models.CharField(blank=True, null=False, max_length=255, verbose_name="图标")



    def __str__(self):
        return self.layer

    class Meta(basemodel.Meta):
        db_table = 'thematicmaps'
        verbose_name = "专题地图"
        verbose_name_plural = verbose_name
