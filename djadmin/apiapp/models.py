from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel

User = get_user_model()


class apiapp(basemodel):

    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    app_id = models.CharField(blank=True, null=True, default='1', max_length=255, verbose_name="App Id")
    cnt_md = models.TextField(verbose_name="内容",null=True)
    # category = models.ForeignKey(igaiscategory, on_delete=models.CASCADE, blank=True, null=True,
    #                              related_name='igaisdata', verbose_name='分类名称')

    def __str__(self):
        return self.title

    class Meta(basemodel.Meta):
        db_table = 'apiapp'
        verbose_name = "Api APP"
        verbose_name_plural = verbose_name
