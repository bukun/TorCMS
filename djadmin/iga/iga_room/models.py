import markdown
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField
from iga.iga_group.models import iga_group
from iga.iga_floor.models import iga_floor
from iga.iga_staff.models import iga_staff
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe


class iga_room(basemodel):
    building = models.CharField(blank=True, default='', max_length=255, verbose_name="所属楼")
    floor = models.ForeignKey(iga_floor, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='iga_room', verbose_name='所在楼层')
    duty =  models.ForeignKey(iga_staff, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='iga_room_duty', verbose_name='责任人')
    num = models.CharField(blank=True, null=False, max_length=255, verbose_name="房间号")
    group = models.ManyToManyField(iga_group, blank=True,
                                   related_name='iga_room', verbose_name='学科组名称')
    title = models.CharField(blank=True, null=False, max_length=255,
                             choices=[('1', '公共设施'), ('2', '办公室'),('3', '实验室'),('4', '档案室'),
                                      ('5', '会议室')],
                             default='2',
                             verbose_name="用途")
    attention = models.CharField(blank=True, null=False, max_length=255,
                             choices=[('1', '安全'), ('2', '危险')],
                             default='',
                             verbose_name="注意事项")

    photo = models.ImageField(upload_to='iga_room/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="照片")
    area = models.CharField(blank=True,default='', max_length=255, verbose_name="面积")
    areafloat = models.FloatField(blank=True, null=True, default=0,verbose_name="面积值")

    staff = models.CharField(blank=True, null=False, max_length=255, verbose_name="备注")
    operaters = models.ManyToManyField(iga_staff, blank=True,
                                 related_name='iga_room_operaters',verbose_name="使用人员")


    sites = models.ManyToManyField(Site, blank=True, related_name='iga_room', verbose_name='Site')

    floor_num = models.CharField(blank=True, null=False, max_length=255,unique=True, verbose_name="楼与房间号组合")
    def __str__(self):
        return self.title

    def get_html_content(self):
        html_content = markdown.markdown(self.cnt_md)
        return mark_safe(html_content)

    class Meta(basemodel.Meta):
        db_table = 'iga_room'
        verbose_name = "办公室"
        verbose_name_plural = verbose_name
