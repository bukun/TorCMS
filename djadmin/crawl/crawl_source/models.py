from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel

User = get_user_model()


class CrawlSource(basemodel):
    title = models.CharField(null=False, max_length=255, verbose_name="标题")
    url = models.URLField(verbose_name="网址")

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'crawlsource'
        verbose_name = "爬取数据来源"
        verbose_name_plural = verbose_name
