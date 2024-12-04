
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField

User = get_user_model()

class Photoinfo(basemodel):

    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    cnt_md = MDTextField(verbose_name="内容", null=True, blank=True)
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")
    logo = models.ImageField(upload_to='photo_info/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="图片")



    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'photoinfo'
        verbose_name = "Photoinfo"
        verbose_name_plural = verbose_name
