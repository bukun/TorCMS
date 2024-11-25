from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from django.contrib.sites.models import Site
User = get_user_model()


class LiteratureDate(basemodel):
    pub_date=models.CharField(blank=True,unique=True, null=False, max_length=255, verbose_name="日期")
    sites = models.ManyToManyField(Site,blank=True, related_name='literature_date', verbose_name='Site')

    def __str__(self):
        return self.pub_date

    class Meta(basemodel.Meta):
        db_table = 'literature_date'
        verbose_name = "Literature Date"
        verbose_name_plural = verbose_name
