from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
User = get_user_model()


class ZNDatasetLabel(basemodel):
    name = models.CharField(blank=True, unique=True, null=False, max_length=255, verbose_name="标签名称")


    def __str__(self):
        return self.name

    class Meta(basemodel.Meta):
        db_table = 'zn_dataset_labels'
        verbose_name = "中南数据标签"
        verbose_name_plural = verbose_name
