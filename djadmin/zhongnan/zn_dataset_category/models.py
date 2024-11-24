from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel, basecategory

User = get_user_model()


class ZNDatasetCategory(basemodel, basecategory):
    class Meta(basemodel.Meta):
        db_table = 'zn_dataset_category'
        verbose_name = "中南数据分类"
        verbose_name_plural = verbose_name
