from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel

User = get_user_model()


class farmpro(basemodel):
    product_name = models.CharField(blank=True, null=False, default='',max_length=255, verbose_name='农产品名称')
    unit = models.CharField(blank=True, null=False, default='',max_length=255, verbose_name="单位")
    address = models.CharField(blank=True, null=False,default='', max_length=255, verbose_name="地址")
    money = models.CharField(blank=True, null=False,default='', max_length=255, verbose_name="价格")
    date_update = models.CharField(blank=True, null=False,default='', max_length=255, verbose_name="更新时间")
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='farmpro',editable=True,
                             verbose_name='用户名')


    def __str__(self):
        return self.product_name

    class Meta(basemodel.Meta):
        db_table = 'farmpro'
        verbose_name = "农产品最新价格"
        verbose_name_plural = verbose_name
