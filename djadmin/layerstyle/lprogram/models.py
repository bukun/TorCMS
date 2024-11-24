from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
# from mdeditor.fields import MDTextField
from django.contrib.sites.models import Site
User = get_user_model()

class lprogram(basemodel):


    user = models.ForeignKey(User,db_constraint=False, on_delete=models.CASCADE, blank=True, null=True, related_name='other_user',
                                  verbose_name='项目负责人')
    title = models.CharField(blank=True, null=False, unique=True, max_length=255, verbose_name="项目名称")
    sites = models.ManyToManyField(Site,blank=True, related_name='lprogram', verbose_name='Site')

    extinfo = models.JSONField(null=True, default=dict, verbose_name='GeoJSON数据', blank=True)

    # # 判断指定字段长度,超出部分用省略号代替
    # def update_content(self):
    #     if len(str(self.txt)) > 150:
    #         return '{}...'.format(str(self.txt)[0:150])
    #     else:
    #         return self.txt
    #
    # # 字段数据处理后,字段verbose_name参数失效
    # # 需要重新指定,否则列表页字段名显示的是方法名(update_content)
    # update_content.short_description = '内容'


    def __str__(self):
        return str(self.user)

    class Meta(basemodel.Meta):
        db_table = 'lprogram'
        verbose_name = '在线制图项目'
        verbose_name_plural = verbose_name
