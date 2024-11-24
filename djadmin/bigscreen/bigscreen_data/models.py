import markdown
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
User = get_user_model()
from qgis.bigscreen_map_category.models import BigScreenMapCategory
from bigscreen.jump_btn.models import JumpBtn
from django.core.validators import MaxValueValidator, MinValueValidator

Fast_Jump_Chose = [
('0', '区县列表'),
('1', '快速跳转'),
]
class BigScreenData(basemodel):
    title = models.CharField(blank=True, unique=True, null=False, max_length=255, verbose_name="标题")
    qgis_map =  models.ManyToManyField(BigScreenMapCategory, related_name='big_screen_data', verbose_name="Qgis地图分类", null=True,
                                         blank=True)
    lat = models.FloatField(blank=True, null=True, default=0,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
                            verbose_name="纬度")
    lng = models.FloatField(blank=True, null=True, default=1,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)], verbose_name="经度")
    zoom = models.FloatField(blank=True, null=True, default=3,
        validators=[MinValueValidator(3.0), MaxValueValidator(18.0)],  verbose_name="初始缩放级别")
    pitch = models.FloatField(blank=True, null=True, default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(85.0)], verbose_name="地图倾斜角度")

    quxian_list = models.JSONField(null=True, default=dict, verbose_name='区县列表', blank=True)
    vector_layer =  models.JSONField(null=True, default=dict, verbose_name='矢量图层分类', blank=True)
    if_fast_jump_show = models.BooleanField(blank=False, null=True, verbose_name="是否显示快速跳转", default=True)
    fast_jump_chose = models.CharField(choices=Fast_Jump_Chose, verbose_name="快速跳转选择", default='0')
    fast_location_btn=models.ManyToManyField(JumpBtn, related_name='big_screen_data', verbose_name="快速跳转按钮", null=True,
                                         blank=True)
    if_qgismap_jump = models.BooleanField(blank=False, null=True, verbose_name="是否转到到图层位置", default=False)

    if_changchunprogram_list_show = models.BooleanField(blank=False, null=True, verbose_name="是否显示长春建筑工程列表", default=True)
    if_search_show = models.BooleanField(blank=False, null=True, verbose_name="是否显示地名检索框", default=True)

    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='bigscreendata', editable=False,
                             verbose_name='作者')
    sites = models.ManyToManyField(Site,blank=True, related_name='bigscreen_data', verbose_name='Site')


    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if not self.pk:  # 当创建新书籍时
    #         # 设置默认作者，这里假设默认作者ID为1
    #         default_site = Site.objects.get(pk=1)
    #         self.sites.add(default_site)
    #     super(BigScreenData, self).save(*args, **kwargs)
    class Meta(basemodel.Meta):
        db_table = 'bigscreen_data'
        verbose_name = "大屏数据"
        verbose_name_plural = verbose_name
