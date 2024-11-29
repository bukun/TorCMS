import markdown
from django.utils.safestring import mark_safe
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel
from qgis.yaou_map_category.models import yaoumapcategory
from qgis.zhongba_map_category.models import zhongbamapcategory
from qgis.zhongmeng_map_category.models import zhongmengmapcategory
from qgis.heitu_map_category.models import heitumapcategory
from qgis.anso_map_category.models import ANSOMapCategory
from qgis.qgis_label.models import QgisLabel
from qgis.bigscreen_map_category.models import BigScreenMapCategory
from django.contrib.sites.models import Site
User = get_user_model()

Fast_Jump_Chose = [
('0', 'symbol'),
('1', 'fill'),
('2', 'circle'),
('3', 'line'),
]

class vectorlayer(basemodel):
    mapid = models.CharField(blank=True, null=False, max_length=255, verbose_name='地图ID')
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    en_title = models.CharField(blank=True, null=True, max_length=255, verbose_name="英文标题")


    type = models.CharField(choices=Fast_Jump_Chose, verbose_name="数据类型", default='0', max_length=255)

    # symbol
    textcolor = models.CharField(blank=True, null=True, max_length=255, verbose_name="字体颜色")
    texthalocolor = models.CharField(blank=True, null=True, max_length=255, verbose_name="字体轮廓颜色")
    texthalowidth = models.CharField(blank=True, null=True, max_length=255, verbose_name="字体轮廓颜色")
    textopacity = models.CharField(blank=True, null=True, max_length=255, verbose_name="字体透明度")


    # line
    linecolor = models.CharField(blank=True, null=True, max_length=255, verbose_name="线条颜色")
    linewidth = models.CharField(blank=True, null=True, max_length=255, verbose_name="线条宽度")
    lineopacity = models.CharField(blank=True, null=True, max_length=255, verbose_name="线条透明度")




    # fill
    fillcolor = models.CharField(blank=True, null=True, max_length=255, verbose_name="面颜色")
    fillopacity = models.CharField(blank=True, null=True, max_length=255, verbose_name="面透明度")
    filloutlinecolor = models.CharField(blank=True, null=True, max_length=255, verbose_name="面轮廓颜色")

    # circle
    circleradius = models.CharField(blank=True, null=True, max_length=255, verbose_name="圆点直径")

    cnt_md = models.TextField(verbose_name="简介", blank=True, null=True)
    # en_cnt_md = models.TextField(verbose_name="英文简介", blank=True, null=True)
    # lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    # lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")
    # zoom_current = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="初始缩放级别")
    # zoom_min = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="最大缩放级别")
    # zoom_max = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="最小缩放级别")
    # layer_name = models.CharField(blank=True, null=True, default='', max_length=255, verbose_name="地图名称")
    url = models.TextField(null=True, blank=True, default='', verbose_name="地址")
    path = models.TextField(null=True, blank=True, default='', verbose_name="路径")
    host = models.CharField(blank=True, null=True, default='', max_length=255, verbose_name="host")
    # name = models.CharField(blank=True, null=True, default='', max_length=255, verbose_name="名称")
    # date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    label = models.ManyToManyField(QgisLabel, related_name='vectorlayer',
                                   verbose_name='标签', blank=True)

    bigscreencategory = models.ManyToManyField(BigScreenMapCategory, blank=True,
                                      related_name='qgismapbigscreen', verbose_name='大屏数据分类')
    # logo = models.ImageField(upload_to='vectorlayer/imgs/', max_length=255, null=True, blank=True,
    #                          verbose_name="LOGO")
    sites = models.ManyToManyField(Site,blank=True, related_name='vectorlayer', verbose_name='Site')
    def get_html_content(self):
        html_content = markdown.markdown(self.cnt_md)
        return mark_safe(html_content)

    def get_en_html_content(self):
        html_content = markdown.markdown(self.en_cnt_md)
        return mark_safe(html_content)
    def __str__(self):
        return self.mapid

    class Meta(basemodel.Meta):
        db_table = 'vectorlayer'
        verbose_name = "矢量图层管理"
        verbose_name_plural = verbose_name
