from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel,basecategory
from django.contrib.sites.models import Site
User = get_user_model()



class heitumapcategory(basemodel,basecategory):
    sites = models.ManyToManyField(Site,blank=True, related_name='heitumapcategory', verbose_name='Site')
    class Meta(basemodel.Meta):
        db_table = 'heitumapcategory'
        verbose_name = "黑土地图分类"
        verbose_name_plural = verbose_name
