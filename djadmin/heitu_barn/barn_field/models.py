from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel

User = get_user_model()


class Barnfield(basemodel):
    name = models.CharField(blank=True, null=False, max_length=255, verbose_name="田块名称")
    fieldid = models.CharField(blank=True, null=False, max_length=255, verbose_name="田块id")
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    logo = models.ImageField(upload_to='barn_field/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")

    cnt_md = models.TextField(verbose_name="内容", null=True)
    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)

    def __str__(self):
        return self.name

    class Meta(basemodel.Meta):
        db_table = 'Barnfield'
        verbose_name = "农业站田块"
        verbose_name_plural = verbose_name
