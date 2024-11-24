from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel

User = get_user_model()


class TranslationZHEN(basemodel):
    text_zh = models.TextField(blank=True, null=True, unique=True, verbose_name="中文内容")
    trans_en = models.TextField(blank=True, null=False, verbose_name="英文内容")

    def __str__(self):
        return str(self.id)

    class Meta(basemodel.Meta):
        db_table = 'trans_zh_en'
        verbose_name = "中-英翻译"
        verbose_name_plural = verbose_name
