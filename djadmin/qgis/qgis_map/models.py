import markdown
from django.utils.safestring import mark_safe
from django.db import models
from django.contrib.auth import get_user_model
from base.models import basemodel, basecategory
from django.contrib.sites.models import Site

User = get_user_model()


class ANSOMapCategory(basemodel, basecategory):
    sites = models.ManyToManyField(Site, blank=True, related_name='ansomapcategory', verbose_name='Site')

    class Meta(basemodel.Meta):
        db_table = 'ansomapcategory'
        verbose_name = "ANSO地图分类"
        verbose_name_plural = verbose_name


class heitumapcategory(basemodel, basecategory):
    sites = models.ManyToManyField(Site, blank=True, related_name='heitumapcategory', verbose_name='Site')

    class Meta(basemodel.Meta):
        db_table = 'heitumapcategory'
        verbose_name = "黑土地图分类"
        verbose_name_plural = verbose_name


class BigScreenMapCategory(basemodel, basecategory):
    sites = models.ManyToManyField(Site, blank=True, related_name='bigscreen_map_category', verbose_name='Site')

    class Meta(basemodel.Meta):
        db_table = 'bigscreen_map_category'
        verbose_name = "大屏地图分类"
        verbose_name_plural = verbose_name


class yaoumapcategory(basemodel, basecategory):
    sites = models.ManyToManyField(Site, blank=True, related_name='yaoumapcategory', verbose_name='Site')

    class Meta(basemodel.Meta):
        db_table = 'yaoumapcategory'
        verbose_name = "亚欧地图分类"
        verbose_name_plural = verbose_name


class zhongmengmapcategory(basemodel, basecategory):
    sites = models.ManyToManyField(Site, blank=True, related_name='zhongmengmapcategory', verbose_name='Site')

    class Meta(basemodel.Meta):
        db_table = 'zhongmengmapcategory'
        verbose_name = "色楞格河地图分类"
        verbose_name_plural = verbose_name


class zhongbamapcategory(basemodel, basecategory):
    sites = models.ManyToManyField(Site, blank=True, related_name='zhongbamapcategory', verbose_name='Site')

    class Meta(basemodel.Meta):
        db_table = 'zhongbamapcategory'
        verbose_name = "中巴地图分类"
        verbose_name_plural = verbose_name


class QgisLabel(basemodel):
    name = models.CharField(blank=True, unique=True, null=False, max_length=255, verbose_name="标签名称")
    sites = models.ManyToManyField(Site, blank=True, related_name='qgislabel', verbose_name='Site')

    def __str__(self):
        return self.name

    class Meta(basemodel.Meta):
        db_table = 'qgislabel'
        verbose_name = "文档标签"
        verbose_name_plural = verbose_name


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
    sites = models.ManyToManyField(Site, blank=True, related_name='vectorlayer', verbose_name='Site')

    def get_en_html_content(self):
        html_content = markdown.markdown(self.cnt_md)
        return mark_safe(html_content)

    def __str__(self):
        return self.mapid

    class Meta(basemodel.Meta):
        db_table = 'vectorlayer'
        verbose_name = "矢量图层管理"
        verbose_name_plural = verbose_name


class qgismap(basemodel):
    mapid = models.CharField(blank=True, null=False, max_length=255, verbose_name='地图ID')
    title = models.CharField(blank=True, null=False, max_length=255, verbose_name="标题")
    en_title = models.CharField(blank=True, null=True, max_length=255, verbose_name="英文标题")
    cnt_md = models.TextField(verbose_name="简介", blank=True, null=True)
    en_cnt_md = models.TextField(verbose_name="英文简介", blank=True, null=True)
    lat = models.CharField(blank=True, null=True, default=0, max_length=255, verbose_name="纬度")
    lon = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="经度")
    zoom_current = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="初始缩放级别")
    zoom_min = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="最大缩放级别")
    zoom_max = models.CharField(blank=True, null=True, default=1, max_length=255, verbose_name="最小缩放级别")
    layer_name = models.CharField(blank=True, null=True, default='', max_length=255, verbose_name="地图名称")
    url = models.TextField(null=True, blank=True, default='', verbose_name="地址")
    path = models.TextField(null=True, blank=True, default='', verbose_name="路径")
    host = models.CharField(blank=True, null=True, default='', max_length=255, verbose_name="host")
    name = models.CharField(blank=True, null=True, default='', max_length=255, verbose_name="名称")
    date = models.DateTimeField(verbose_name='创建日期', auto_now_add=True)
    label = models.ManyToManyField(QgisLabel, related_name='qgismap', verbose_name='标签', blank=True)

    zhongbacategory = models.ForeignKey(zhongbamapcategory, on_delete=models.CASCADE, blank=True, null=True,
                                        related_name='zhongbadata', verbose_name='中巴地图分类名称')
    yaoucategory = models.ForeignKey(yaoumapcategory, on_delete=models.CASCADE, blank=True, null=True,
                                     related_name='yaoudata', verbose_name='亚欧地图分类名称')
    zhongmengcategory = models.ForeignKey(zhongmengmapcategory, on_delete=models.CASCADE, blank=True, null=True,
                                          related_name='zhongmengdata', verbose_name='色楞格河地图分类名称')
    heitucategory = models.ForeignKey(heitumapcategory, on_delete=models.CASCADE, blank=True, null=True,
                                      related_name='heitudata', verbose_name='黑土地图分类名称')
    ansocategory = models.ForeignKey(ANSOMapCategory, on_delete=models.CASCADE, blank=True, null=True,
                                     related_name='ansodata', verbose_name='ANSO地图分类名称')
    bigscreencategory = models.ManyToManyField(BigScreenMapCategory, blank=True,
                                               related_name='bigscreendata', verbose_name='大屏数据分类')
    logo = models.ImageField(upload_to='qgismap/imgs/', max_length=255, null=True, blank=True,
                             verbose_name="LOGO")
    sites = models.ManyToManyField(Site, blank=True, related_name='qgismap', verbose_name='Site')

    def get_en_html_content(self):
        html_content = markdown.markdown(self.en_cnt_md)
        return mark_safe(html_content)

    def __str__(self):
        return self.mapid

    class Meta(basemodel.Meta):
        db_table = 'qgismap'
        verbose_name = "QGIS地图"
        verbose_name_plural = verbose_name
