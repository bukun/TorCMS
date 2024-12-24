import markdown
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from django.contrib.sites.models import Site

class iga_group(basemodel):
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="学科组")
    group_type = models.CharField(blank=True, null=False, choices=[('1', '学科组'), ('2', '管理支撑部门'),('3', '野外台站')],
                                 default='1',
                                  max_length=255, verbose_name="学科组")
    sites = models.ManyToManyField(Site, blank=True, related_name='iga_group', verbose_name='Site')

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'iga_group'
        verbose_name = "学科组"
        verbose_name_plural = verbose_name
