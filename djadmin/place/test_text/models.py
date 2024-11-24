from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from mdeditor.fields import MDTextField

User = get_user_model()

class TestText(basemodel):


    icon = models.CharField(blank=True,unique=True, null=False, max_length=255, verbose_name="图标")
    txt = MDTextField(verbose_name="内容", null=True, blank=True)


    def update_content(self):
        if len(str(self.txt)) > 150:
            return '{}...'.format(str(self.txt)[0:150])
        else:
            return self.txt

    # 字段数据处理后,字段verbose_name参数失效
    # 需要重新指定,否则列表页字段名显示的是方法名(update_content)
    update_content.short_description = '内容'
    def __str__(self):
        return self.txt

    class Meta(basemodel.Meta):
        db_table = 'testtext'
        verbose_name = "测试文本"
        verbose_name_plural = verbose_name
