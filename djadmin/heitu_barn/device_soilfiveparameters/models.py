from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel

User = get_user_model()


class Soilfivepara1(basemodel):

    devid = models.CharField(null=False, max_length=36, help_text='设备id', verbose_name="设备id" )

    par_timestamp = models.IntegerField(null=False, default=0, help_text='注意，JSON获取的数据为浮点型')
    par_datetime = models.CharField(null=False, max_length=19, help_text='日期',verbose_name="日期" )
    typenum = models.CharField(max_length=100, help_text='设备编码',verbose_name="设备编码" )

    soiltemperature  = models.CharField( default=0, max_length=36, help_text='土壤温度(℃)', )
    soilmoisture  = models.CharField( default=0, max_length=36, help_text='土壤湿度(%)', )
    soilsalinity = models.CharField(default=0, max_length=36, help_text='土壤盐分(mS/cm)', )
    conductivity = models.CharField(default=0, max_length=36, help_text='电导率(mS/cm)', )
    phnum = models.CharField(default=0, max_length=36, help_text='PH', )
    dlnum = models.CharField(default=0, max_length=36, help_text='DL', )


    def __str__(self):
        return self.devid

    class Meta(basemodel.Meta):
        db_table = 'Soilfivepara1'
        verbose_name = "土壤五参数1数据"
        verbose_name_plural = verbose_name
