from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from django.contrib.gis.db import models as gismodels
User = get_user_model()
class ChangChunProject(basemodel):
    cadastre_id = models.CharField(blank=True, null=False, max_length=255,unique=True, verbose_name="地籍号")
    name = models.CharField(blank=True, null=True, max_length=255, verbose_name="项目名称（建设工程名称）")
    xmdz = models.CharField(blank=True, null=True, max_length=255, verbose_name="项目地址")
    company = models.CharField(blank=True, null=True, max_length=255, verbose_name="建设单位（建设单位名称）")
    jzd = models.CharField(blank=True, null=True, max_length=255, verbose_name="建字第 业务阶段（证号）")
    xkz = models.CharField(blank=True, null=True, max_length=255, verbose_name="建设用地规划许可证")
    hzd = models.CharField(blank=True, null=True, max_length=255, verbose_name="核字第")
    dzd = models.CharField(blank=True, null=True, max_length=255, verbose_name="地字第")

    location = gismodels.PolygonField(null=True, blank=True, verbose_name="位置")
    def __str__(self):
        return self.cadastre_id


    class Meta(basemodel.Meta):
        db_table = 'changchun_project'
        verbose_name = "ChangChunProject"
        verbose_name_plural = verbose_name
