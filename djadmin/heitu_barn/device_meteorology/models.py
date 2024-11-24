from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel

User = get_user_model()


class Meteorology(basemodel):

    devid = models.CharField(null=False, max_length=36, help_text='设备id', verbose_name="设备id" )

    par_timestamp = models.IntegerField(null=False, default=0, help_text='注意，JSON获取的数据为浮点型')
    par_datetime = models.CharField(null=False, max_length=19, help_text='日期',verbose_name="日期" )
    typenum = models.CharField(max_length=100, help_text='设备编码',verbose_name="设备编码" )

    windspeed  = models.CharField( default=0, max_length=36, help_text='风速(m/s)', )
    winddirection  = models.CharField( default=0, max_length=36, help_text='风向', )
    airtemperature = models.CharField(default=0, max_length=36, help_text='空气温度(℃)', )
    airhumidity = models.CharField(default=0, max_length=36, help_text='空气湿度(%)', )
    atmos = models.CharField(default=0, max_length=36, help_text='大气压力(kPa)', )
    radiation = models.CharField(default=0, max_length=36, help_text='总辐射（W/m2）', )
    rainfall = models.CharField(default=0, max_length=36, help_text='降雨量(mm)', )
    photosynthesis = models.CharField(default=0, max_length=36, help_text='光合有效1(umol* m2*s)', )
    watersurface = models.CharField(default=0, max_length=36, help_text='水面蒸发(mm)', )
    dlnum = models.CharField(default=0, max_length=36, help_text='DL', )


    def __str__(self):
        return self.devid

    class Meta(basemodel.Meta):
        db_table = 'Meteorology'
        verbose_name = "全自动气象站"
        verbose_name_plural = verbose_name
