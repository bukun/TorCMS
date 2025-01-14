import markdown
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from django.contrib.sites.models import Site

class iga_group(basemodel):
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="学科组")
    group_type = models.CharField(blank=True, null=False, choices=[('1', '学科组'), ('2', '管理支撑部门'),('3', '野外台站')],
                                 default='1',
                                  max_length=255, verbose_name="学科组")
    sites = models.ManyToManyField(Site, blank=True, related_name='iga_group', verbose_name='Site')

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'iga_group'
        verbose_name = "学科组"
        verbose_name_plural = verbose_name

class iga_floor(basemodel):
    num = models.CharField(blank=True, null=False, max_length=255, verbose_name="楼层")
    build = models.CharField(blank=True, null=False, max_length=255, verbose_name="所属楼")
    sites = models.ManyToManyField(Site, blank=True, related_name='iga_floor', verbose_name='Site')

    def __str__(self):
        return self.num

    class Meta(basemodel.Meta):
        db_table = 'iga_floor'
        verbose_name = "楼层"
        verbose_name_plural = verbose_name

class iga_staff(basemodel):
    name = models.CharField(blank=True, null=False, max_length=255, verbose_name="人员名")
    sites = models.ManyToManyField(Site, blank=True, related_name='iga_staff', verbose_name='Site')

    def __str__(self):
        return self.name

    class Meta(basemodel.Meta):
        db_table = 'iga_staff'
        verbose_name = "人员"
        verbose_name_plural = verbose_name



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



    class Meta(basemodel.Meta):
        db_table = 'iga_room'
        verbose_name = "办公室"
        verbose_name_plural = verbose_name