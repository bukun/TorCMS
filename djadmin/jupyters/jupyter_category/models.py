from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel, basecategory
from django.contrib.sites.models import Site
User = get_user_model()


class JupyterCatagory(basemodel, basecategory):
    sites = models.ManyToManyField(Site,blank=True, related_name='jupyter_category', verbose_name='Site')
    class Meta(basemodel.Meta):
        db_table = 'jupyter_category'
        verbose_name = "科学数据计算模型分类"
        verbose_name_plural = verbose_name