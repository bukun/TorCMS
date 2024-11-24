import markdown
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()

class JumpBtn(basemodel):
    name = models.CharField(blank=True, unique=True, null=False, max_length=255, verbose_name="名称")

    lat = models.FloatField(blank=True, null=True, default=0,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
                            verbose_name="纬度")
    lng = models.FloatField(blank=True, null=True, default=1,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)], verbose_name="经度")
    zoom = models.FloatField(blank=True, null=True, default=3,
        validators=[MinValueValidator(3.0), MaxValueValidator(18.0)],  verbose_name="初始缩放级别")


    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='jumpbtn', editable=False,
                             verbose_name='作者')


    def __str__(self):
        return self.name


    class Meta(basemodel.Meta):
        db_table = 'jump_btn'
        verbose_name = "跳转按钮管理"
        verbose_name_plural = verbose_name
