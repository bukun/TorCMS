from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel, basecategory

User = get_user_model()


class language(models.IntegerChoices):
    type1 = 1, '英文'
    type2 = 2, '中文'


class CrawlLabel(basemodel, basecategory):
    is_en = models.IntegerField(choices=language.choices, verbose_name="语言", default=1)

    class Meta(basemodel.Meta):
        db_table = 'crawllabel'
        verbose_name = "爬取文档标签"
        verbose_name_plural = verbose_name
