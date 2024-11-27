from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from django.contrib.sites.models import Site

User = get_user_model()


class labels(basemodel):
    name = models.CharField(blank=True, unique=True, null=False, max_length=255, verbose_name="标签名称")
    sites = models.ManyToManyField(Site,blank=True, related_name='data_label', verbose_name='Site')

    def __str__(self):
        return self.name

    class Meta(basemodel.Meta):
        db_table = 'labels'
        verbose_name = "数据标签"
        verbose_name_plural = verbose_name
