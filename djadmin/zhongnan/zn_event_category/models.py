from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel, basecategory

User = get_user_model()


class ZNEventCategory(basemodel, basecategory):
    class Meta(basemodel.Meta):
        db_table = 'zn_event_category'
        verbose_name = "中南事件分类"
        verbose_name_plural = verbose_name
