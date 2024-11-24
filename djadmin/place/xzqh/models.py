from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField
from mptt.models import MPTTModel, TreeForeignKey
User = get_user_model()


class XZQH(MPTTModel,basemodel):
    '''
    行政区划
    '''

    zoning = models.CharField(max_length=255, unique=True, blank=True, null=False, verbose_name="行政区划代码")
    name = models.CharField(max_length=255, blank=True, null=False, verbose_name="名称")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name='上级名称')
    content = MDTextField(verbose_name="介绍", null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta(basemodel.Meta):
        db_table = 'xzqh'
        verbose_name = "行政区划"
        verbose_name_plural = verbose_name
