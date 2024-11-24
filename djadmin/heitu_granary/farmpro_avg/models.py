from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel

User = get_user_model()


class farmproavg(basemodel):
    product_name = models.CharField(blank=True, null=False, default='',max_length=255, verbose_name='农产品名称')
    unit = models.CharField(blank=True, null=False, default='',max_length=255, verbose_name="计价单位")
    avg = models.CharField(blank=True, null=False,default='', max_length=255, verbose_name="参考均价")
    sample = models.CharField(blank=True, null=False,default='', max_length=255, verbose_name="样本数量")
    address = models.CharField(blank=True, null=False,default='', max_length=255, verbose_name="省份")
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='farmpro_avg',editable=True,
                             verbose_name='用户名')


    def __str__(self):
        return self.product_name

    class Meta(basemodel.Meta):
        db_table = 'farmproavg'
        verbose_name = "农产品地区均价"
        verbose_name_plural = verbose_name
