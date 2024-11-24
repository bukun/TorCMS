from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel, basecategory
from django.contrib.sites.models import Site
User = get_user_model()


class LiteratureCatagory(basemodel, basecategory):
    sites = models.ManyToManyField(Site,blank=True, related_name='literature_category', verbose_name='Site')
    class Meta(basemodel.Meta):
        db_table = 'literature_category'
        verbose_name = "Literature Category"
        verbose_name_plural = verbose_name
