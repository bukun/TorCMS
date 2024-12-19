import markdown
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField
from iga.iga_group.models import iga_group
from iga.iga_floor.models import iga_floor
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe


class iga_room(basemodel):
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="办公室")
    num = models.CharField(blank=True, null=False, max_length=255, verbose_name="房间号")
    area = models.CharField(blank=True,default='', max_length=255, verbose_name="面积")
    staff = models.CharField(blank=True,default='',  max_length=255, verbose_name="使用人员")

    cnt_md = MDTextField(verbose_name="用途",default='', blank=True)

    building = models.CharField(blank=True,default='',  max_length=255, verbose_name="所属楼")
    sites = models.ManyToManyField(Site, blank=True, related_name='iga_room', verbose_name='Site')

    group = models.ManyToManyField(iga_group, blank=True,
                                 related_name='iga_room', verbose_name='学科组名称')
    floor = models.ForeignKey(iga_floor, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='iga_room', verbose_name='所在楼层')

    def __str__(self):
        return self.title

    def get_html_content(self):
        html_content = markdown.markdown(self.cnt_md)
        return mark_safe(html_content)

    class Meta(basemodel.Meta):
        db_table = 'iga_room'
        verbose_name = "办公室"
        verbose_name_plural = verbose_name
