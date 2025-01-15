from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from base.models import basemodel

User = get_user_model()


class Barndataset(basemodel):
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    logo = models.ImageField(upload_to='barn_dataset/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")

    cnt_md = models.TextField(verbose_name="内容", null=True)
    location = gismodels.PointField(null=True, blank=True, verbose_name="位置", default=(Point(0, 0, srid=4326)))

    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'Barndataset'
        verbose_name = "农业站照片"
        verbose_name_plural = verbose_name

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

class Barndevice(basemodel):
    name = models.CharField(blank=True, null=False, max_length=255, verbose_name="设备名称")
    deviceid = models.CharField(blank=True, null=False, max_length=255, verbose_name="设备id")
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")

    cnt_md = models.TextField(verbose_name="内容", null=True)
    location = gismodels.PointField(null=True, blank=True, verbose_name="位置", default=(Point(0, 0, srid=4326)))
    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)

    def __str__(self):
        return self.name

    class Meta(basemodel.Meta):
        db_table = 'Barndevice'
        verbose_name = "农业站设备"
        verbose_name_plural = verbose_name


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

class Soilfiveparav2(basemodel):

    devid = models.CharField(null=False, max_length=36, help_text='设备id', verbose_name="设备id" )

    par_timestamp = models.IntegerField(null=False, default=0, help_text='注意，JSON获取的数据为浮点型')
    par_datetime = models.CharField(null=False, max_length=19, help_text='日期',verbose_name="日期" )
    typenum = models.CharField(max_length=100, help_text='设备编码',verbose_name="设备编码" )

    soiltemperature = models.CharField(default=0, max_length=36, help_text='土壤温度(℃)', )
    soilmoisture = models.CharField(default=0, max_length=36, help_text='土壤湿度(%)', )
    soilsalinity = models.CharField(default=0, max_length=36, help_text='土壤盐分(mS/cm)', )
    conductivity = models.CharField(default=0, max_length=36, help_text='电导率(mS/cm)', )
    phnum = models.CharField(default=0, max_length=36, help_text='PH', )
    dlnum = models.CharField(default=0, max_length=36, help_text='DL', )


    def __str__(self):
        return self.devid

    class Meta(basemodel.Meta):
        db_table = 'Soilfiveparav2'
        verbose_name = "土壤五参数2数据"
        verbose_name_plural = verbose_name


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