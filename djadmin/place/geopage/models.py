from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField

User = get_user_model()

class GeoPage(basemodel):


    title = models.CharField(blank=True, null=False, unique=True, max_length=255, verbose_name="标题")
    txt = MDTextField(verbose_name="内容", null=True, blank=True)
    extinfo = models.JSONField(null=True, default=dict, verbose_name='Extra data in JSON.', blank=True)

    # 判断指定字段长度,超出部分用省略号代替
    def update_content(self):
        if len(str(self.txt)) > 150:
            return '{}...'.format(str(self.txt)[0:150])
        else:
            return self.txt

    # 字段数据处理后,字段verbose_name参数失效
    # 需要重新指定,否则列表页字段名显示的是方法名(update_content)
    update_content.short_description = '内容'


    def __str__(self):
        return self.txt

    class Meta(basemodel.Meta):
        db_table = 'geopage'
        verbose_name = "地名页面"
        verbose_name_plural = verbose_name
