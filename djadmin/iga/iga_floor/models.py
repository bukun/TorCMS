import markdown
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from django.contrib.sites.models import Site

class iga_floor(basemodel):
    num = models.CharField(blank=True, null=False, max_length=255, verbose_name="楼层")
    sites = models.ManyToManyField(Site, blank=True, related_name='iga_floor', verbose_name='Site')

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'iga_floor'
        verbose_name = "楼层"
        verbose_name_plural = verbose_name
