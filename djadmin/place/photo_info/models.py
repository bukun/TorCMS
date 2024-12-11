import exifread
import os
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
    def save(self, *args, **kwargs):
        super(Photoinfo, self).save(*args, **kwargs)
        if self.logo:
            self.convert_to_photo()
            super(Photoinfo, self).save(*args, **kwargs)


    def convert_to_photo(self):
        print('asdasdf')

        print(self.logo)
        file_src = os.path.join(self.logo.path)
        print(file_src)
        x,y = self.get_single_gps(file_src)
        print(x,y)
    def get_single_gps(self,img):
        with open(str(img), 'rb') as f:
            # 直接读取度分秒格式的经纬度数据
            contents = exifread.process_file(f)
            try:
                longitude = contents["GPS GPSLongitude"].values
                has_longitude = True
            except:
                has_longitude = False
            if not has_longitude:
                return '', ''
            else:
                longitude = contents["GPS GPSLongitude"].values
                latitude = contents["GPS GPSLatitude"].values
                # 度分秒转换成十进制数据
                longitude_f = longitude[0].num / longitude[0].den + (longitude[1].num / longitude[1].den / 60) + (
                        longitude[2].num / longitude[2].den / 3600)
                latitude_f = latitude[0].num / latitude[0].den + (latitude[1].num / latitude[1].den / 60) + (
                        latitude[2].num / latitude[2].den / 3600)
                return longitude_f, latitude_f


    class Meta(basemodel.Meta):
        db_table = 'photoinfo'
        verbose_name = "Photoinfo"
        verbose_name_plural = verbose_name
