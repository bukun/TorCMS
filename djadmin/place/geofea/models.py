from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField

User = get_user_model()

class Geofea(basemodel):

    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    cnt_md = MDTextField(verbose_name="内容", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, editable=False,
                             null=True, related_name='geofea', verbose_name='用户名',)
    status = models.BooleanField(blank=False, null=True, verbose_name="是否发布", default=0)


    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'geofeaq'
        verbose_name = "Geofea"
        verbose_name_plural = verbose_name
