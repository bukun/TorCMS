from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel

User = get_user_model()


class Devicesoilmoisture(basemodel):

    devid = models.CharField(null=False, max_length=36, help_text='设备id', verbose_name="设备id" )

    par_timestamp = models.IntegerField(null=False, default=0, help_text='注意，JSON获取的数据为浮点型')
    par_datetime = models.CharField(null=False, max_length=19, help_text='日期',verbose_name="日期" )
    typenum = models.CharField(max_length=100, help_text='设备编码',verbose_name="设备编码" )

    soiltemperature1  = models.CharField( default=0, max_length=36, help_text='土壤温度1(℃)', )
    soiltemperature2  = models.CharField( default=0, max_length=36, help_text='土壤温度2(℃)', )
    soiltemperature3  = models.CharField( default=0, max_length=36, help_text='土壤温度3(℃)', )
    soiltemperature4  = models.CharField( default=0, max_length=36, help_text='土壤温度4(℃)', )
    soiltemperature5  = models.CharField( default=0, max_length=36, help_text='土壤温度5(℃)', )
    soiltemperature6  = models.CharField( default=0, max_length=36, help_text='土壤温度6(℃)', )
    soiltemperature7  = models.CharField( default=0, max_length=36, help_text='土壤温度7(℃)', )
    soiltemperature8  = models.CharField( default=0, max_length=36, help_text='土壤温度8(℃)', )
    soiltemperature9  = models.CharField( default=0, max_length=36, help_text='土壤温度9(℃)', )
    soiltemperature10  = models.CharField( default=0, max_length=36, help_text='土壤温度10(℃)', )
    soiltemperature11  = models.CharField( default=0, max_length=36, help_text='土壤温度11(℃)', )
    soiltemperature12  = models.CharField( default=0, max_length=36, help_text='土壤温度12(℃)', )
    soiltemperature13  = models.CharField( default=0, max_length=36, help_text='土壤温度13(℃)', )
    soiltemperature14  = models.CharField( default=0, max_length=36, help_text='土壤温度14(℃)', )

    soilmoisture1 = models.CharField( default=0, max_length=36, help_text='土壤湿度1(%)', )
    soilmoisture2 = models.CharField( default=0, max_length=36, help_text='土壤湿度2(%)', )
    soilmoisture3 = models.CharField( default=0, max_length=36, help_text='土壤湿度3(%)', )
    soilmoisture4 = models.CharField( default=0, max_length=36, help_text='土壤湿度4(%)', )
    soilmoisture5 = models.CharField( default=0, max_length=36, help_text='土壤湿度5(%)', )
    soilmoisture6 = models.CharField( default=0, max_length=36, help_text='土壤湿度6(%)', )
    soilmoisture7 = models.CharField( default=0, max_length=36, help_text='土壤湿度7(%)', )
    soilmoisture8 = models.CharField( default=0, max_length=36, help_text='土壤湿度8(%)', )
    soilmoisture9 = models.CharField( default=0, max_length=36, help_text='土壤湿度9(%)', )
    soilmoisture10 = models.CharField( default=0, max_length=36, help_text='土壤湿度10(%)', )
    soilmoisture11 = models.CharField( default=0, max_length=36, help_text='土壤湿度11(%)', )
    soilmoisture12 = models.CharField( default=0, max_length=36, help_text='土壤湿度12(%)', )
    soilmoisture13 = models.CharField( default=0, max_length=36, help_text='土壤湿度13(%)', )
    soilmoisture14 = models.CharField( default=0, max_length=36, help_text='土壤湿度14(%)', )

    soilsalinity1 = models.CharField(default=0, max_length=36, help_text='土壤盐分1(mS)', )
    soilsalinity2 = models.CharField(default=0, max_length=36, help_text='土壤盐分2(mS)', )
    soilsalinity3 = models.CharField(default=0, max_length=36, help_text='土壤盐分3(mS)', )
    soilsalinity4 = models.CharField(default=0, max_length=36, help_text='土壤盐分4(mS)', )
    soilsalinity5 = models.CharField(default=0, max_length=36, help_text='土壤盐分5(mS)', )
    soilsalinity6 = models.CharField(default=0, max_length=36, help_text='土壤盐分6(mS)', )
    soilsalinity7 = models.CharField(default=0, max_length=36, help_text='土壤盐分7(mS)', )
    soilsalinity8 = models.CharField(default=0, max_length=36, help_text='土壤盐分8(mS)', )
    soilsalinity9 = models.CharField(default=0, max_length=36, help_text='土壤盐分9(mS)', )
    soilsalinity10 = models.CharField(default=0, max_length=36, help_text='土壤盐分10(mS)', )
    soilsalinity11 = models.CharField(default=0, max_length=36, help_text='土壤盐分11(mS)', )
    soilsalinity12 = models.CharField(default=0, max_length=36, help_text='土壤盐分12(mS)', )
    soilsalinity13 = models.CharField(default=0, max_length=36, help_text='土壤盐分13(mS)', )
    soilsalinity14 = models.CharField(default=0, max_length=36, help_text='土壤盐分14(mS)', )

    dlnum = models.CharField(default=0, max_length=36, help_text='DL',)


    def __str__(self):
        return self.devid

    class Meta(basemodel.Meta):
        db_table = 'Devicesoilmoisture'
        verbose_name = "土壤水分数据"
        verbose_name_plural = verbose_name
