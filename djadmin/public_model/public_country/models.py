import markdown
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
User = get_user_model()


class PublicCountry(basemodel):
    name=models.CharField(blank=True,unique=True, null=False, max_length=255, verbose_name="名称")


    sites = models.ManyToManyField(Site,blank=True, related_name='public_country', verbose_name='Site')

    def __str__(self):
        return self.name


    class Meta(basemodel.Meta):
        db_table = 'public_country'
        verbose_name = "Country"
        verbose_name_plural = verbose_name
