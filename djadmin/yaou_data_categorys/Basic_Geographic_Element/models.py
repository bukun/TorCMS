from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel, basecategory
from django.contrib.sites.models import Site
User = get_user_model()


class Basic_Geographic_Element_Category(basemodel, basecategory):
    category_code = models.CharField(blank=True, null=False, max_length=255, verbose_name="编码")
    sites = models.ManyToManyField(Site,blank=True, related_name='Basic_Geographic_Element_Category', verbose_name='Site')

    class Meta(basemodel.Meta):
        db_table = 'yaou_basic_geo'
        verbose_name = "基础地理要素数据指标分类"
        verbose_name_plural = verbose_name
